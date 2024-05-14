"""Handle /genconf."""
from ..OwegaSession import OwegaSession as ps
from ..utils import genconfig


# generates config file
def handle_genconf(
    temp_file,
    messages,
    given="",
    temp_is_temp=False,
    silent=False
):
    """Handle /genconf.

    Command description:
        (Re)generates owega's config file.

    Usage:
        /genconf
    """
    genconfig()
    return messages


item_genconf = {
    "fun": handle_genconf,
    "help": "generates a sample config file",
    "commands": ["genconf"],
}
