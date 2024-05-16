import base64
import time
import copy
import json
import os
import subprocess
import requests
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from inferless_cli.utils.constants import (
    DEFAULT_RUNTIME_FILE_NAME,
    DEFAULT_YAML_FILE_NAME,
)
from inferless_cli.utils.helpers import (
    build_docker_image,
    create_config_from_json,
    create_input_from_schema,
    decrypt_tokens,
    delete_files,
    generate_template_model,
    get_inputs_from_input_json,
    is_docker_running,
    is_inferless_yaml_present,
    log_exception,
    read_json,
    read_yaml,
    start_docker_container,
    stop_containers_using_port_8000,
    yaml,
)
from inferless_cli.utils.services import (
    create_presigned_download_url,
    get_cli_files,
    get_file_download,
    get_templates_list,
    get_volume_info_with_id,
)
from inferless_cli.utils.convertors import Convertors

MODEL_DIR_STRING = "##model_dir_path##"


def local_run(runtime: str, runtime_type: str, name: str, env_dict: dict):
    if not is_docker_running():
        rich.print("[red]Docker is not running.[/red]")
        raise typer.Exit(1)
    _, _, _, workspace_id, _ = decrypt_tokens()
    volume_path = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description="Setting up things...", total=None)
        is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)
        if not is_yaml_present:
            config = {
                "name": name,
                "source_framework_type": "PYTORCH",
                "io_schema": True,
                "env": env_dict,
            }
        else:
            config = read_yaml(DEFAULT_YAML_FILE_NAME)

        if runtime and runtime_type == "replicate":
            Convertors.convert_cog_to_runtime_yaml(runtime, DEFAULT_RUNTIME_FILE_NAME)

        # add a logic to check if inferless.yaml is present. id yes continue else check for name param is present or generate new random name. check for env variables if sent via parmas. check for runtime param and type. if the type is not inferless run inferless export command and generate inferless-runtime-config file. 
        if (
            config
            and "configuration" in config
            and "custom_volume_id" in config["configuration"]
            and config["configuration"]["custom_volume_id"]
        ):
            progress.update(
                task_id, description="Getting your Volume Mount details..."
            )
            volume_data = find_volume_by_id(
                workspace_id, config["configuration"]["custom_volume_id"]
            )
            volume_path = volume_data["path"]

        model_name = config["name"]

        yaml_location = DEFAULT_RUNTIME_FILE_NAME

        if runtime:
            yaml_location = runtime
        elif "optional" in config and "runtime_file_name" in config["optional"]:
            yaml_location = config["optional"]["runtime_file_name"]

        if (
            "source_framework_type" in config
            and config["source_framework_type"] == "PYTORCH"
        ):
            progress.update(
                task_id,
                description="Generating required files for loading model...",
            )
            try:
                config_pbtxt_file_contents = get_cli_files("sample_config.pbtxt")
                config_pbtxt_file = base64.b64decode(
                    config_pbtxt_file_contents
                ).decode("utf-8")
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            inputs = create_config_from_json(config, config_pbtxt_file)

            io_schema = False
            if "io_schema" in config:
                io_schema = config["io_schema"]

            input_schema_path = "input_schema.py"
            data_dict = None
            if not io_schema:
                input_json = read_json(config["optional"]["input_file_name"])
                output_json = read_json(config["optional"]["output_file_name"])

            if os.path.exists(input_schema_path):
                data_dict = create_input_from_schema(input_schema_path)
                input_tensor = copy.deepcopy(data_dict["inputs"])
                output_tensor = []
            elif io_schema and not os.path.exists(input_schema_path):
                rich.print(
                    "[red]Input Schema not Found[/red]"
                )
            # elif io_schema and not os.path.exists(input_schema_path) then typer.exit("input schema not found")
            elif input_json and "inputs" in input_json:
                input_tensor = copy.deepcopy(input_json["inputs"])
                # ! Handle this edge case
                output_tensor = copy.deepcopy(output_json["outputs"])
            else:
                rich.print(
                    "[red]Both Input Schema and Input Json are not present[/red]"
                )
                raise typer.Exit(1)

            if (
                config
                and "configuration" in config
                and "is_serverless" in config["configuration"]
                and config["configuration"]["is_serverless"]
            ):
                try:
                    model_py_file_contents = get_cli_files(
                        "default_serverless_model.py"
                    )
                    model_py_file = base64.b64decode(model_py_file_contents).decode(
                        "utf-8"
                    )
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
            elif data_dict and "batch_size" in data_dict:
                try:
                    model_py_file_contents = get_cli_files("default_batch_model.py")
                    model_py_file = base64.b64decode(model_py_file_contents).decode(
                        "utf-8"
                    )
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
            else:
                try:
                    model_py_file_contents = get_cli_files("default_model.py")
                    model_py_file = base64.b64decode(model_py_file_contents).decode(
                        "utf-8"
                    )
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)

            generate_template_model(input_tensor, output_tensor, model_py_file)
        else:
            inputs = get_inputs_from_input_json(config)

        runtime_id = None
        runtime_url = None
        if (
            runtime is None
            and "configuration" in config
            and "custom_runtime_id" in config["configuration"]
        ):
            try:
                runtimes_list = get_templates_list(workspace_id)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            runtime_id = config["configuration"]["custom_runtime_id"]

            for item in runtimes_list:
                # Use .get() for safer access to dictionary items
                item_id = item.get("id")
                if item_id == runtime_id:
                    runtime_url = item.get("template_url")
                    break  # Exit the loop since we found the matching item

        BUILDING_DOCKER_MSG = (
            "Building the Docker Image (Might take some time. Please wait...)"
        )
        if runtime_id and not runtime_url:
            rich.print(
                f"[yellow]runtime with id: {runtime_id}, not found! Please check if the rutime is avaliabe in current workspace"
            )

        if os.path.exists(yaml_location):
            progress.update(
                task_id,
                description="Analysing your runtime config...",
            )
            try:
                docker_file_contents = get_cli_files("default_template_dockerfile")
                default_template_dockerfile = base64.b64decode(
                    docker_file_contents
                ).decode("utf-8")
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            default_template_dockerfile = default_template_dockerfile.replace(
                MODEL_DIR_STRING, f"/models/{model_name}/1/"
            )
            if (
                "source_framework_type" in config
                and config["source_framework_type"] == "PYTORCH"
            ):
                default_template_dockerfile = default_template_dockerfile.replace(
                    "##configpbtxt##",
                    f"COPY config.pbtxt /models/{model_name}/",
                )
            with open(yaml_location, "r") as yaml_file:
                default_template_dockerfile = load_yaml_file(
                    yaml_file, default_template_dockerfile
                )

                progress.update(
                    task_id,
                    description=BUILDING_DOCKER_MSG,
                )
                build_docker_image(default_template_dockerfile)
        elif runtime_url and runtime_id:
            progress.update(
                task_id,
                description="Analysing your runtime config...",
            )
            runtime_url = runtime_url.split("/")
            filename = (
                runtime_url[len(runtime_url) - 2]
                + "/"
                + runtime_url[len(runtime_url) - 1]
            )
            payload = {
                "url_for": "YAML_FILE_DOWNLOAD",
                "file_name": filename,
            }
            try:
                res = create_presigned_download_url(payload)
                response = get_file_download(res)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            if response.status_code == 200:
                yaml_file = response.content
                try:
                    docker_file_contents = get_cli_files(
                        "default_template_dockerfile"
                    )
                    default_template_dockerfile = base64.b64decode(
                        docker_file_contents
                    ).decode("utf-8")
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
                default_template_dockerfile = default_template_dockerfile.replace(
                    MODEL_DIR_STRING, f"/models/{model_name}/1/"
                )
                default_template_dockerfile = load_yaml_file(
                    yaml_file, default_template_dockerfile
                )
                if (
                    "source_framework_type" in config
                    and config["source_framework_type"] == "PYTORCH"
                ):
                    default_template_dockerfile = (
                        default_template_dockerfile.replace(
                            "##configpbtxt##",
                            f"COPY config.pbtxt /models/{model_name}/",
                        )
                    )

                progress.update(
                    task_id,
                    description=BUILDING_DOCKER_MSG,
                )
                build_docker_image(default_template_dockerfile)
        else:
            rich.print(
                "\n[yellow]No Custom runtime dectected. Using Inferless default runtime [/yellow]\n"
            )
            try:
                requirements_text_contents = get_cli_files("requirements.txt")
                requirements_text = base64.b64decode(
                    requirements_text_contents
                ).decode("utf-8")
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

            requirements_lines = requirements_text.strip().split("\n")
            requirements_lines = [
                line
                for line in requirements_lines
                if not line.strip().startswith("#")
            ]
            pip_install_commands = "\n".join(
                f"RUN pip install --no-cache-dir {line}"
                for line in requirements_lines
                if line.strip()
            )
            try:
                docker_file_contents = get_cli_files("default_dockerfile")
                default_dockerfile = base64.b64decode(docker_file_contents).decode(
                    "utf-8"
                )
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            default_dockerfile = default_dockerfile.replace(
                MODEL_DIR_STRING, f"/models/{model_name}/1/"
            )
            default_dockerfile = default_dockerfile.replace(
                "##localdependencies##", pip_install_commands
            )
            if (
                "source_framework_type" in config
                and config["source_framework_type"] == "PYTORCH"
            ):
                default_dockerfile = default_dockerfile.replace(
                    "##configpbtxt##", f"COPY config.pbtxt /models/{model_name}/"
                )
            progress.update(
                task_id,
                description=BUILDING_DOCKER_MSG,
            )
            build_docker_image(default_dockerfile)

        rich.print("[green]Docker Image Successfully Built.[/green]\n")
        files_to_delete = ["config.pbtxt", "model.py"]
        delete_files(files_to_delete)
        progress.update(
            task_id,
            description="Starting the Docker Container...",
        )
        env_vars = {}
        if "env" in config:
            env_vars = config["env"]

        # Start Docker container
        stop_containers_using_port_8000()
        if (
            "source_framework_type" in config
            and config["source_framework_type"] == "PYTORCH"
        ):
            start_docker_container(
                volume_path=volume_path, autostart=False, env=env_vars
            )
            time.sleep(10)
            load_model_template(model_name)
            time.sleep(5)
            infer_model(model_name, inputs)
            unload_model_template(model_name)
            load_model_template(model_name)
        else:
            start_docker_container(
                volume_path=volume_path, autostart=True, env=env_vars
            )

        progress.remove_task(task_id)

        rich.print("[green]Container started successfully.[/green]\n")
        rich.print(
            "\n[bold][yellow]Note: [/yellow][/bold]Container usually takes around 15 to 20 seconds to expose the PORT. cURL command should work after that.\n"
        )
        rich.print("\n[bold][underline]CURL COMMAND[/underline][/bold]\n")
        print_curl_command(model_name, inputs)


def create_requirements_file(requirements_text):
    with open("inferless_requirements.txt", "w") as f:
        f.write(requirements_text)


def unload_model_template(model_name):
    try:
        url = f"http://localhost:8000/v2/repository/models/{model_name}/unload"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        log_exception(e)


def load_model_template(model_name):
    try:
        url = f"http://localhost:8000/v2/repository/models/{model_name}/load"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        log_exception(e)


# Function to infer using the specified model and inputs
def infer_model(model_name, inputs):
    try:
        url = f"http://localhost:8000/v2/models/{model_name}/infer"
        headers = {"Content-Type": "application/json"}
        data = json.dumps(inputs)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        log_exception(e)


def execute_curl(curl_command):
    subprocess.run(curl_command, shell=True)


def find_volume_by_id(workspace_id, volume_id):
    try:
        volume = get_volume_info_with_id(workspace_id, volume_id)
        return volume
    except Exception as e:
        rich.print(e)
        raise typer.Exit(1)


# def print_curl_command(model_name: str, inputs: dict = None):
#     if inputs is None:
#         inputs = {}
#     json_data = json.dumps(inputs).replace("'", "\\'")
#     curl_command = f"curl --location 'http://localhost:8000/v2/models/{model_name}/infer' --header 'Content-Type: application/json' --data '{json_data}'"
#     rich.print(f"\n{curl_command}")
#     return curl_command


def print_curl_command(model_name: str, inputs: dict = None):
    if inputs is None:
        inputs = {}
    # Convert the inputs dict to a JSON string.
    json_data = json.dumps(inputs)

    # Escape single quotes for shell usage by wrapping the JSON data in double quotes
    # and escaping any internal double quotes.
    json_data_for_shell = json_data.replace('"', '\\"')

    # Prepare the curl command split across lines for readability.
    # Since we can't include backslashes directly in f-string expressions,
    # we add them outside of the expression braces.
    curl_command = (
        f"curl --location 'http://localhost:8000/v2/models/{model_name}/infer' \\\n"
        f"--header 'Content-Type: application/json' \\\n"
        f'--data "{json_data_for_shell}"'
    )

    rich.print(curl_command)
    return curl_command


def load_yaml_file(yaml_file, api_text_template_import):
    yaml_dict = yaml.load(yaml_file)
    sys_packages_string = ""
    pip_packages_string = ""
    if (
        "system_packages" in yaml_dict["build"]
        and yaml_dict["build"]["system_packages"] is not None
    ):
        sys_packages_string = "RUN apt update && apt -y install "
        for each in yaml_dict["build"]["system_packages"]:
            sys_packages_string = sys_packages_string + each + " "
    if (
        "python_packages" in yaml_dict["build"]
        and yaml_dict["build"]["python_packages"] is not None
    ):
        pip_packages_string = "RUN pip install "
        for each in yaml_dict["build"]["python_packages"]:
            pip_packages_string = pip_packages_string + each + " "

    api_text_template_import = api_text_template_import.replace(
        "##oslibraries##", sys_packages_string
    )
    api_text_template_import = api_text_template_import.replace(
        "##piplibraries##", pip_packages_string
    )
    return api_text_template_import
