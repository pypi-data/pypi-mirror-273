from typing import List
import typer

from cnc.models import ProvisionStageManager
from .telemetry import send_event

from cnc.logger import get_logger

log = get_logger(__name__)


app = typer.Typer()


@app.callback()
def add_common(
    ctx: typer.Context,
    collection_name: str = typer.Option(
        default=None, envvar="CNC_COLLECTION_NAME", help="Collection name"
    ),
):
    """Common Entry Point for Provision"""
    if collection_name:
        collection = ctx.obj.application.collection_by_name(collection_name)
        if not collection:
            log.error(
                f"No collection found for: {collection_name} | (configured "
                f"collections are: {[c.name for c in ctx.obj.application.collections]})"
            )
            raise typer.Exit(code=1)
    elif len(ctx.obj.application.collections) == 1:
        collection = ctx.obj.application.collections[0]
    else:
        log.error(
            f"No collection name provided and more than one collection found for {ctx.obj.application} | (configured "
            f"collections are: {[c.name for c in ctx.obj.application.collections]})"
        )
        raise typer.Exit(code=1)

    ctx.obj.collection = collection


@app.command()
def plan(
    ctx: typer.Context,
    cleanup: bool = True,
    generate: bool = True,
):
    """Generate an infrastructure plan"""
    send_event("provision.plan")
    tf_config = ProvisionStageManager(ctx.obj.collection)
    is_setup = tf_config.make_ready_for_use(
        should_cleanup=cleanup,
        should_regenerate_config=generate,
    )

    if not is_setup:
        log.info(f"Cannot setup {tf_config}")
        return

    try:
        plan = tf_config._tf_command("plan")
        log.info(plan)
    except Exception as e:
        log.error(f"Cannot do TF plan for {tf_config}: {e}")
    finally:
        if cleanup:
            tf_config.cleanup()

    log.debug(f"All set planning for {tf_config.config_files_path}")
    raise typer.Exit()


@app.command()
def apply(
    ctx: typer.Context,
    cleanup: bool = True,
    generate: bool = True,
):
    """Apply an infrastructure plan"""
    send_event("provision.apply")
    tf_config = ProvisionStageManager(ctx.obj.collection)
    is_setup = tf_config.make_ready_for_use(
        should_cleanup=cleanup,
        should_regenerate_config=generate,
    )

    if not is_setup:
        log.info(f"Cannot setup {tf_config}")
        return

    try:
        _ret = tf_config._tf_command("apply")
        log.info(_ret)
    except Exception as e:
        log.error(f"Cannot do TF apply for {tf_config}: {e}")
    finally:
        if cleanup:
            tf_config.cleanup()

    log.debug(f"All set applying for {tf_config.config_files_path}")
    raise typer.Exit()


@app.command()
def debug(
    ctx: typer.Context,
    cleanup: bool = False,
    generate: bool = True,
):
    """Debug an infrastructure plan"""
    send_event("provision.debug")
    tf_config = ProvisionStageManager(ctx.obj.collection)
    is_setup = tf_config.make_ready_for_use(
        should_cleanup=cleanup,
        should_regenerate_config=generate,
    )

    if not is_setup:
        log.info(f"Cannot setup {tf_config}")
        return

    try:
        tf_config.debug_template_output_directory()
        tf_config.debug_template_output("main.tf")
    except Exception as e:
        log.error(f"Cannot do TF debug for {tf_config}: {e}")
    finally:
        if cleanup:
            tf_config.cleanup()

    log.debug(f"All set debugging for {tf_config}")
    raise typer.Exit()


@app.command()
def cmd(ctx: typer.Context, tf_cmd: List[str]):
    """Run an infrastructure command in the CLI"""
    send_event("provision.cmd")
    tf_config = ProvisionStageManager(ctx.obj.collection)
    tf_config.make_ready_for_use()

    try:
        _ret = tf_config._tf_command(tf_cmd[0], args=tf_cmd[1:])
        log.info(_ret)
    except Exception as e:
        log.error(f"Cannot do TF ({tf_cmd}) for {tf_config}: {e}")
    finally:
        tf_config.cleanup()

    log.debug(f"All set running cmd {tf_cmd} for {tf_config.config_files_path}")
    raise typer.Exit()
