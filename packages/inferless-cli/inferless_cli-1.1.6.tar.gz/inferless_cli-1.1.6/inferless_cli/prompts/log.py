from datetime import datetime, timedelta
import rich
import typer
from inferless_cli.utils.helpers import log_exception
from inferless_cli.utils.services import get_build_logs, get_call_logs
import dateutil.parser


def log_prompt(model_id: str, logs_type: str = "BUILD", import_logs: bool = False):
    if not model_id:
        rich.print("[red]Please provide a model id or model import id[/red]")
        raise typer.Abort(1)
    if logs_type == "BUILD":
        try:
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
            _type = import_logs and "MODELIMPORT" or "MODEL"
            payload = {
                "model_id": model_id,
                "time_from": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "time_to": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "type": _type,
            }
            token = None
            while True:
                # Fetch logs based on the build_id and token
                if token:
                    payload["next_token"] = token
                try:
                    logs = get_build_logs(payload)
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)

                if len(logs["details"]) == 0 and not token:
                    rich.print("\nNo Logs found\n")

                for log_entry in logs["details"]:
                    timestamp = "-"
                    try:
                        timestamp = dateutil.parser.isoparse(log_entry["time"])
                    except Exception as e:
                        log_exception(e)

                    rich.print(f"[green]{timestamp}[/green]: {log_entry['log']}")

                # Check if there is a next_token
                next_token = logs.get("next_token")

                if not next_token:
                    break

                # Update the token for the next iteration
                token = next_token
        except Exception as e:
            rich.print(f"[red]Error while fetching build logs: {e}[/red]")
            log_exception(e)
            raise typer.Abort(1)
    elif logs_type == "CALL":
        try:
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
            payload = {
                "model_id": model_id,
                "time_from": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "time_to": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            token = None
            while True:
                # Fetch logs based on the build_id and token
                if token:
                    payload["next_token"] = token
                try:
                    logs = get_call_logs(payload)
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)

                if len(logs["details"]) == 0 and not token:
                    rich.print("\nNo Logs found\n")

                for log_entry in logs["details"]:
                    timestamp = "-"
                    try:
                        timestamp = dateutil.parser.isoparse(log_entry["time"])
                    except Exception as e:
                        log_exception(e)
                    rich.print(f"[green]{timestamp}[/green]: {log_entry['log']}")

                # Check if there is a next_token
                next_token = logs.get("next_token")
                if not next_token:
                    break

                # Update the token for the next iteration
                token = next_token
        except Exception as e:
            rich.print(f"[red]Error while fetching call logs: {e}[/red]")
            log_exception(e)
            raise typer.Abort(1)
