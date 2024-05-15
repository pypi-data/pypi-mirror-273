"""Handle /tokens."""
import prompt_toolkit as pt

from ..config import baseConf
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# change requested tokens amount
def handle_tokens(
    temp_file,
    messages,
    given="",
    temp_is_temp=False,
    silent=False
):
    """Handle /tokens.

    Command description:
        Changes the max amount of requested tokens.

    Usage:
        /tokens [max tokens]
    """
    given = given.strip()
    if given.isdigit():
        baseConf["max_tokens"] = int(given)
        if not silent:
            info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
        return messages
    if not silent:
        info_print(f'Currently requested tokens: {baseConf.get("max_tokens", 3000)}')
        info_print('How many tokens should be requested?')
    new_tokens = pt.prompt(pt.ANSI(
        '\n' + clrtxt("magenta", " tokens ") + ': '
    )).strip()
    if new_tokens.isdigit():
        baseConf["max_tokens"] = int(new_tokens)
        if not silent:
            info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
    else:
        if not silent:
            info_print('Invalid input, keeping current requested tokens amount')
    return messages


item_tokens = {
    "fun": handle_tokens,
    "help": "changes the max amount of requested tokens",
    "commands": ["tokens"],
}
