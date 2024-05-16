import typer
from inferless_cli.utils.helpers import read_yaml, create_yaml
import rich


class Convertors:
    @staticmethod
    def get_cuda_version(cuda_version: str) -> str:
        cuda_version = float(cuda_version)
        if cuda_version >= 11.0 and cuda_version < 12.0:
            return "11.8.0"
        elif cuda_version >= 12.0:
            return "12.1.1"

    @staticmethod
    def convert_cog_to_runtime_yaml(
        source_file: str, destination_file: str, return_as_json: bool = False
    ):
        cog_yaml = read_yaml(source_file)

        filtered_data = {"build": {}}
        if cog_yaml is not None:
            for key, value in cog_yaml.get("build", {}).items():
                if key in ["cuda", "python_packages", "system_packages"]:
                    if key == "cuda":
                        filtered_data["build"]["cuda_version"] = (
                            Convertors.get_cuda_version(value)
                        )
                    else:
                        filtered_data["build"][key] = value
        else:
            rich.print("[bold red]Error:[/bold red] cog.yaml not found.")
            raise typer.Exit(1)
        if return_as_json:
            return filtered_data

        create_yaml(filtered_data, destination_file)
