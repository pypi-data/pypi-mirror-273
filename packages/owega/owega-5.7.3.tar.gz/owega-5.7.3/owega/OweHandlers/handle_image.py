"""Handle /image."""
import base64
import mimetypes
import tempfile
import time

import openai
import prompt_toolkit as pt

from ..ask import ask
from ..config import baseConf
from ..OwegaFun import existingFunctions, functionlist_to_toollist
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, estimated_tokens_and_cost, info_print, play_tts


def encode_image(filename: str) -> str:
    """
    Return the local image as a base64 url.

    Args:
        filename: The path to the image file to encode.

    Returns:
        The base64url-encoded image.
    """
    if "http" in filename:
        return filename
    out_str = filename
    try:
        with open(filename, "rb") as image_data:
            mt = mimetypes.guess_type(filename)[0]
            if not isinstance(mt, str):
                mt = 'data'
            out_str = f"data:{mt};base64,"
            out_str += base64.b64encode(image_data.read()).decode('utf-8')
    except Exception:
        pass
    return out_str


def handle_image(
    temp_file, messages, given="", temp_is_temp=False, silent=False
):
    """Handle /image.

    Command description:
        Sends a prompt and an image from an url.

    Usage:
        /image [image path/url] [prompt]
    """
    given = given.strip()
    user_prompt = ''
    if given.split(' ')[0]:
        image_url = given.split(' ')[0]
        user_prompt = ' '.join(given.split(' ')[1:])
    else:
        image_url = ps['main'].prompt(pt.ANSI(
            clrtxt("yellow", " IMAGE URL ") + ": ")).strip()
    image_url = encode_image(image_url)
    image_urls = [image_url]
    if not user_prompt:
        user_prompt = ps['main'].prompt(pt.ANSI(
            clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
    if baseConf.get("estimation", False):
        etkn, cost = estimated_tokens_and_cost(
            "",
            messages,
            functionlist_to_toollist(existingFunctions.getEnabled()),
            baseConf.get('model', ''),
            baseConf.get("max_tokens", 4096)
        )
        if not silent:
            print(f"\033[37mestimated tokens: {etkn}\033[0m")
            print(f"\033[37mestimated cost: {cost:.5f}\033[0m")
    if baseConf.get("debug", False):
        pre_time = time.time()
    messages.add_image(user_prompt, image_urls)
    messages = ask(
        prompt=None,
        messages=messages,
        model=baseConf.get("model", ""),
        temperature=baseConf.get("temperature", 0.8),
        max_tokens=baseConf.get("max_tokens", 3000),
        top_p=baseConf.get("top_p", 1.0),
        frequency_penalty=baseConf.get("frequency_penalty", 0.0),
        presence_penalty=baseConf.get("presence_penalty", 0.0)
    )
    if baseConf.get("debug", False):
        post_time = time.time()
        if not silent:
            print(f"\033[37mrequest took {post_time-pre_time:.3f}s\033[0m")
    if not silent:
        print()
        print(' ' + clrtxt("magenta", " Owega ") + ": ")
        print()
        print(messages.last_answer())
    if baseConf.get('tts_enabled', False):
        play_tts(messages.last_answer())
    return messages


item_image = {
    "fun": handle_image,
    "help": "sends a prompt and an image from an url",
    "commands": ["image"],
}
