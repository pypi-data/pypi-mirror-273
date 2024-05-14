import logging
import os
import sys
from importlib import metadata

log = logging.getLogger(__name__)


def load(plugins=(), full_install=True):
    try:
        version = metadata.version("virtualfish")
        commands = [f"set -g VIRTUALFISH_VERSION {version}"]
    except metadata.PackageNotFoundError:
        commands = []
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if full_install:
        commands += [
            f"set -g VIRTUALFISH_PYTHON_EXEC {sys.executable}",
            "source {}".format(os.path.join(base_path, "virtual.fish")),
        ]
    else:
        commands = []

    for plugin in plugins:
        path = os.path.join(base_path, plugin + ".fish")
        if os.path.exists(path):
            commands.append(f"source {path}")
        else:
            log.error(f"Plugin does not exist: {plugin}")
            sys.exit(1)

    if full_install:
        commands.append("emit virtualfish_did_setup_plugins")

    return commands
