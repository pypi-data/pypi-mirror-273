import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import typer
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from inferless_cli.utils.constants import (
    DEFAULT_YAML_FILE_NAME,
    REGION_MAP,
    REGION_MAP_KEYS,
    REGION_MAP_VOLUME,
    REGION_MAP_VOLUME_KEYS,
)
from inferless_cli.utils.helpers import (
    key_bindings,
    create_yaml,
    decrypt_tokens,
    get_region_types,
    is_inferless_yaml_present,
    log_exception,
    yaml,
)

from prompt_toolkit.validation import Validator
from inferless_cli.utils.services import (
    delete_volume_files_url,
    create_presigned_download_url,
    create_presigned_upload_url,
    delete_volume_temp_dir,
    get_file_download,
    get_volume_info,
    get_volume_info_with_id,
    get_volumes_list,
    create_volume,
    get_workspaces_list,
    sync_s3_to_nfs,
    sync_s3_to_s3,
    get_volume_files,
    upload_file,
)
from inferless_cli.utils.validators import validate_region_types
from pathlib import Path

app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = "[progress.description]{task.description}"
no_volumes = "[red]No volumes found in your account[/red]"


@app.command(
    "list",
    help="List all existing volumes",
)
def list():
    _, _, _, workspace_id, _ = decrypt_tokens()

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        try:
            volumes = get_volumes_list(workspace_id=workspace_id)
        except Exception as e:
            rich.print(e)
            raise typer.Exit(1)

        progress.remove_task(task_id)

    if len(volumes) == 0:
        rich.print(no_volumes)
        raise typer.Exit(1)

    rich.print("\n[bold][underline]Volumes List[/underline][/bold]\n")
    for volume in volumes:
        volume_name = volume["name"]
        volume_id = volume["id"]
        path = volume["path"]
        region = volume["region"]
        mapped_region = REGION_MAP[region]
        mapped_region_vol = REGION_MAP_VOLUME[region]
        rich.print(f"Volume: [bold]{volume_name}[/bold]")
        rich.print(f"ID: [bold]{volume_id}[/bold]")
        rich.print(f"Mount Path: [bold][purple]{path}[/purple][/bold]")
        rich.print(f"Region: [blue][bold]{mapped_region}[/bold][/blue]")
        rich.print(
            f"Infer Path: [bold][purple]infer://volumes/{mapped_region_vol}/{volume_name}[/purple][/bold]\n"
        )


@app.command(
    "create",
    help="Create a new volume",
)
def create(
    name: str = typer.Option(
        None, "--name", "-n", help="Assign a name to the new volume."
    ),
):
    try:
        workspaces = get_workspaces_list()
    except Exception as e:
        rich.print(e)
        raise typer.Exit(1)
    _, _, _, workspace_id, workspace_name = decrypt_tokens()
    if name is None:
        name = prompt(
            "Enter the name for volume: ",
        )
    is_aws_enabled = False
    for workspace in workspaces:
        if workspace["id"] == workspace_id:
            is_aws_enabled = workspace["is_aws_cluster_enabled"]
            break

    region = None
    if is_aws_enabled:
        region = prompt(
            "Select Region ( Region 1, Region 2 ) : ",
            completer=get_region_types(),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(validate_region_types),
            validate_while_typing=False,
        )
    else:
        region = "Region 2"
    res = None
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            description=f"Creating model in [blue]{workspace_name}[/blue] workspace",
            total=None,
        )
        try:
            res = create_volume(
                workspace_id=workspace_id, name=name, region=REGION_MAP_KEYS[region]
            )
        except Exception as e:
            rich.print(e)
            raise typer.Exit(1)
        progress.remove_task(task_id)

    if "id" in res and "name" in res:
        rich.print(f"[green]Volume {res['name']} created successfully[/green]")
        is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)

        if is_yaml_present:
            is_update = typer.confirm(
                f"Found {DEFAULT_YAML_FILE_NAME} file. Do you want to update it? ",
                default=True,
            )
            if is_update:
                rich.print("Updating yaml file")
                with open(DEFAULT_YAML_FILE_NAME, "r") as yaml_file:
                    config = yaml.load(yaml_file)
                    config["configuration"]["custom_volume_id"] = res["id"]
                    config["configuration"]["custom_volume_name"] = res["name"]
                    create_yaml(config, DEFAULT_YAML_FILE_NAME)
                    rich.print(
                        f"[green]{DEFAULT_YAML_FILE_NAME} file updated successfully[/green]"
                    )


@app.command(
    "ls",
    help="List files and directories within a volume",
)
def list_files(
    id: str = typer.Option(
        None, "--id", "-i", help=" Specify the ID of the volume to list."
    ),
    path: str = typer.Option(
        None,
        "--path",
        "-p",
        help="Define a specific directory path within the volume. Defaults to the root directory if not specified.",
    ),
    directory_only: bool = typer.Option(
        False, "--directory", "-d", help="List only directories."
    ),
    files_only: bool = typer.Option(False, "--files", "-f", help="List only files."),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Recursively list contents of directories."
    ),
):
    _, _, _, workspace_id, _ = decrypt_tokens()
    if id is None:
        rich.print(
            "\n[red]Error: The --id option is required. Use `[blue]inferless volume list[/blue]` to find the volume id.[/red]\n"
        )
        raise typer.Exit(1)

    volume_data = find_volume_by_id(workspace_id, id)
    if volume_data is None:
        rich.print(f"[red]Error: No volume found with id {id}.[/red]")
        raise typer.Exit(1)

    volume_name = volume_data["name"]

    def list_directory(path, table):
        payload = {
            "volume_name": volume_name,
            "workspace_id": workspace_id,
            "volume_id": volume_data["id"],
        }

        if path != "":
            payload["file_path"] = path

        response = {}
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task("fetching files and directories")
            try:
                response = get_volume_files(payload)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

        progress.remove_task(task_id)
        if not response and not response["details"]:
            table.add_row(f"[yellow]No files or directories found at '{path}'[/yellow]")

        for item in response["details"]:
            if directory_only and item["type"] != "directory":
                continue
            if files_only and item["type"] != "file":
                continue

            path_new = path + "/" if path else ""

            table.add_row(
                f"[blue]{path_new}{item['name']}[/blue]",
                item["type"],
                str(item["file_size"]),
                item["created_at"],
            )
            if recursive and item["type"] == "directory":
                list_directory(f"{path_new}{item['name']}", table)

    table = Table(show_header=False, box=None)
    list_directory(path or "", table)
    rich.print(
        f"\n [green][bold]Volume: {volume_name}[/bold][/green] (Path: {path or '/'}) \n"
    )
    rich.print(table)
    rich.print("\n")
    if not recursive:
        rich.print(
            f"You can run `[blue]inferless volume ls -i {id} -p DIR_NAME[/blue]` for viewing files inside dir\n"
        )
        rich.print(
            "[green]Tip: Use the --recursive (-r) flag to list contents of directories recursively.[/green]\n\n"
        )


@app.command(
    "select", help="Select a volume for updates in the Inferless configuration."
)
def select(
    path: str = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to the Inferless configuration file (typically inferless.yaml)",
    ),
    id: str = typer.Option(None, "--id", "-i", help="The ID of the volume to select."),
):
    _, _, _, workspace_id, _ = decrypt_tokens()
    if id is None:
        rich.print(
            "\n[red]--id is required. Please use `[blue]inferless volume list[/blue]` to get the id[/red]\n"
        )
        raise typer.Exit(1)

    if path is None:
        path = prompt(
            "Enter path of inferless config file : ",
            default="%s" % DEFAULT_YAML_FILE_NAME,
        )

    volume = find_volume_by_id(workspace_id, id)

    if not volume:
        rich.print(
            "\n[red]Volume with id [blue]%s[/blue] not found in your workspace[/red]\n"
            % id
        )
        raise typer.Exit(1)

    rich.print("Updating yaml file")
    with open(path, "r") as yaml_file:
        config = yaml.load(yaml_file)
        config["configuration"]["custom_volume_name"] = volume["name"]
        config["configuration"]["custom_volume_id"] = volume["id"]
        create_yaml(config, DEFAULT_YAML_FILE_NAME)
        rich.print(f"[green]{DEFAULT_YAML_FILE_NAME} file updated successfully[/green]")


@app.command("cp", help="Add a file or directory to a volume.")
def copy(
    source: str = typer.Option(
        None,
        "--source",
        "-s",
        help="Specify the source path (either a local directory/file path or an Inferless path)",
    ),
    destination: str = typer.Option(
        None,
        "--destination",
        "-d",
        help="Specify the destination path (either a local directory/file path or an Inferless path)",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively copy the contents of a directory to the destination.",
    ),
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    if not source:
        rich.print("\n[red]--source is a required param")
        raise typer.Exit(1)
    if not destination:
        rich.print("\n[red]--destination is a required param")
        raise typer.Exit(1)

    if source and not source.startswith("infer://"):
        source = make_absolute(source)
    elif destination and not destination.startswith("infer://"):
        destination = make_absolute(destination)

    volume_name = ""
    cp_type = None
    if source.startswith("infer://"):
        volume_name, volume_region = extract_volume_info(source)
        cp_type = "DOWNLOAD"
    elif destination.startswith("infer://"):
        volume_name, volume_region = extract_volume_info(destination)
        cp_type = "UPLOAD"
    else:
        rich.print("\n[red]--source or --destination should start with infer://")
        raise typer.Exit(1)

    volume_data = find_volume_by_name(
        workspace_id, volume_name, REGION_MAP_VOLUME_KEYS[volume_region]
    )
    if volume_data is None:
        rich.print(f"[red]Error: No volume found with {volume_name}.[/red]")
        raise typer.Exit(1)
    vol_region = volume_data["region"]
    try:
        if cp_type == "UPLOAD":
            if os.path.isdir(source) and not recursive:
                rich.print(
                    f"[red]Please provide `-r` or `--recursive` flag to copy the directroy [/red]"
                )
                raise typer.Exit(1)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                s3_path = destination.split("infer://")[1]
                vol_id = volume_data["id"]
                mapped_region = REGION_MAP_VOLUME[vol_region]
                s3_path = s3_path.replace(
                    f"volumes/{mapped_region}/",
                    f"volumes_temp/{vol_region}/{workspace_id}/{vol_id}/",
                )
                try:
                    base_path_region = (
                        volume_data["region"] if volume_data["region"] else "AZURE"
                    )
                    base_path_volume_id = volume_data["id"]
                    base_path_volume_name = volume_data["name"]
                    base_temp_s3_path = f"volumes_temp/{base_path_region}/{workspace_id}/{base_path_volume_id}/{base_path_volume_name}"
                    payload = {"s3_path": base_temp_s3_path, "volume_id": vol_id}
                    delete_volume_temp_dir(payload)
                except Exception:
                    pass

                volume_data["volume_id"] = volume_data["id"]
                futures = []
                if os.path.isfile(source):
                    futures.append(
                        executor.submit(
                            process_file,
                            source,
                            s3_path,
                            source,
                        )
                    )

                elif os.path.isdir(source):
                    futures += process_directory(
                        executor,
                        source,
                        s3_path,
                        source,
                    )

                results = [future.result() for future in futures]
                if all(results):
                    rich.print("verifiying upload...")
                    s3_path_original = s3_path.replace(
                        f"volumes_temp/{vol_region}/", f"volumes/{vol_region}/"
                    )
                    payload = {"source": s3_path, "destination": s3_path_original}
                    try:
                        res = sync_s3_to_s3(payload)
                    except Exception as e:
                        rich.print(e)
                        raise typer.Exit(1)
                    base_s3_path_region = (
                        volume_data["region"] if volume_data["region"] else "AZURE"
                    )
                    base_s3_path_volume_id = volume_data["id"]
                    base_s3_path_volume_name = volume_data["name"]
                    base_s3_path = f"volumes/{base_s3_path_region}/{workspace_id}/{base_s3_path_volume_id}/{base_s3_path_volume_name}"
                    try:
                        sync_s3_to_nfs({"s3_path": base_s3_path, "volume_id": vol_id})
                    except Exception as e:
                        rich.print(e)
                        raise typer.Exit(1)
                    rich.print("\n[green]Upload successful[/green]\n\n")
                else:
                    rich.print("\n[red]Upload unsuccessful[/red]\n\n")
                    raise typer.Exit(1)

        if cp_type == "DOWNLOAD":
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description="Downloading..", total=None)
                s3_path = source.split("infer://")[1]
                vol_id = volume_data["id"]
                region = volume_data["region"]
                mapped_region = REGION_MAP_VOLUME[vol_region]
                s3_path = s3_path.replace(
                    f"volumes/{mapped_region}/",
                    f"volumes/{region}/{workspace_id}/{vol_id}/",
                )
                payload = {
                    "url_for": "VOLUME_FOLDER_DOWNLOAD",
                    "file_name": f"{s3_path}",
                }
                try:
                    res = create_presigned_download_url(payload)
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
                download_files_in_parallel(res, destination)
                progress.remove_task(task_id)
            rich.print(
                f"[green]downloaded successfully and saved at '{destination}'[/green]"
            )

    except Exception as e:
        log_exception(e)
        rich.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command(
    "rm", help="Specify the Inferless path to the file or directory you want to delete."
)
def delete(
    path: str = typer.Option(
        None, "--path", "-p", help="Infer Path to the file/dir your want to delete"
    ),
):

    if not path:
        rich.print("\n[red]--path is a required param\n")
        raise typer.Exit(1)

    _, _, _, workspace_id, _ = decrypt_tokens()
    volume_name, volume_region = extract_volume_info(path)
    if id is None:
        rich.print(
            "\n[red]--id is required. Please use `[blue]inferless volume list[/blue]` to get the id[/red]\n"
        )
        raise typer.Exit(1)

    volume_data = find_volume_by_name(
        workspace_id, volume_name, REGION_MAP_VOLUME_KEYS[volume_region]
    )
    if volume_data is None:
        rich.print(f"[red]Error: No volume found with name {volume_name}.[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description="deleting...", total=None)
        region = volume_data["region"] if "region" in volume_data else "AZURE"
        vol_id = volume_data["id"]
        s3_path = path.split("infer://")[1]
        mapped_region = REGION_MAP_VOLUME[region]
        s3_path = s3_path.replace(
            f"volumes/{mapped_region}/", f"volumes/{region}/{workspace_id}/{vol_id}/"
        )

        payload = {"s3_path": s3_path, "volume_id": vol_id}
        try:
            res = delete_volume_files_url(payload)
        except Exception as e:
            rich.print(e)
            raise typer.Exit(1)

        if res == "Deleted Successfully":
            rich.print("[green]File successfully deleted.[/green]")
        else:
            rich.print("[red]Failed to delete file.[/red]")

        progress.remove_task(task_id)


def find_volume_by_name(workspace_id, volume_name, volume_region):
    try:
        volume = get_volume_info(workspace_id, volume_name, volume_region)
        return volume
    except Exception as e:
        rich.print(e)
        raise typer.Exit(1)


def find_volume_by_id(workspace_id, volume_id):
    try:
        volume = get_volume_info_with_id(workspace_id, volume_id)

        return volume
    except Exception as e:
        rich.print(e)
        raise typer.Exit(1)


def process_file(path: str, s3_path, root_path):
    try:
        unix_file_path = Path(path).as_posix()
        unix_root_path = Path(root_path).as_posix()

        if unix_root_path == unix_file_path:
            save_path = s3_path
        else:
            relative_path = unix_file_path[len(unix_root_path) :].lstrip("/")
            save_path = f"{s3_path}/{relative_path}"

        if save_path.startswith("/"):
            save_path = save_path[1:]
        file_size = os.path.getsize(path)

        if file_size > 5 * 1024**3:  # File size is more than 5GB
            with open(path, "rb") as file:
                rich.print(f"Uploading {path}")
                save_path = save_path.replace("volumes_temp", "volumes")
                try:
                    url = upload_file(file, save_path, file_size, type="ANY")
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
                if url:
                    return True
        else:
            payload = {
                "url_for": "VOLUME_FILE_UPLOAD",
                "file_name": save_path,
            }
            try:
                res = create_presigned_upload_url(payload, path)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            if "status" in res and res["status"] == "success":
                return True
    except Exception as e:
        log_exception(e)
        return True


def process_directory(executor, dir_path: str, s3_path, root_path):
    futures = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = Path(root) / file
            unix_file_path = file_path.as_posix()
            future = executor.submit(process_file, unix_file_path, s3_path, root_path)
            futures.append(future)

    return futures


def extract_volume_info(input_string):
    # Splitting the URL by '/'
    parts = input_string.split("/")

    # Extracting workspace_id, volume_id, and volume_name
    # The indices are based on the structure of your URL
    volume_region = parts[3] if len(parts) > 3 else None
    volume_name = parts[4] if len(parts) > 4 else None

    return volume_name, volume_region


def make_request(url, destination):
    try:
        response = get_file_download(url)
    except Exception as e:
        rich.print(e)
        raise typer.Exit(1)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as file:
            file.write(response.content)
    else:
        rich.print(f"Failed to download {url}")


def download_files_in_parallel(file_dict, dest):
    # Using ThreadPoolExecutor to download files in parallel
    with ThreadPoolExecutor() as executor:
        # Creating a list of futures
        futures = []
        for local_path, url in file_dict.items():
            destination = os.path.join(dest, local_path)
            rich.print(f"Downloading {local_path} to {destination}")
            # Submitting the download task
            futures.append(executor.submit(make_request, url, destination))

        # Waiting for all futures to complete
        for future in futures:
            future.result()


def make_absolute(path):
    # Check if the path is either '.' (current directory) or a relative path
    if path == "." or not os.path.isabs(path):
        # Use os.path.abspath to convert to an absolute path
        return os.path.abspath(path)
    else:
        # If the path is already absolute, return it as is
        return path
