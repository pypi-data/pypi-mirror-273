import os
import subprocess

from .cycle_stage_base import EnvironmentTemplatedBase
from .stage import Stage

from cnc.logger import get_logger

log = get_logger(__name__)


class DeployStageManager(EnvironmentTemplatedBase):
    template_type = "deploy"

    def template_context(self, service):
        # cluster name, subnet, security group, load_database_snapshot (flag from CLI?)

        return {
            "deployer": self,
            "service": service,
            "environment": self.environment,
            "stage": Stage.model_validate({"name": "deploy"}),
            "load_database_snapshot": False,
            "environment_items": self.environment_items,
        }

    def render_scripts(self, service_names=None):
        context = self.template_context(None)
        if os.path.isfile(f"{self.config_files_path}/pre_deploy_functions.sh.j2"):
            self.write_template(
                "pre_deploy_functions.sh.j2",
                output_name=f"pre-deploy-{self.environment.name}-functions.sh",
                context=context,
            )
            self.write_template(
                "pre_deploy.sh.j2",
                output_name=f"pre-deploy-{self.environment.name}.sh",
                context=context,
            )
            self.scripts_to_run.append(f"pre-deploy-{self.environment.name}.sh")

        for service in self.environment.services:
            if service_names:
                if service.name not in service_names:
                    continue

            if service.settings.is_resource:
                continue

            context = self.template_context(service)
            context["render_template"] = self.write_template_with_context(service)

            self.write_template(
                "deploy_functions.sh.j2",
                output_name=f"deploy-{service.name}-functions.sh",
                context=context,
            )
            self.write_template(
                "main.sh.j2", output_name=f"deploy-{service.name}.sh", context=context
            )
            self.scripts_to_run.append(f"deploy-{service.name}.sh")

    def perform(self, should_cleanup=True, should_regenerate_config=True, debug=False, service_names=None):
        log.debug(f"Performing deploy for {self} @ {self.config_files_path}")
        if should_cleanup:
            self.cleanup()
        self.setup()
        if should_regenerate_config:
            self.render_scripts(service_names=service_names)
            log.debug(f"Done rendering deploy for {self} (svcs: {service_names}), going to execute...")

        if debug:
            for script in self.scripts_to_run:
                self.debug_template_output(script)

            log.debug(f"All done with debug for {self}")
            return

        for script in self.scripts_to_run:
            # self.debug_template_output("run-app.yml")

            try:
                # log.debug(f"Going to run {script}...")
                ret = subprocess.run(
                    ["bash", "-c", f"source {self.rendered_files_path}/{script}"],
                    executable="/bin/bash",
                )
                if ret.returncode != 0:
                    raise Exception(
                        f"Deploy failed for {self.rendered_files_path}/{script}"
                    )
                # log.debug(f"Output from {script}: \n{ret.stdout}\n{ret.stderr}")
            except subprocess.CalledProcessError as e:
                # Handle any errors that occurred during script execution
                print(f"Error running the script: {e}")
                print("Error output:")
                print(e.stderr)

        log.info(f"All done with perform for {self}")
