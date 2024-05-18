import typer
import time
from typing import List

from cnc.models import BuildStageManager
from .telemetry import send_event

from cnc.logger import get_logger
log = get_logger(__name__)


app = typer.Typer()


@app.command()
def perform(
    ctx: typer.Context,
    environment_name: str,
    services: List[str] = typer.Option(
        [],
        "--service",
        help="Set for each service you want to build, if omitted will build all.",
    ),
    service_tags: List[str] = typer.Option(
        [],
        "--service-tag",
        help="Set the tag to use for this service, default is 'latest'",
    ),
    collection_name: str = "",
    cleanup: bool = True,
    debug: bool = False,
    generate: bool = True,
):
    """Build containers for config-defined services"""
    start_time = time.time()
    send_event("build.perform")
    collection = ctx.obj.application.collection_by_name(collection_name)
    if not collection:
        log.error(f"No collection found for: {collection_name}")
        raise typer.Exit(code=1)

    environment = collection.environment_by_name(environment_name)
    if not environment:
        log.error(f"No environment found for: {environment_name}")
        raise typer.Exit(code=1)

    builder = BuildStageManager(environment, service_tags=service_tags)
    builder.perform(
        should_cleanup=cleanup,
        should_regenerate_config=generate,
        debug=debug,
        service_names=services,
    )

    log.debug(f"All set building for {builder.config_files_path} in {int(start_time - time.time())} seconds")
    raise typer.Exit()
