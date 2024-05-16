import shutil
import sys

from .logger import get_logger

log = get_logger(__name__)


def check_deps():
    # add provider-specific ones
    # check bash shell available
    # print info of what version of each is installed
    # print tested versions?

    for tool_name in ["terraform"]:
        check_if_installed(tool_name)


def check_if_installed(tool_name):
    if shutil.which(tool_name) is None:
        log.warning(f"Error: The tool '{tool_name}' is not installed.")
        sys.exit(1)
