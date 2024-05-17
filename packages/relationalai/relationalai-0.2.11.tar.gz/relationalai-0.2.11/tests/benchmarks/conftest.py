import os

import pytest

from relationalai import debugging
from relationalai.debugging import logger
from relationalai.util.tracing_logger import TracingLogger
from tests.util import engine_config_fixture, root_span_fixture, snowflake_logger_fixture

@pytest.fixture(scope="function")
def engine_size():
    return "M"

@pytest.fixture(scope="function")
def engine_config(engine_size):
    yield from engine_config_fixture(engine_size)

# Create a root span that all tests will be a part of
# add `snowflake_logger` as a parameter, to make sure it is initialized before the root span
# and finishes afterwards
@pytest.fixture(scope="session", autouse=True)
def root_span(snowflake_logger):
    yield from root_span_fixture()

# Attach Snowflake logger; shutting down that the end of the session
@pytest.fixture(scope="session", autouse=True)
def snowflake_logger():
    yield from snowflake_logger_fixture()

# Wrap each test in a `benchmark` span
@pytest.fixture(scope="function", autouse=True)
def benchmark_span(request, engine_size):
    # trim 'test_' from the beginning of the test name
    name = request.node.name[5:]
    with debugging.span("benchmark", name=name, engine_size=engine_size):
        yield

if os.getenv('ENABLE_TRACING_LOGGER') is not None:
    logger.addHandler(TracingLogger())
