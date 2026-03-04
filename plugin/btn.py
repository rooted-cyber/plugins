from telethon import Button, events
from . import *
import os

@astra_command(name="btn")
async def btn_handler(client, message):

    # File create using with open
    code = """
from telethon import Button

buttons = [
    [Button.url("🌐 Google", "https://google.com")],
    [Button.inline("⚡ Click Me", b"astra_click")]
]
"""

    with open("buttons_data.py", "w") as f:
        f.write(code)

    os.system("python but*")