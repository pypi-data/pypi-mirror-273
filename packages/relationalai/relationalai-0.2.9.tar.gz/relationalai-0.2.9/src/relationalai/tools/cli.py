#pyright: reportPrivateImportUsage=false
from collections import defaultdict
import functools
import io
import re
import shlex
from typing import Sequence, cast, Any, List
from click.core import Context
from click.formatting import HelpFormatter
import requests

from relationalai.clients import azure
from relationalai.errors import RelQueryError
from relationalai.loaders.types import LoadType, UnsupportedTypeError
from relationalai.loaders.csv import CSVLoader
from relationalai.loaders.loader import Loader, rel_schema_to_type
from relationalai.util.constants import (
    DEFAULT_PROFILE_NAME,
    PARTIAL_PROFILE_NAME,
    TOP_LEVEL_PROFILE_NAME,
)
from relationalai.util.format import humanized_bytes, humanized_duration
from ..clients.types import ImportSource, ImportSourceFile, ImportSourceTable
from ..clients.client import ResourceProvider
from .. import Resources
import rich
from rich.console import Console
from rich import box as rich_box
from rich.table import Table
from ..tools import debugger as deb
from ..clients import config, snowflake
from ..clients.config import (
    FIELD_PLACEHOLDER,
    CONFIG_FILE,
    ConfigFile,
    ConfigStore,
    all_configs_including_legacy,
    get_from_snowflake_connections_toml,
    azure_default_props,
    map_toml_value,
    snowflake_default_props,
)
from InquirerPy.base.control import Choice
from InquirerPy.validator import ValidationError

import os
import sys
import click
from pathlib import Path
from .cli_controls import divider, Spinner
from . import cli_controls as controls
from datetime import datetime, timedelta

#--------------------------------------------------
# Constants
#--------------------------------------------------

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ENGINE_SIZES = ["XS", "S", "M", "L", "XL"]
PROFILE = None

SNOWFLAKE = "Snowflake"
AZURE = "Azure (Beta)"

AZURE_ENVS = {
    "Production": {
        "host": "azure.relationalai.com",
        "client_credentials_url": "https://login.relationalai.com/oauth/token"
    },
    "Early Access": {
        "host": "azure-ea.relationalai.com",
        "client_credentials_url": "https://login-ea.relationalai.com/oauth/token"
    },
    "Staging": {
        "host": "azure-staging.relationalai.com",
        "client_credentials_url": "https://login-staging.relationalai.com/oauth/token"
    },
    "Latest": {
        "host": "azure-latest.relationalai.com",
        "client_credentials_url": "https://login-latest.relationalai.com/oauth/token"
    },
}

#--------------------------------------------------
# Helpers
#--------------------------------------------------

@functools.cache
def get_config(profile:str|None = None):
    global PROFILE
    return config.Config(profile or PROFILE)

@functools.cache
def get_resource_provider(platform:str|None=None, _cfg:config.Config|None = None) -> ResourceProvider:
    cfg = _cfg or get_config()
    provider = Resources(config=cfg)
    return provider

def supports_platform(*platform_names: str):
    def decorator(cmd: click.Command):
        setattr(cmd, "__available_platforms", platform_names)
        cb = cmd.callback
        assert cb
        def checked(*args, **kwargs):
            assert cmd.name
            assert_command_available(cmd.name, command_available(cmd))
            return cb(*args, **kwargs)

        cmd.callback = checked
        return cmd
    return decorator

def command_available(cmd: click.Command) -> bool:
    available_platforms = getattr(cmd, "__available_platforms", ())
    platform = get_config().get("platform", "")
    return not available_platforms or not platform or platform in available_platforms

def assert_command_available(name: str, available: bool, plural=False):
    if not available:
        platform = get_config().get("platform", "")
        rich.print(f"[yellow]{name} {'are' if plural else 'is'} not available for {platform}")
        divider()
        sys.exit(1)

def coming_soon():
    rich.print("[yellow]This isn't quite ready yet, but it's coming soon!")
    divider()
    sys.exit(1)

def issue_top_level_profile_warning():
    rich.print("[yellow]Warning: Using a top-level profile is not recommended")
    rich.print("[yellow]Consider naming the profile by adding \\[profile.<name>] to your raiconfig.toml file\n")
    rich.print("[yellow]Example:")
    rich.print("[yellow]\\[profile.default]")
    rich.print("[yellow]platform = \"snowflake\"")
    rich.print("[yellow]account = ...")
    divider()

def ensure_config(profile:str|None=None) -> config.Config:
    cfg = get_config(profile)
    if not cfg.file_path:
        rich.print("[yellow bold]No configuration file found.")
        rich.print("To create one, run: [green bold]rai init[/green bold]")
        divider()
        sys.exit(1)
    return cfg

#--------------------------------------------------
# Validation
#--------------------------------------------------

EMPTY_STRING_REGEX = re.compile(r'^\S+$')
ENGINE_NAME_REGEX = re.compile(r'^[a-zA-Z]\w{2,}$')
ENGINE_NAME_ERROR = "Min 3 chars, start with letter, only letters, numbers, underscores allowed."

def engine_name_validator(cfg:config.Config, name:str):
    if not ENGINE_NAME_REGEX.match(name):
        raise ValidationError(message=ENGINE_NAME_ERROR)

    try:
        provider = get_resource_provider(None, cfg)
        engine = provider.get_engine(name)
        if engine and provider.is_valid_engine_state(engine['state']):
            raise ValidationError(message=f"Engine '{name}' already exists")
        return True
    except Exception as e:
        raise ValidationError(message=f"{e}")

def validate_engine_name(cfg:config.Config, name:str):
    try:
        return engine_name_validator(cfg, name)
    except ValidationError as e:
        return e.message

#--------------------------------------------------
# Custom help printer
#--------------------------------------------------

class RichGroup(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        global PROFILE
        # @NOTE: I couldn't find a sane way to access the --profile option from here, so insane it is.
        if "--profile" in sys.argv:
            ix = sys.argv.index("--profile") + 1
            if ix < len(sys.argv):
                PROFILE = sys.argv[ix]

        profile = get_config().profile
        if profile == TOP_LEVEL_PROFILE_NAME:
            profile = "[yellow bold]None[/yellow bold]" if not get_config().get("platform", "") else "[ROOT]"

        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        divider(console)
        console.print("[bold]Welcome to [green]RelationalAI![/bold]")
        console.print()
        console.print("rai [magenta]\\[options][/magenta] [cyan]command[/cyan]")

        console.print()
        console.print(f"[magenta]--profile[/magenta][dim] - which config profile to use (current: [/dim][cyan]{profile}[/cyan][dim])")

        unavailable_commands = []
        groups = defaultdict(list)
        for command in self.commands.keys():
            if ":" in command:
                group, _, _ = command.rpartition(":")
                groups[group].append(command)
            else:
                groups[""].append(command)

        console.print()
        for command in groups[""]:
            console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")

        for group, commands in groups.items():
            if not group:
                continue

            empty = True
            for command in commands:
                if command_available(self.commands[command]):
                    if empty:
                        empty = False
                        console.print()

                    console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")
                else:
                    unavailable_commands.append(command)

        if unavailable_commands:
            platform = get_config().get("platform", "")
            console.print()
            console.print(f"[yellow]Not available on {platform}[/yellow]")
            console.print()
            for command in unavailable_commands:
                console.print(f"[dim yellow]{command} - {self.commands[command].help}")

        divider(console)
        formatter.write(sio.getvalue())
        sio.close()

#--------------------------------------------------
# Custom Click Option and Argument Types
#--------------------------------------------------

ImportOption = tuple[list[str], str]

class ImportOptionsType(click.ParamType):
    def __init__(self):
        self.options = {}

    name ="import_options"
    def convert(self, raw, param, ctx) -> ImportOption:
        if ':' not in raw or '=' not in raw:
            self.fail(f"'{raw}' is not a valid import option.", param, ctx)
        raw_key, val = raw.split('=', 1)
        if len(val) == 2 and val[0] == "\\":
            val = val.encode().decode("unicode_escape")
        return (raw_key.split(":"), val)

    @classmethod
    def reduce(cls, kvs:Sequence[ImportOption]):
        options = {}
        for (key_parts, val) in kvs:
            cur = options
            for part in key_parts[:-1]:
                cur = cur.setdefault(part, {})
            cur[key_parts[-1]] = val
        return options

#--------------------------------------------------
# Main group
#--------------------------------------------------

@click.group(cls=RichGroup, context_settings=CONTEXT_SETTINGS)
@click.option("--profile", help="Which config profile to use")
def cli(profile):
    global PROFILE
    PROFILE = profile

#--------------------------------------------------
# Init
#--------------------------------------------------

@cli.command(help="Initialize a new project")
def init():
    init_flow()

#--------------------------------------------------
# Init flow
#--------------------------------------------------

def azure_flow(cfg:config.Config):
    option_selected = check_original_config_flow(cfg, "azure")
    # get the client id and secret
    client_id = controls.text("Client ID:", default=cfg.get("client_id", "") if option_selected else "")
    client_secret = controls.password("Client Secret:", default=cfg.get("client_secret", "") if option_selected else "")
    host = cfg.get("host", "")
    client_credentials_url = cfg.get("client_credentials_url", "")
    if not host or not client_credentials_url:
        env = controls.fuzzy("Select environment:", [*AZURE_ENVS.keys(), "<custom>"])
        if env == "<custom>":
            host = controls.text("Host:")
            client_credentials_url = controls.text("Client Credentials URL:")
        else:
            host = AZURE_ENVS[env]["host"]
            client_credentials_url = AZURE_ENVS[env]["client_credentials_url"]
    # setup the default config
    cfg.fill_in_with_azure_defaults(
        client_id=client_id,
        client_secret=client_secret,
        host=host if host else None,
        client_credentials_url=client_credentials_url if client_credentials_url else None
    )

def unexpand_user_path(path):
    """Inverse of os.path.expanduser"""
    home_dir = os.path.expanduser('~')
    if path.startswith(home_dir):
        return '~' + path[len(home_dir):]
    return path

def account_from_url(account_or_url:str):
    regex = r"https://app.snowflake.com/([^/]+)/([^/]+)/?.*"
    match = re.match(regex, account_or_url)
    if match:
        org = match.group(1)
        account = match.group(2)
        return f"{org}-{account}"
    elif "app.snowflake.com" in account_or_url or "https://" in account_or_url:
        raise ValueError("URL not of the form https://app.snowflake.com/[org]/[account]")
    else:
        return account_or_url

def snowflake_flow(cfg:config.Config):
    pyrel_config = check_original_config_flow(cfg, "snowflake")
    if not pyrel_config:
        check_snowflake_connections_flow(cfg)

    # get account info
    user = controls.text(
        "SnowSQL user:",
        default=cfg.get("user", ""),
        validator=EMPTY_STRING_REGEX.match,
        invalid_message="User is required"
    )
    cfg.set("user", user)

    password = controls.password(
        "SnowSQL password:",
        default=cfg.get("password", ""),
        validator=EMPTY_STRING_REGEX.match,
        invalid_message="Password is required"
    )
    cfg.set("password", password)

    rich.print("\n  Note: Account ID should look like: myorg-account123")
    rich.print("  Details: https://docs.snowflake.com/en/user-guide/admin-account-identifier\n")
    rich.print("  Alternatively, you can log in to Snowsight, copy the URL, and paste it here.")
    rich.print("  Example: https://app.snowflake.com/myorg/account123/worksheets\n")
    account_or_url = controls.text(
        "Snowflake account:",
        default=cfg.get("account", ""),
        validator=EMPTY_STRING_REGEX.match,
        invalid_message="Account is required"
    )
    account = account_from_url(account_or_url)
    if "." in account:
        rich.print("\n[yellow] Your Account ID should not contain a period (.) character.")
        corrected_account = account.replace(".", "-")
        use_replacement = controls.confirm(f"Use '{corrected_account}' instead", default=True)
        if use_replacement:
            account = corrected_account
    if account_or_url != account:
        rich.print(f"\n[dim]  Account ID: {account}")
    cfg.set("account", account)
    # setup the default config
    cfg.fill_in_with_snowflake_defaults(
        user=user,
        password=password,
        account=account,
    )

def filter_profiles_by_platform(config:ConfigFile, platform:str):
    filtered_config = {}
    for profile, props in config.get_combined_profiles().items():
        if profile == TOP_LEVEL_PROFILE_NAME:
            continue
        if props.get("platform") == platform or (
            props.get("platform") is None
            and platform == "azure"
        ):
            filtered_config[profile] = props
    return filtered_config

def check_original_config_flow(cfg:config.Config, platform:str):
    all_profiles = {}
    for config_file in all_configs_including_legacy():
        file_path = config_file.path
        plt_config = filter_profiles_by_platform(config_file, platform)
        for profile, props in plt_config.items():
            profile_id = (profile, file_path)
            all_profiles[profile_id] = props
    if platform == "snowflake":
        sf_config = get_from_snowflake_connections_toml()
        if sf_config:
            file_path = os.path.expanduser("~/.snowflake/connections.toml")
            for profile, props in sf_config.items():
                profile_id = (profile, file_path)
                all_profiles[profile_id] = props
    if len(all_profiles) == 0:
        return
    max_profile_name_len = max(len(profile) for profile, _ in all_profiles.keys())
    profile_options: List[Choice] = []
    for profile, props in all_profiles.items():
        formatted_name = f"{profile[0]:<{max_profile_name_len}}  {unexpand_user_path(profile[1])}"
        profile_options.append(Choice(value=profile, name=formatted_name))
    selected_profile = controls.select("Use existing profile", list(profile_options), None, mandatory=False)
    if not selected_profile:
        return
    cfg.profile = selected_profile[0]
    cfg.update(all_profiles[selected_profile])
    return True

def check_snowflake_connections_flow(cfg:config.Config):
    sf_config = get_from_snowflake_connections_toml()
    if not sf_config or len(sf_config) == 0:
        return
    profiles = list(sf_config.keys())
    if len(profiles) == 0:
        return
    profile = controls.fuzzy("Use profile from ~/.snowflake/connections.toml", profiles, mandatory=False)
    if not profile:
        return
    cfg.profile = profile
    cfg.update(sf_config[profile])
    return True

def role_flow(provider:ResourceProvider, cfg:config.Config):
    roles = cast(snowflake.Resources, provider).list_roles()
    result = controls.fuzzy_with_refetch(
            "Select a role:",
            "roles",
            lambda: [r["name"] for r in roles],
            default=cfg.get("role", None),
        )
    if isinstance(result, Exception):
        return
    else:
        role = result
    cfg.set("role", role or FIELD_PLACEHOLDER)
    provider.reset()

def warehouse_flow(provider:ResourceProvider, cfg:config.Config):
    result = controls.fuzzy_with_refetch(
            "Select a warehouse:",
            "warehouses",
            lambda: [w["name"] for w in cast(snowflake.Resources, provider).list_warehouses()],
            default=cfg.get("warehouse", None),
        )
    if not result or isinstance(result, Exception):
        return
    else:
        warehouse = result
    cfg.set("warehouse", warehouse or FIELD_PLACEHOLDER)

def rai_app_flow(provider:ResourceProvider, cfg:config.Config):
    result = controls.fuzzy_with_refetch(
            "Select RelationalAI app name:",
            "apps",
            lambda: [w["name"] for w in cast(snowflake.Resources, provider).list_apps()],
            default=cfg.get("rai_app_name", None),
        )
    if not result or isinstance(result, Exception):
        return
    else:
        app = result
    cfg.set("rai_app_name", app or FIELD_PLACEHOLDER)
    provider.reset()

def spcs_flow(provider: ResourceProvider, cfg: config.Config):
    role_flow(provider, cfg)
    warehouse_flow(provider, cfg)
    rai_app_flow(provider, cfg)

def engine_flow(provider:ResourceProvider, cfg:config.Config):
    if provider.config.get("platform") == "snowflake":
        app_name = cfg.get("rai_app_name", None)
        if not app_name:
            rich.print("[yellow]App name is required for engine selection. Skipping step.\n")
            raise Exception("App name is required for engine selection")
        warehouse = cfg.get("warehouse", None)
        if not warehouse:
            rich.print("[yellow]Warehouse is required for engine selection. Skipping step.\n")
            raise Exception("Warehouse is required for engine selection")
    result = controls.fuzzy_with_refetch(
        "Select an engine:",
        "engines",
        lambda: ["[CREATE A NEW ENGINE]"] + [engine.get("name") for engine in provider.list_engines()],
        default=cfg.get("engine", None),
    )
    if not result or isinstance(result, Exception):
        raise Exception("Error fetching engines")
    else:
        engine = result
    if result == "[CREATE A NEW ENGINE]":
        engine = create_engine_flow(cfg)
        rich.print("")
    cfg.set("engine", engine or FIELD_PLACEHOLDER)

def gitignore_flow():
    current_dir = Path.cwd()
    prev_dir = None
    while current_dir != prev_dir:
        gitignore_path = current_dir / '.gitignore'
        if gitignore_path.exists():
            # if there is, check to see if raiconfig.toml is in it
            with open(gitignore_path, 'r') as gitignore_file:
                if CONFIG_FILE in gitignore_file.read():
                    return
                else:
                    # if it's not, ask to add it
                    add_to_gitignore = controls.confirm(f"Add {CONFIG_FILE} to .gitignore?", default=True)
                    if add_to_gitignore:
                        with open(gitignore_path, 'a') as gitignore_file:
                            gitignore_file.write(f"\n{CONFIG_FILE}")
                    return
        prev_dir = current_dir
        current_dir = current_dir.parent

def is_valid_bare_toml_key(key):
    pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')
    return bool(pattern.match(key))

def name_profile_flow(cfg: config.Config):
    if cfg.profile != TOP_LEVEL_PROFILE_NAME:
        return
    profile = controls.text("New name for this profile:", default=DEFAULT_PROFILE_NAME)
    if not is_valid_bare_toml_key(profile):
        rich.print(
            "[yellow]Invalid profile name: should contain only alphanumeric characters, dashes, and hyphens"
        )
        return name_profile_flow(cfg)
    config_store = ConfigStore()
    if profile in config_store.get_profiles():
        overwrite = controls.confirm(f"[yellow]Overwrite existing {profile} profile?")
        if overwrite:
            return profile
        else:
            return name_profile_flow(cfg)
    return profile

def save_flow(cfg:config.Config):
    config_store = ConfigStore()
    if cfg.profile != PARTIAL_PROFILE_NAME and cfg.profile in config_store.get_profiles():
        if not controls.confirm(f"Overwrite existing {cfg.profile} profile"):
            profile_name = controls.text("Profile name:")
            if profile_name:
                cfg.profile = profile_name
            else:
                save_flow(cfg)
                return
    config_store.add_profile(cfg)
    if cfg.profile != PARTIAL_PROFILE_NAME:
        if config_store.num_profiles() == 1 or controls.confirm("Activate this profile?"):
            config_store.change_active_profile(cfg.profile)
    config_store.save()

def init_flow():
    cfg = config.Config(fetch=False)
    try:
        cfg.clone_profile()
        rich.print("\n[dim]---------------------------------------------------\n")
        rich.print("[bold]Welcome to [green]RelationalAI!\n")
        rich.print("Press Control-S to skip a prompt\n")

        if ConfigStore().get("platform"):
            issue_top_level_profile_warning()

        platform = controls.fuzzy("Host platform:", choices=[SNOWFLAKE, AZURE])
        cfg.set("platform", {
            SNOWFLAKE: "snowflake",
            AZURE: "azure"
        }[platform])

        if platform == SNOWFLAKE:
            snowflake_flow(cfg)
        elif platform == AZURE:
            azure_flow(cfg)
        elif platform:
            rich.print("[yellow]Initialization aborted!")
            rich.print(f"[yellow]Unknown platform: {platform}")
            return

        provider = get_resource_provider(None, cfg)

        rich.print()
        if platform == SNOWFLAKE:
            spcs_flow(provider, cfg)
        engine_flow(provider, cfg)
        profile = name_profile_flow(cfg)
        if profile:
            cfg.profile = profile
        save_flow(cfg)

        gitignore_flow()
        rich.print("")
        rich.print(f"[green]✓ {CONFIG_FILE} saved!")
        rich.print("\n[dim]---------------------------------------------------\n")
    except Exception as e:
        rich.print("")
        rich.print("[yellow bold]Initialization aborted!\n")
        print(e.with_traceback(None))
        rich.print("")

        save = controls.confirm("Save partial config?")
        if save:
            cfg.profile = PARTIAL_PROFILE_NAME
            rich.print("")
            cfg.fill_in_with_defaults()
            save_flow(cfg)
            gitignore_flow()
            rich.print(f"[yellow bold]✓ Saved partial {CONFIG_FILE} ({os.path.abspath(CONFIG_FILE)})")

        divider()

#--------------------------------------------------
# Profile switcher
#--------------------------------------------------

@cli.command(
    name="profile:switch",
    help="Switch to a different profile",
)
@click.option("--profile", help="Profile to switch to")
def profile_switch(profile:str|None=None):
    config_store = ConfigStore()
    profiles = list(config_store.get_profiles().keys())
    divider()
    if not profile:
        if len(profiles) == 0:
            rich.print("[yellow]No profiles found")
            divider()
            sys.exit(1)
        profile = controls.fuzzy("Select a profile:", profiles)
        divider()
    else:
        if profile not in profiles:
            rich.print(f"[yellow]Profile '{profile}' not found")
            divider()
            sys.exit(1)
    config_store.change_active_profile(profile)
    config_store.save()
    rich.print(f"[green]✓ Switched to profile '{profile}'")
    divider()

#--------------------------------------------------
# Explain config
#--------------------------------------------------

@cli.command(
    name="config:explain",
    help="Inspect config status",
)
@click.option(
    "--profile",
    help="Profile to inspect",
)
@click.option(
    "--all-profiles",
    help="Whether to show all profiles in config file",
    is_flag=True,
)
def config_explain(profile:str|None=None, all_profiles:bool=False):
    divider()
    cfg = ensure_config(profile)
    config_store = ConfigStore()

    if config_store.get("platform"):
        issue_top_level_profile_warning()

    rich.print(f"[bold green]{cfg.file_path}")
    if os.getenv("RAI_PROFILE"):
        rich.print(f"[yellow]Environment variable [bold]RAI_PROFILE = {os.getenv('RAI_PROFILE')}[/bold]")
    rich.print("")
    if cfg.profile != TOP_LEVEL_PROFILE_NAME:
        rich.print(f"[bold]\\[{cfg.profile}]")

    for key, value in cfg.items_with_dots():
        if key == "active_profile" and cfg.profile != TOP_LEVEL_PROFILE_NAME:
            continue
        rich.print(f"{key} = [cyan bold]{map_toml_value(mask(key, value))}")

    platform = cfg.get("platform", "snowflake")
    defaults = snowflake_default_props if platform == "snowflake" else azure_default_props

    for key, value in defaults.items():
        if key not in cfg:
            rich.print(f"[yellow bold]{key}[/yellow bold] = ?" + (
                f" (default: {value})" if value and value != FIELD_PLACEHOLDER else ""
            ))

    if all_profiles:
        for profile, props in config_store.get_profiles().items():
            if profile == cfg.profile:
                continue
            if len(props):
                rich.print()
                rich.print(f"[bold]\\[{profile}][/bold]")
                for key, value in props.items():
                    rich.print(f"{key} = [cyan bold]{map_toml_value(mask(key, value))}")

    divider()

def mask(key: str, value: Any):
    if key in ["client_secret", "password"]:
        return "*" * len(str(value))
    return value

#--------------------------------------------------
# Check config
#--------------------------------------------------

@cli.command(
    name="config:check",
    help="Check whether config is valid",
)
def config_check(all_profiles:bool=False):
    divider()
    if ConfigStore().get("platform"):
        issue_top_level_profile_warning()
    ensure_config()
    with Spinner("Connecting to platform...", "Connection successful!", "Error:"):
        get_resource_provider().list_engines()
    divider()

#--------------------------------------------------
# Version
#--------------------------------------------------

def latest_version(package_name):
    """Get the current version of a package on PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        version = data['info']['version']
        return version
    else:
        return None

@cli.command(help="Print version info")
def version():
    from .. import __version__
    from railib import __version__ as railib_version

    table = Table(show_header=False, border_style="dim", header_style="bold", box=rich_box.SIMPLE)
    def print_version(name, version, latest=None):
        if latest is not None and version != latest:
            table.add_row(f"[bold]{name}[red]", f"[red bold]{version} → {latest}")
        else:
            table.add_row(f"[bold]{name}", f"[green]{version}")

    divider()
    print_version("RelationalAI", __version__, latest_version("relationalai"))
    print_version("Rai-sdk", railib_version, latest_version("rai-sdk"))
    print_version("Python", sys.version.split()[0])

    try:
        cfg = get_config()
        if not cfg.file_path:
            table.add_row("[bold]App", "No configuration file found. To create one, run: [green]rai init")
        else:
            platform = cfg.get("platform", None)
            if platform == "snowflake":
                # print()
                with Spinner("Checking app version"):
                    try:
                        app_version = get_resource_provider().get_version()
                    except Exception as e:
                        rich.print(f"\n\n[yellow]Error fetching app version: {e}")
                        exit(1)
                print_version("App", app_version)

    except Exception as e:
        rich.print(f"[yellow]Error checking app version: {e}")
        divider()
        exit(1)

    rich.print(table)
    divider()

#--------------------------------------------------
# Debugger
#--------------------------------------------------

@cli.command(help="Open the RAI debugger")
@click.option("--host", help="Host to use", default="0.0.0.0")
@click.option("--port", help="Port to use", default=8080)
@click.option("--new", help="Use the new debugger", is_flag=True, default=False)
def debugger(host, port, new):
    if new:
        from relationalai.tools import debugger_server
        debugger_server.start_server(host, port)
    else:
        deb.main(host, port)

#--------------------------------------------------
# Engine list
#--------------------------------------------------

@cli.command(name="engines:list", help="List all engines")
@click.option("--state", help="Filter by engine state")
def engines_list(state:str|None=None):
    divider(flush=True)
    ensure_config()
    with Spinner("Fetching engines"):
        try:
            engines = get_resource_provider().list_engines(state)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching engines: {e}")
            exit(1)

    if len(engines):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Name")
        table.add_column("Size")
        table.add_column("State")
        for engine in engines:
            table.add_row(engine.get("name"), engine.get("size"), engine.get("state"))
        rich.print(table)
    else:
        rich.print("[yellow]No engines found")

    divider()

@cli.command(name="engines:get", help="Get engine details")
@click.option("--name", help="Name of the engine")
def engines_get(name):
    divider(flush=True)
    ensure_config()

    if not name:
        name = controls.text("Engine name:", validator=ENGINE_NAME_REGEX.match, invalid_message=ENGINE_NAME_ERROR)
        rich.print("")

    with Spinner("Fetching engine"):
        try:
            engine = get_resource_provider().get_engine(name)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching engine: {e}")
            divider(flush=True)
            exit(1)

    if engine:
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Name")
        table.add_column("Size")
        table.add_column("State")
        table.add_row(engine.get("name"), engine.get("size"), engine.get("state"))
        rich.print(table)
    else:
        rich.print("[yellow]Engine not found")

    divider()

#--------------------------------------------------
# Engine create
#--------------------------------------------------

def create_engine_flow(cfg:config.Config, name=None, size=None, pool=None):
    provider = get_resource_provider(None, cfg)
    is_snowflake = provider.config.get("platform") == "snowflake"
    is_interactive = name is None or size is None or (is_snowflake and pool is None)

    if not name:
        name = controls.prompt(
            "Engine name:",
            name,
            validator=ENGINE_NAME_REGEX.match,
            invalid_message=ENGINE_NAME_ERROR,
            newline=True
        )

    if is_interactive:
        with Spinner(f"Validating engine '{name}' name", "Engine name validated", "Error:"):
            is_name_valid = validate_engine_name(cfg, name)
        if isinstance(is_name_valid, str):
            rich.print("")
            rich.print(f"[yellow]{is_name_valid}")
            rich.print("")
            return create_engine_flow(cfg)
    else:
        is_name_valid = validate_engine_name(cfg, name)
        if isinstance(is_name_valid, str):
            rich.print(f"[yellow]{is_name_valid}")
            return None

    rich.print()
    if not size:
        size = controls.fuzzy("Engine size:", choices=ENGINE_SIZES)
        rich.print("")

    if is_snowflake:
        provider = cast(snowflake.Resources, provider)
        if not pool:
            result = controls.fuzzy_with_refetch(
                "Compute pool:",
                "compute pools",
                provider.list_valid_compute_pools_by_engine_size,
                size,
            )
            if isinstance(result, Exception):
                return None
            else:
                pool = result
        if is_interactive and not pool:
            rich.print("[yellow]No compute pool selected\n")
            redo = controls.confirm("Would you like to choose a different engine size?", default=True)
            rich.print("")
            if redo:
                return create_engine_flow(cfg, name)
            else:
                return None
    else:
        pool = ""

    create_exception = None

    with Spinner(
        f"Creating '{name}' engine... (this may take several minutes)",
        f"Engine '{name}' created!",
        failed_message="Error:"
    ):
        try:
            provider.create_engine(name, size, pool)
        except Exception as e:
            create_exception = e
            # We do not want to print the success context message if the engine creation fails
            # Since we are raising here and passing a "fail_message", the spinner will print the actual error message
            raise e
    if isinstance(create_exception, Exception):
        if is_interactive and "does not exist" in f"{create_exception}".lower():
            rich.print("")
            redo = controls.confirm("Would you like to choose a different compute pool?", default=True)
            rich.print("")
            if redo:
                return create_engine_flow(cfg, name, size)
    return name

@cli.command(name="engines:create", help="Create a new engine")
@click.option("--name", help="Name of the engine")
@click.option("--size", type=click.Choice(ENGINE_SIZES, case_sensitive=False), help="Size of the engine")
@click.option("--pool", help="Compute pool name. Note: Snowflake platform only.")
def engines_create(name, size, pool):
    divider(flush=True)
    cfg = ensure_config()
    create_engine_flow(cfg, name, size, pool)
    divider()

#--------------------------------------------------
# Engine delete
#--------------------------------------------------

@cli.command(name="engines:delete", help="Delete an engine")
@click.option("--name", help="Name of the engine")
def engines_delete(name):
    divider(flush=True)
    ensure_config()
    provider = get_resource_provider()
    if not name:
        name = controls.fuzzy_with_refetch(
            "Select an engine:",
            "engines",
            lambda: [engine["name"] for engine in provider.list_engines()],
        )
        if not name or isinstance(name, Exception):
            return
    else:
        try:
            engine = provider.get_engine(name)
            if not engine:
                rich.print(f"[yellow]Engine '{name}' not found")
                divider()
                return
        except Exception as e:
            rich.print(f"[yellow]Error fetching engine: {e}")
            divider()
            return

    with Spinner(f"Deleting '{name}' engine", f"Engine '{name}' deleted!"):
        try:
            provider.delete_engine(name)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error deleting engine: {e}")
    divider()

#--------------------------------------------------
# Import Source flows
#--------------------------------------------------

def import_source_flow(provider: ResourceProvider) -> Sequence[ImportSource]:
    match provider:
        case snowflake.Resources():
            return snowflake_import_source_flow(provider)
        case azure.Resources():
            return azure_import_source_flow(provider)
        case _:
            raise Exception(f"No import source flow available for {type(provider).__module__}.{type(provider).__name__}")

def snowflake_import_source_flow(provider: snowflake.Resources) -> Sequence[ImportSource]:
    with Spinner("Fetching databases", "Databases fetched"):
        try:
            dbs = provider.list_databases()
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching databases: {e}")
            dbs = []
    if len(dbs) == 0:
        rich.print("[yellow]No databases found")
        exit(1)
    rich.print()
    db = controls.fuzzy("Select a database:", [db["name"] for db in dbs])
    rich.print()

    with Spinner("Fetching schemas", "Schemas fetched"):
        try:
            schemas = provider.list_sf_schemas(db)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching schemas: {e}")
            schemas = []
    if len(schemas) == 0:
        rich.print("[yellow]No schemas found")
        exit(1)
    rich.print()
    schema = controls.fuzzy("Select a schema:", [s["name"] for s in schemas])
    rich.print()

    with Spinner("Fetching tables", "Tables fetched"):
        try:
            tables = provider.list_tables(db, schema)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching tables: {e}")
            tables = []
    if len(tables) == 0:
        rich.print("[yellow]No tables found")
        exit(1)
    rich.print()
    if tables:
        tables = controls.fuzzy("Select tables (tab for multiple):", [t["name"] for t in tables], multiselect=True)
    else:
        rich.print("[yellow]No tables found")
        tables = ""
    rich.print()
    if isinstance(tables, list):
        return [ImportSourceTable(db, schema, table) for table in tables]
    else:
        return [ImportSourceTable(db, schema, tables)]

def azure_import_source_flow(provider: azure.Resources) -> Sequence[ImportSource]:
    result = controls.file("Select a file:", allow_freeform=True)
    return [ImportSourceFile(result)] if result else []

def import_source_options_flow(provider: ResourceProvider, source: ImportSource, default_options:dict) -> dict:
    match source:
        case ImportSourceFile():
            type: LoadType = default_options.get("type", None)
            if type is None or type == "auto":
                type = Loader.get_type_for(source)
            match type:
                case "csv":
                    return import_source_csv_options_flow(provider, source, default_options)
                case _:
                    pass
        case _:
            pass

    return default_options

def import_source_csv_options_flow(provider: ResourceProvider, source: ImportSourceFile, default_options:dict) -> dict:
    user_specified_schema = {k.strip(): rel_schema_to_type(v.lower()) for k, v in default_options.get("schema", {}).items()}
    user_specified_syntax = default_options.get("syntax", {})

    if source.is_url():
        # @FIXME: Should maybe prompt user to provide a schema manually for urls?
        return {**default_options, "schema": user_specified_schema}

    # Syntax inference + confirmation for local files ==========================

    syntax = CSVLoader.guess_syntax(source.raw_path)
    syntax.update(user_specified_syntax)

    syntax_table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
    for k in syntax.keys():
        syntax_table.add_column(k)
    syntax_table.add_row(*[
        repr(v)[1:-1] if isinstance(v, str) else
        "[dim]<default>[/dim]" if v is None else
        str(v)
        for v in syntax.values()])

    rich.print(syntax_table)

    if not controls.confirm(f"Use this dialect for {source.name}:", True):
        fail_import_options_flow(
            source,
            "You can manually specify the CSV dialectusing syntax arguments. For example, to set the [cyan]delimiter[/cyan] to [green]tab[/green], run:",
            'syntax:[cyan]delim[/cyan]="[green]\\t[/green]"'
        )

    # Schema inference + confirmation for local files ==========================

    schema, csv_chunk = CSVLoader.guess_schema(source.raw_path, syntax)
    schema.update(user_specified_schema)

    schema_table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
    schema_table.add_column("Field")
    schema_table.add_column("Type")
    schema_table.add_column("Ex.")
    for field, type in schema.items():
        schema_table.add_row(field, type.name, f"[dim]{csv_chunk[field][0]}")

    rich.print(schema_table)

    if not controls.confirm(f"Use this schema for {source.name}:", True):
        field = next(iter(schema.keys()))
        fail_import_options_flow(
            source,
            f"You can manually specify column types using schema arguments. For example, to load the column [cyan]{field}[/cyan] as a [green]string[/green], run:",
            f"schema:[cyan]{field}[/cyan]=[green]string[/green]"
        )

    return {**default_options, "schema": schema, "syntax": syntax}

def fail_import_options_flow(source: ImportSourceFile, message: str, solution_args: str):
    prev_cmd_args = " ".join(shlex.quote(arg) for arg in sys.argv[1:])
    saved_args = []
    if "--source" not in sys.argv:
        saved_args.append(f"--source {shlex.quote(source.raw_path)}")
    if "--name" not in sys.argv:
        saved_args.append(f"--name {shlex.quote(source.name)}")

    saved_args = " " + " ".join(saved_args) if saved_args else ""
    print()
    rich.print(message)
    print()
    rich.get_console().print(f"[dim]    rai {prev_cmd_args}{saved_args}[/dim] {solution_args}", highlight=False)
    divider()
    sys.exit(0)


def parse_source(provider: ResourceProvider, raw: str) -> Sequence[ImportSource]:
    if provider.platform == "azure":
        return [ImportSourceFile(raw)]
    elif provider.platform == "snowflake":
        parts = raw.split(".")
        assert len(parts) == 3, "Snowflake table imports must be in `database.schema.table` format"
        return [ImportSourceTable(*parts)]
    else:
        raise Exception(f"Unsupported platform: {provider.platform}")

#--------------------------------------------------
# Imports list
#--------------------------------------------------

@cli.command(name="imports:list", help="List objects imported into RAI")
@click.option("--model", help="Model")
def imports_list(model):
    divider(flush=True)
    ensure_config()
    provider = get_resource_provider()

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        try:
            imports = provider.list_imports(model)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching imports: {e}")
            imports = []

    rich.print()
    if len(imports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        cols = {"Import": "name"}
        if len(imports) and "type" in imports[0]:
            cols["Type"] = "type"
        if len(imports) and "id" in imports[0]:
            cols["ID"] = "id"
        if len(imports) and "status" in imports[0]:
            cols["Status"] = "status"

        for label in cols.keys():
            table.add_column(label)

        for imp in imports:
            table.add_row(*[imp.get(attr, None) for attr in cols.values()])
        rich.print(table)
    else:
        rich.print("[yellow]No imports found")

    divider()

#--------------------------------------------------
# Imports stream
#--------------------------------------------------

@supports_platform("snowflake")
@cli.command(name="imports:stream", help="Stream an object into RAI")
@click.option("--source", help="Source")
@click.option("--model", help="Model")
@click.option("--rate", help="Rate")
@click.argument('options', nargs=-1, type=ImportOptionsType())
def imports_stream(source, model, rate, options):
    divider(flush=True)
    ensure_config()
    provider = get_resource_provider()
    default_options = ImportOptionsType.reduce(options)

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    sources = parse_source(provider, source) if source else import_source_flow(provider)
    for import_source in sources:
        try:
            options = import_source_options_flow(provider, import_source, default_options)
            with Spinner(f"Creating stream for {import_source.name}", f"Stream for {import_source.name} created"):
                provider.create_import_stream(import_source, model, rate, options=options)
        except UnsupportedTypeError as err:
            rich.print(f"\n\n[yellow]The [bold]{provider.platform}[/bold] integration doesn't support streaming from [bold]'{err.type}'[/bold] sources.")
        except Exception as e:
            rich.print(f"\n[yellow]Error creating stream: {e}")

    divider()

#--------------------------------------------------
# Imports snapshot
#--------------------------------------------------

@supports_platform("azure")
@cli.command(name="imports:snapshot", help="Load an object once into RAI")
@click.option("--source", help="Source")
@click.option("--model", help="Model")
@click.option("--name", help="Import name")
@click.option("--type", help="Import as type", default="auto", type=click.Choice(["auto", *Loader.type_to_loader.keys()]))
@click.argument('options', nargs=-1, type=ImportOptionsType())
def imports_snapshot(source:str|None, model:str|None, name:str|None, type:str|None, options):
    divider(flush=True)
    ensure_config()
    provider = get_resource_provider()
    default_options = ImportOptionsType.reduce(options)
    default_options["type"] = type

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    sources = parse_source(provider, source) if source else import_source_flow(provider)
    for import_source in sources:
        try:
            import_source.name = name if name else controls.text("name:", import_source.name)
            options = import_source_options_flow(provider, import_source, default_options)
            with Spinner(f"Creating snapshot for {import_source.name}", f"Snapshot for {import_source.name} created"):
                provider.create_import_snapshot(import_source, model, options=options)
        except UnsupportedTypeError as err:
            rich.print(f"\n\n[yellow]The [bold]{provider.platform}[/bold] integration doesn't support loading [bold]'{err.type}'[/bold] files.")
        except RelQueryError as e:
            rich.print(f"\n\n[yellow]Error creating snapshot: {e.pprint()}")
        except Exception as e:
            rich.print(f"\n\n[yellow]Error creating snapshot: {e}")


    divider()

#--------------------------------------------------
# Imports delete
#--------------------------------------------------

@cli.command(name="imports:delete", help="Delete an import from RAI")
@click.option("--object", help="Object")
@click.option("--model", help="Model")
def imports_delete(object, model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        try:
            imports = provider.list_imports(model)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching imports: {e}")
            exit(1)

    if not imports:
        rich.print()
        rich.print("[yellow]No imports to delete")
    if object:
        objects = [object]
    else:
        if len(imports) == 0:
            rich.print("[yellow]No imports found")
            exit(1)
        rich.print()
        objects = controls.fuzzy("Select objects (tab for multiple):", [t["name"] for t in imports], multiselect=True)
        rich.print()

    for object in objects:
        with Spinner(f"Removing {object}", f"{object} removed"):
            try:
                provider.delete_import(object, model)
            except Exception as e:
                rich.print(f"\n\n[yellow]Error deleting import: {e}")

    divider()

#--------------------------------------------------
# Exports list
#--------------------------------------------------

@supports_platform("snowflake")
@cli.command(name="exports:list", help="List objects exported out of RAI")
@click.option("--model", help="Model")
def exports_list(model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching exports for {model}", "Exports fetched"):
        try:
            exports = provider.list_exports(model, "")
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching exports: {e}")
            exit(1)

    rich.print()
    if len(exports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Object")
        for imp in exports:
            table.add_row(imp.get("name"))
        rich.print(table)
    else:
        rich.print("[yellow]No exports found")

    divider()

#--------------------------------------------------
# Exports delete
#--------------------------------------------------

@supports_platform("snowflake")
@cli.command(name="exports:delete", help="Delete an export from RAI")
@click.option("--export", help="export")
@click.option("--model", help="Model")
def exports_delete(export, model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            try:
                models = [model["name"] for model in provider.list_graphs()]
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching models: {e}")
                exit(1)
        if len(models) == 0:
            rich.print("[yellow]No models found")
            exit(1)
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    # @FIXME It seems like we should just fuzzy list exports but this was the original behavior
    source_names = [export] if export else [source.name for source in import_source_flow(provider)]
    for source_name in source_names:
        with Spinner(f"Removing {source_name}", f"{source_name} removed"):
            try:
                provider.delete_export(model, "", source_name)
            except Exception as e:
                rich.print(f"\n\n[yellow]Error deleting export: {e}")

    divider()

#--------------------------------------------------
# Transactions get
#--------------------------------------------------

def get_color_by_transaction_state(state:str) -> str:
    match state.lower():
        case "aborted":
            return "red"
        case "completed":
            return "white"
        case "created" | "running" | "cancelling":
            return "bold yellow"
        case _:
            return ""

def show_transaction_table(dict):
    table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
    table.add_column("Field")
    table.add_column("Value")
    for key, value in dict.items():
        style = get_color_by_transaction_state(value) if key == "state" else ""

        if key == "query_size" and isinstance(value, int):
            value = humanized_bytes(value)

        match value:
            case None:
                val = "N/A"
            case int():
                val = f"{value}"
            case float():
                val = f"{value}"
            case list():
                val = ", ".join(value)
            case bool():
                val = f"{value}"
            case datetime():
                val = value.strftime("%Y-%m-%d %H:%M:%S")
            case timedelta():
                val = humanized_duration(value.total_seconds() * 1000)
            case _:
                val = value
        table.add_row(key, val, style=style)
    rich.print(table)

@cli.command(name="transactions:get", help="Get transaction details")
@click.option("--id", help="Transaction id")
def transactions_get(id):
    divider()
    ensure_config()
    provider = get_resource_provider()
    transaction = None

    if not id:
        id = controls.text("Transaction id:")
        rich.print("")

    with Spinner("Fetching transaction", "Transaction fetched"):
        try:
            transaction = provider.get_transaction(id)
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching transaction: {e}")
            divider()
            exit(1)

    rich.print()

    if transaction:
        show_transaction_table(transaction)

    divider()

#--------------------------------------------------
# Transactions list
#--------------------------------------------------

def show_transactions(transactions, limit, all_users):
    config = ensure_config()
    provider = get_resource_provider()
    platform = provider.config.get("platform", "snowflake")
    if len(transactions):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("ID")
        table.add_column("Schema")
        table.add_column("State")
        table.add_column("Created")
        table.add_column("Duration", justify="right")

        added = 0
        for txn in transactions:
            if platform == "snowflake":
                if (
                    not all_users
                    and txn.get("created_by", "").lower()
                    != cast(str, config.get("user", "")).lower()
                ):
                    continue
            if added >= limit:
                break

            state = txn.get("state", "")
            duration = txn.get("duration")
            created_on = txn.get("created_on")

            if isinstance(created_on, int):
                created_on = datetime.fromtimestamp(created_on / 1000)
            if duration is None:
                duration = (datetime.now(created_on.tzinfo) - created_on).total_seconds() * 1000

            table.add_row(
                txn.get("id"),
                txn.get("database"),
                state,
                created_on.strftime("%Y-%m-%d %H:%M:%S"),
                humanized_duration(duration),
                style=get_color_by_transaction_state(state)
            )
            added += 1
        rich.print(table)
    else:
        rich.print("[yellow]No transactions found")

@cli.command(name="transactions:list", help="List transactions")
@click.option("--id", help="Filter by transaction id", type=str)
@click.option("--state", help="Filter by transaction state", type=str)
@click.option("--limit", default=20, help="Limit")
@click.option("--all-users", is_flag=True, default=False, help="Show transactions from all users")
def transactions_list(id, state, limit, all_users):
    divider()
    ensure_config()
    provider = get_resource_provider()
    with Spinner("Fetching transactions", "Transactions fetched"):
        try:
            transactions = provider.list_transactions(
                id=id,
                state=state,
                limit=max(limit, 100)
            )
        except Exception as e:
            rich.print(f"\n\n[yellow]Error fetching transactions: {e}\n")
            exit(1)

    rich.print()
    show_transactions(transactions, limit, all_users)

    divider()

#--------------------------------------------------
# Transaction cancel
#--------------------------------------------------

@cli.command(name="transactions:cancel", help="Cancel a transaction")
@click.option("--id", help="Transaction ID")
@click.option("--all-users", is_flag=True, help="Show transactions from all users")
def transactions_cancel(id, all_users):
    divider()
    ensure_config()
    provider = get_resource_provider()
    if id is None:
        with Spinner("Fetching transactions", "Transactions fetched"):
            try:
                transactions = provider.list_transactions(limit=20, only_active=True)
            except Exception as e:
                rich.print(f"\n\n[yellow]Error fetching transactions: {e}")
                exit(0)

        if not transactions:
            rich.print("\n[yellow]No active transactions found")
            rich.print("")
            exit(1)

        show_transactions(transactions, 20, all_users)

        id = controls.fuzzy("Select a transaction to cancel:", [t["id"] for t in transactions])
        print()

    with Spinner("Cancelling transaction", "Transaction cancelled", "Error:"):
        provider.cancel_transaction(id)

    divider()

#--------------------------------------------------
# Main
#--------------------------------------------------

if __name__ == "__main__":
    # app = EventApp()
    # app.run()
    cli()
