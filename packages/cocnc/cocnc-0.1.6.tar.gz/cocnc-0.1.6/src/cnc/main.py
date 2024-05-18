import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Any

import typer
from rich import print

from .commands import provision, build, deploy, info, shell, toolbox, update
from .commands.template_editor import inspector
from .commands.telemetry import send_event
from .models import Application
from .check_dependencies import check_deps
from cnc.logger import get_logger

log = get_logger(__name__)

app = typer.Typer()
app.add_typer(provision.app, name="provision")
app.add_typer(build.app, name="build")
app.add_typer(deploy.app, name="deploy")
app.add_typer(inspector.app, name="inspector")
app.add_typer(info.app, name="info")
app.add_typer(shell.app, name="shell")
app.add_typer(toolbox.app, name="toolbox")
app.add_typer(update.app, name="update")

@dataclass
class Common:
    application: Any = None
    collection: Any = None


@app.callback()
def add_common(
    ctx: typer.Context,
    config_file_path: Path = typer.Option(
        default="cnc.yml", envvar="CNC_CONFIG_PATH", help="CNC config file path"
    ),
    environments_file_path: Path = typer.Option(
        default="environments.yml",
        envvar="CNC_ENVIRONMENTS_PATH",
        help="Environments data file path",
    ),
):
    """Common Entry Point for whole app"""
    if "--help" in sys.argv:
        return True

    check_deps()

    if not config_file_path.is_file():
        log.error(f"Config file not found: {config_file_path}")
        raise typer.Exit(code=1)

    if not environments_file_path.is_file():
        log.error(f"Environments data file not found: {environments_file_path}")
        raise typer.Exit(code=1)

    application = Application.from_environments_yml(
        environments_file_path,
        config_file_path,
    )
    if not application:
        log.error(f"No application for: {environments_file_path}")
        raise typer.Exit(code=1)

    ctx.obj = Common(application)


@app.command()
def hello():
    send_event("hello")
    print("[bold red]Welcome[/bold red] to [bold purple]" "CNC[/bold purple]")

    raise typer.Exit()


if __name__ == "__main__":
    app()
