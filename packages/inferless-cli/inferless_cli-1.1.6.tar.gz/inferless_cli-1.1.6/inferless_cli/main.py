import rich
import typer
from inferless_cli.prompts import run

from typing import Optional, List
from inferless_cli.utils.constants import (
    DEFAULT_YAML_FILE_NAME,
    DEFAULT_RUNTIME_FILE_NAME,
    PROVIDER_CHOICES,
)
from .utils.services import (
    callback_with_auth_validation,
    min_version_required,
)
from .utils.helpers import (
    check_import_source,
    sentry_init,
    set_env_mode,
    version_callback,
)
from .prompts import (
    init,
    login,
    workspace,
    token,
    deploy,
    log,
    model,
    secret,
    volume,
    runtime,
    export,
)
from prompt_toolkit import prompt
import sys

sys.tracebacklimit = 0

sentry_init()


app = typer.Typer(
    name="Inferless CLI",
    add_completion=False,
    rich_markup_mode="markdown",
    no_args_is_help=True,
    pretty_exceptions_enable=True,
    help="""
    Inferless - Deploy Machine Learning Models in Minutes.

    See the website at https://inferless.com/ for documentation and more information
    about running code on Inferless.
    """,
    callback=sentry_init,
)


@app.callback()
def inferless(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback),
):
    """
    This function is currently empty because it is intended to be used as a callback for the `inferless` command.
    The `inferless` command is not yet implemented, but this function is included here as a placeholder for future development.
    """
    pass


@app.command("mode", help="Change mode", hidden=True)
def run_mode(
    mode: str = typer.Argument(
        ..., help="The mode to run the application in, either 'DEV' or 'PROD'."
    )
):
    """
    Runs the application in the specified mode.
    """
    mode = mode.upper()  # Ensure mode is uppercase
    if mode not in ["DEV", "PROD"]:
        rich.print("[red]Error: Mode must be 'DEV' or 'PROD'[/red]")
        raise typer.Exit(code=1)

    if mode == "DEV":
        set_env_mode(mode)
        rich.print("[green]Running in development mode[/green]")
        # Insert your development mode code here
    else:
        set_env_mode(mode)
        rich.print("[green]Running in production mode[/green]")
        # Insert your production mode code here


app.add_typer(
    token.app,
    name="token",
    help="Manage Inferless tokens",
    callback=min_version_required,
)
app.add_typer(
    workspace.app,
    name="workspace",
    help="Manage Inferless workspaces (can be used to switch between workspaces)",
    callback=callback_with_auth_validation,
)
app.add_typer(
    model.app,
    name="model",
    help="Manage Inferless models (list , delete , activate , deactivate , rebuild the models)",
    callback=callback_with_auth_validation,
)
app.add_typer(
    secret.app,
    name="secret",
    help="Manage Inferless secrets (list secrets)",
    callback=callback_with_auth_validation,
)

app.add_typer(
    volume.app,
    name="volume",
    help="Manage Inferless volumes (can be used to list volumes and create new volumes)",
    callback=callback_with_auth_validation,
)

app.add_typer(
    runtime.app,
    name="runtime",
    help="Manage Inferless runtimes (can be used to list runtimes and upload new runtimes)",
    callback=callback_with_auth_validation,
)


@app.command(
    "export",
    help="Export the runtime configuration of another provider to Inferless runtime config",
)
def export_def(
    source_file: Optional[str] = typer.Option(
        "cog.yaml",
        "--runtime",
        "-r",
        help="The runtime configuration file of another provider",
    ),
    destination_file: Optional[str] = typer.Option(
        DEFAULT_RUNTIME_FILE_NAME,
        "--destination",
        "-d",
        help="The destination file for the Inferless runtime configuration",
    ),
    from_provider: Optional[str] = typer.Option(
        "replicate",
        "--from",
        "-f",
        help="The provider from which to export the runtime configuration",
    ),
):
    callback_with_auth_validation()
    export.export_runtime_configuration(source_file, destination_file, from_provider)


@app.command("log", help="Inferless models logs (view build logs or call logs)")
def log_def(
    model_id: str = typer.Argument(None, help="Model id or model import id"),
    import_logs: bool = typer.Option(False, "--import-logs", "-i", help="Import logs"),
    logs_type: str = typer.Option(
        "BUILD", "--type", "-t", help="Logs type [BUILD, CALL]]"
    ),
):
    callback_with_auth_validation()
    log.log_prompt(model_id, logs_type, import_logs)


@app.command("init", help="Initialize a new Inferless model")
def init_def():
    callback_with_auth_validation()
    init.init_prompt()


@app.command("deploy", help="Deploy a model to Inferless")
def deploy_def():
    callback_with_auth_validation()
    config_file_name = prompt(
        "Enter the name of your config file: ", default=DEFAULT_YAML_FILE_NAME
    )
    if check_import_source(config_file_name) == "GIT":
        deploy.deploy_git(config_file_name)
    elif check_import_source(config_file_name) == "LOCAL":
        deploy.deploy_local(config_file_name, False)
    else:
        rich.print(
            "[red] config file not found [/red] please run [blue] inferless init [/blue] "
        )
        raise typer.Exit(1)


@app.command("run", help="Run a model locally")
def run_local_def(
    runtime: str = typer.Option(
        None,
        "--runtime",
        "-r",
        help="custom runtime config file path to override from inferless-runtime-config.yaml",
    ),
    runtime_type: str = typer.Option(
        None,
        "--type",
        "-t",
        help="Type of runtime to run [inferless, replicate]",
    ),
    name: str = typer.Option(
        "inferless-model",
        "--name",
        "-n",
        help="Name of the model to deploy on inferless",
    ),
    env_file: Optional[str] = typer.Option(
        None,
        "--env-file",
        "-f",
        help="Path to an env file containing environment variables (one per line in KEY=VALUE format)",
    ),
    env_vars: List[str] = typer.Option(
        [],
        "--env",
        "-e",
        help="Environment variables to set for the runtime (e.g. 'KEY=VALUE'). If the env variable contains special chars please escape them.",
    ),
):
    callback_with_auth_validation()
    if runtime_type is not None and runtime_type not in PROVIDER_CHOICES:
        rich.print(
            f"Error: '--type' must be one of {PROVIDER_CHOICES}, got '{runtime_type}' instead."
        )
        raise typer.Exit(code=1)

    if runtime_type is None and runtime is not None:
        rich.print(
            "[yellow]Type not given. Assuming type as Inferless.[/yellow]"
        )
        runtime_type = "inferless"

    env_dict = {}
    if env_file:
        with open(env_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                env_dict[key] = value

    for env_var in env_vars:
        key, value = env_var.split("=", 1)
        env_dict[key] = value

    run.local_run(runtime, runtime_type, name, env_dict)


@app.command("login", help="Login to Inferless")
def login_def():
    min_version_required()
    login.login_prompt()


if __name__ == "__main__":
    app()
