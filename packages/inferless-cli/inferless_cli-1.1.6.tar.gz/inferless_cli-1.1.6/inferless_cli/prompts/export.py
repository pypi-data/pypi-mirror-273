import rich
import os
import typer
from typing import Optional
from prompt_toolkit import prompt
from inferless_cli.utils.convertors import Convertors
from inferless_cli.utils.constants import PROVIDER_EXPORT_CHOICES, DEFAULT_RUNTIME_FILE_NAME


def export_runtime_configuration(
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
    if not os.path.exists(source_file):
        rich.print(f"[bold red]Error:[/bold red] File '{source_file}' does not exist.")
        raise typer.Exit(code=1)

    if destination_file == DEFAULT_RUNTIME_FILE_NAME and os.path.exists(
        destination_file
    ):
        rich.print(
            f"[yellow]Warning:[/yellow] File '{destination_file}' already exists. It will be overwritten."
        )
        answer = prompt("Do you want to continue? (y/n) ", default="n")
        if answer != "y":
            raise typer.Exit(code=0)

    if from_provider not in PROVIDER_EXPORT_CHOICES:
        rich.print(
            f"Error: '--from' must be one of {PROVIDER_EXPORT_CHOICES}, got '{from_provider}' instead."
        )
        raise typer.Exit(code=1)

    Convertors.convert_cog_to_runtime_yaml(source_file, destination_file)

    rich.print(
        f"[green]Success:[/green] Runtime configuration exported to '{destination_file}'"
    )
