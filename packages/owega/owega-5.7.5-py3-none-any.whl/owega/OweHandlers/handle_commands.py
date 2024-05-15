"""Handle /commands."""
from ..config import baseConf
from ..OwegaFun import existingFunctions
from ..OwegaSession import OwegaSession as ps
from ..utils import info_print


# enables/disables command execution
def handle_commands(
    temp_file,
    messages,
    given="",
    temp_is_temp=False,
    silent=False
):
    """Handle /commands.

    Command description:
        Toggles command execution / file creation.

    Usage:
        /commands [on/true/enable/enabled/off/false/disable/disabled]
    """
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["commands"] = True
        existingFunctions.enableGroup("utility.system")
        if not silent:
            info_print("Command execution enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["commands"] = False
        existingFunctions.disableGroup("utility.system")
        if not silent:
            info_print("Command execution disabled.")
        return messages

    baseConf["commands"] = (not baseConf.get("commands", False))
    if baseConf.get("commands", False):
        existingFunctions.enableGroup("utility.system")
        if not silent:
            info_print("Command execution enabled.")
    else:
        existingFunctions.disableGroup("utility.system")
        if not silent:
            info_print("Command execution disabled.")
    return messages


item_commands = {
    "fun": handle_commands,
    "help": "toggles command execution / file creation",
    "commands": ["commands"],
}
