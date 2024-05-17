from datetime import datetime, timedelta
import json
import textwrap
import time
from typing import Any, Tuple, List
import base64
from urllib.error import HTTPError

from pandas import DataFrame
import pandas as pd
import re
import decimal

from relationalai import debugging

from ..errors import Errors, RAIException
from ..rel_utils import assert_no_problems
from ..loaders.loader import emit_delete_import, import_file, list_available_resources
from .config import Config
from .types import ImportSource, ImportSourceFile
from .client import Client, ResourceProvider
from .. import dsl, rel, metamodel as m
from railib import api

#--------------------------------------------------
# Constants
#--------------------------------------------------

UNIXEPOCH = 62135683200000
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
TXN_FIELDS = ["id", "account_name", "state", "created_on", "finished_at", "duration", "database_name", "read_only", "engine_name", "query", "query_size", "tags", "user_agent", "response_format_version"]
TXN_REPLACE_MAP = {"database_name": "database", "engine_name": "engine", "account_name": "account", "user_agent": "agent"}
VALID_ENGINE_STATES = ["REQUESTED", "PROVISIONED", "PROVISIONING"]

#--------------------------------------------------
# Resources
#--------------------------------------------------

class Resources(ResourceProvider):
    def __init__(self, profile:str|None=None, config:Config|None=None):
        super().__init__(profile, config=config)
        self._ctx = None

    def _api_ctx(self):
        if not self._ctx:
            self._ctx = api.Context(**self.config.to_rai_config())
        return self._ctx

    def reset(self):
        self._ctx = None

    #--------------------------------------------------
    # Generic
    #--------------------------------------------------

    def get_version(self):
        raise Exception("Azure version not available")

    #--------------------------------------------------
    # Databases
    #--------------------------------------------------

    def get_database(self, name:str):
        return api.get_database(self._api_ctx(), name)

    #--------------------------------------------------
    # Engines
    #--------------------------------------------------

    def list_engines(self, state:str|None = None):
        return api.list_engines(self._api_ctx(), state)

    def get_engine(self, name:str):
        return api.get_engine(self._api_ctx(), name)

    def is_valid_engine_state(self, state:str):
        return state in VALID_ENGINE_STATES

    def create_engine(self, name:str, size:str, pool:str=""):
        with debugging.span("create_engine", name=name, size=size):
            return api.create_engine_wait(self._api_ctx(), name, size)

    def delete_engine(self, name:str):
        return api.delete_engine(self._api_ctx(), name)

    def suspend_engine(self, name:str):
        return api.suspend_engine(self._api_ctx(), name)

    def resume_engine(self, name:str):
        return api.resume_engine_wait(self._api_ctx(), name)

    #--------------------------------------------------
    # Graphs
    #--------------------------------------------------

    def list_graphs(self) -> List[Any]:
        with debugging.span("list_models"):
            return api.list_databases(self._api_ctx())

    def get_graph(self, name:str):
        with debugging.span("get_model", name=name):
            return api.get_database(self._api_ctx(), name)

    def create_graph(self, name: str):
        with debugging.span("create_model", name=name):
            return api.create_database(self._api_ctx(), name)

    def delete_graph(self, name:str):
        with debugging.span("delete_model", name=name):
            return api.delete_database(self._api_ctx(), name)

    #--------------------------------------------------
    # Models
    #--------------------------------------------------

    def list_models(self, database: str, engine: str):
        return api.list_databases(self._api_ctx())

    def create_models(self, database: str, engine: str, models:List[Tuple[str, str]]) -> List[Any]:
        rel_code = self.create_models_code(models)
        results = self.exec_raw(database, engine, rel_code, readonly=False)
        if results.problems:
            return results.problems
        return []

    def delete_model(self, database:str, engine:str, name:str):
        return api.delete_model(self._api_ctx(), database, engine, name)

    def create_models_code(self, models:List[Tuple[str, str]]) -> str:
        lines = []
        for (name, code) in models:
            name = name.replace("\"", "\\\"")
            assert "\"\"\"\"\"\"\"" not in code, "Code literals must use fewer than 7 quotes."

            lines.append(textwrap.dedent(f"""
            def delete[:rel, :catalog, :model, "{name}"]: rel[:catalog, :model, "{name}"]
            def insert[:rel, :catalog, :model, "{name}"]: raw\"\"\"\"\"\"\"
            """) + code + "\n\"\"\"\"\"\"\"")
        rel_code = "\n\n".join(lines)
        return rel_code

    #--------------------------------------------------
    # Exports
    #--------------------------------------------------

    def list_exports(self, database: str, engine: str):
        raise Exception("Azure doesn't support exports")

    def create_export(self, database: str, engine: str, name: str, inputs: List[str], out_fields: List[str], code: str):
        raise Exception("Azure doesn't support exports")

    def delete_export(self, database: str, engine: str, name: str):
        raise Exception("Azure doesn't support exports")

    #--------------------------------------------------
    # Imports
    #--------------------------------------------------

    def list_imports(self, model:str|None, id:str|None, status:str|None = None, name:str|None = None, creator:str|None = None):
        return [*list_available_resources(self, model, self.get_default_engine_name()).values()]

    def create_import_stream(self, source:ImportSource, model:str, rate = 1, options: dict|None = None):
        raise Exception("Azure doesn't support import streams")

    def create_import_snapshot(self, source:ImportSource, model:str, options: dict|None = None):
        assert isinstance(source, ImportSourceFile), "Azure integration only supports loading from files and URLs right now."
        import_file(self, model, source, **(options or {}))

    def delete_import(self, import_name: str, model:str):
        res = self.exec_raw(model, self.get_default_engine_name(), emit_delete_import(import_name), False)
        assert_no_problems(res)

    def set_imports_engine(self, engine:str):
        raise Exception("Azure doesn't support setting imports engine")

    def change_imports_status(self, status:str):
        raise Exception("Azure doesn't support import status changes")

    def change_stream_status(self, stream_id: str, model:str, suspend: bool):
        raise Exception("Azure doesn't support stream status changes")

    def get_import_stream(self, stream_id: str, model:str):
        raise Exception("Azure doesn't support get import streams")

    #--------------------------------------------------
    # Exec
    #--------------------------------------------------

    def exec_raw(self, database:str, engine:str, raw_code:str, readonly=True, raw_results=True, inputs: dict = {}):
        try:
            with debugging.span("transaction") as txn_span:
                ctx = self._api_ctx()
                with debugging.span("create"):
                    txn = api.exec_async(ctx, database, engine, raw_code, readonly=readonly, inputs=inputs)
                txn_id = txn.transaction["id"]
                txn_span["txn_id"] = txn_id

                # TODO: dedup with SDK
                rsp = api.TransactionAsyncResponse()
                txn = api.get_transaction(ctx, txn_id)
                start_time = time.time()

                def check_done():
                    with debugging.span("check_status"):
                        state = api.get_transaction(ctx, txn_id)["state"]
                        return api.is_txn_term_state(state)

                with debugging.span("wait", txn_id=txn_id):
                    api.poll_with_specified_overhead(
                        check_done,
                        overhead_rate=0.2,
                        start_time=start_time,
                    )

                # TODO: parallelize
                with debugging.span("fetch"):
                    rsp.transaction = api.get_transaction(ctx, txn_id)
                    rsp.metadata = api.get_transaction_metadata(ctx, txn_id)
                    rsp.problems = api.get_transaction_problems(ctx, txn_id)
                    with debugging.span("fetch_results"):
                        rsp.results = api.get_transaction_results(ctx, txn_id)

                return rsp
        except HTTPError as err:
            res = json.loads(err.read().decode())
            # RAI API uses a JSON payload in the body to explain why the request failed
            # This annotates the error with that to make the exception actually useful.
            if "engine not found" in res.get('message', ''):
                print("") # the SDK appears to print some stuff before the error message
                Errors.engine_not_found(self.config.get("engine", "Unknown"), res.get('message'))
            raise RAIException(f" {res.get('message', '')} {res.get('details', '')}")

    def _has_errors(self, results):
        if len(results.problems):
            for problem in results.problems:
                if problem.get('is_error') or problem.get('is_exception'):
                    return True

    def format_results(self, results, task:m.Task|None=None) -> Tuple[DataFrame, List[Any]]:
        data_frame = DataFrame()
        if len(results.results):
            ret_cols = task.return_cols() if task else []
            for result in results.results:
                types = [t for t in result["relationId"].split("/") if t != "" and not t.startswith(":")]
                result_frame:DataFrame = result["table"].to_pandas()
                for i, col in enumerate(result_frame.columns):
                    if "UInt128" in types[i]:
                        result_frame[col] = result_frame[col].apply(lambda x: base64.b64encode(x.tobytes()).decode()[:-2])
                    elif "FixedDecimal" in types[i]:
                        decimal_info = re.search(r"FixedDecimal\{Int(\d+), (\d+)\}", types[i])
                        if decimal_info:
                            bits = int(decimal_info.group(1))
                            scale = int(decimal_info.group(2))
                            if bits == 128:
                                result_frame[col] = result_frame[col].apply(lambda x: (decimal.Decimal(str((int(x[1]) << 64) + int(x[0]))) if x[1] > 0 else decimal.Decimal(str(x[0]))) / (10 ** scale))
                            else:
                                result_frame[col] = result_frame[col].apply(lambda x: decimal.Decimal(str(x)) / (10 ** scale))
                    elif "Int128" in types[i]:
                        result_frame[col] = result_frame[col].apply(lambda x: (int(x[1]) << 64) + int(x[0]) if x[1] > 0 else x[0])
                    elif types[i] == "Dates.DateTime":
                        result_frame[col] = pd.to_datetime(result_frame[col] - UNIXEPOCH, unit="ms")
                    elif types[i] == "Dates.Date":
                        result_frame[col] = pd.to_datetime(result_frame[col] * MILLISECONDS_PER_DAY - UNIXEPOCH, unit="ms")
                if len(ret_cols) and len(result_frame.columns) == len(ret_cols):
                    result_frame.columns = ret_cols[0:len(result_frame.columns)]
                result["table"] = result_frame
                if ":output" in result["relationId"]:
                    data_frame = pd.concat([data_frame, result_frame], ignore_index=True)
        return (data_frame, results.problems)

    #--------------------------------------------------
    # Transactions
    #--------------------------------------------------

    def get_transaction(self, transaction_id):
        txn = api.get_transaction(self._api_ctx(), transaction_id)
        if not txn:
            return None
        created_on = txn.get("created_on")
        finished_at = txn.get("finished_at")
        duration = txn.get("duration")
        if duration:
            txn["duration"] = timedelta(milliseconds=duration)
        else:
            txn["duration"] = datetime.now() - datetime.fromtimestamp(created_on / 1000)
        if created_on:
            txn["created_on"] = datetime.fromtimestamp(created_on / 1000)
        if finished_at:
            txn["finished_at"] = datetime.fromtimestamp(finished_at / 1000)
        # Remap based on the fields we care about
        result = {TXN_REPLACE_MAP.get(k, k): v for k, v in txn.items() if k in TXN_FIELDS}
        return result

    def remap_fields(self, transactions):
        if not transactions:
            return []
        for transaction in transactions:
            for key in list(transaction.keys()):
                if key in TXN_REPLACE_MAP:
                    transaction[TXN_REPLACE_MAP[key]] = transaction.pop(key)
        return transactions

    def list_transactions(self, **kwargs):
        TERMINAL_STATES = ["COMPLETED", "ABORTED"]
        VALID_KEYS = ["id", "state"]

        state = kwargs.get("state")
        only_active = kwargs.get("only_active", False)
        options = {}

        # Azure sdk supports more than just VALID_KEYS as filters but for now we pass through those
        for k, v in kwargs.items():
            if k in VALID_KEYS and v is not None:
                # Only pass state if it is a valid terminal state
                if k == "state" and v.upper() in TERMINAL_STATES:
                    options[k] = v.upper()
                if k != "state":
                    options[k] = v
        # In Azure we store transactions in cosmos and consul
        # Cosmos if the state is terminal (COMPLETED or ABORTED) and Consul if the state is not (e.g. "RUNNING")
        # So we can not filter on active non terminal states via the options passed
        transactions = api.list_transactions(self._api_ctx(), **options)

        if not transactions:
            return []
        # We filter non terminal transactions here
        if only_active:
            transactions = [t for t in transactions if t["state"] in ["CREATED", "RUNNING", "PENDING"]]
        if (isinstance(state, str) and state.upper() not in TERMINAL_STATES):
            transactions = [t for t in transactions if t["state"] in [state.upper()]]
        return self.remap_fields(transactions)

    def cancel_transaction(self, transaction_id):
        return api.cancel_transaction(self._api_ctx(), transaction_id)

    def cancel_pending_transactions(self):
        # all transactions are executed synchronously against azure
        pass

#--------------------------------------------------
# Graph
#--------------------------------------------------

def Graph(name, *, profile:str|None=None, config:Config, dry_run:bool=False):
    client = Client(Resources(profile, config), rel.Compiler(config), name, dry_run=dry_run)
    client.install("pyrel_base", dsl.build.raw_task("""
        @inline
        def make_identity(x..., z):
            exists((u) | hash128({x...}, x..., u) and
            hash_value_uint128_convert(u, z))

        @inline
        def pyrel_default({F}, c, k..., v):
            F(k..., v) or (not F(k..., _) and v = c)

        @inline
        def pyrel_unwrap(x in UInt128, y): y = x

        declare __resource
    """))
    return dsl.Graph(client, name)
