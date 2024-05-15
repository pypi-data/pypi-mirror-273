import typer
from typing import List

from cnc.models import DeployStageManager
from .telemetry import send_event

from cnc.logger import get_logger

log = get_logger(__name__)


app = typer.Typer()


@app.command()
def perform(
    ctx: typer.Context,
    environment_name: str,
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
    send_event("deploy.perform")
    collection = ctx.obj.application.collection_by_name(collection_name)
    if not collection:
        log.error(f"No collection found for: {collection_name}")
        raise typer.Exit(code=1)

    environment = collection.environment_by_name(environment_name)
    if not environment:
        log.error(f"No environment found for: {environment_name}")
        raise typer.Exit(code=1)

    deployer = DeployStageManager(environment, service_tags=service_tags)
    deployer.perform(
        should_cleanup=cleanup,
        should_regenerate_config=generate,
        debug=debug,
    )

    log.debug(f"All set deploying for {deployer.rendered_files_path}")
    raise typer.Exit()
