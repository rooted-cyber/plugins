import asyncio
import base64
import os
import time
import platform
from astra import Client, Message
from . import astra_command

IMAGE_PATH = "/storage/emulated/0/Download/ub.png"
START_TIME = time.time()


def get_image():
    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def uptime():
    up = int(time.time() - START_TIME)
    return f"{up//3600}h {(up%3600)//60}m {up%60}s"


# ---------------- ALIVE ---------------- #

@astra_command(
    name="al",
    description="Check bot status",
    category="System",
    usage=".alive",
    is_public=True
)
async def alive_cmd(client: Client, message: Message):

    ping_start = time.time()
    await asyncio.sleep(0)
    ping = round((time.time() - ping_start) * 1000)

    caption = f"""
**🚀 Astra Userbot Alive**

⚡ Ping: `{ping} ms`
⏱ Uptime: `{uptime()}`
🐍 Python: `{platform.python_version()}`
"""

    img = get_image()

    if img:
        await client.send_media(
            message.chat.id,
            {"mimetype": "image/png", "data": img},
            caption=caption,
            reply_to=message.id
        )
    else:
        await message.reply(caption)


# ---------------- NEOFETCH ---------------- #

@astra_command(
    name="neo",
    description="Show neofetch",
    category="System",
    usage=".neo",
    is_public=True
)
async def neo_cmd(client: Client, message: Message):

    start = await message.reply("⚡ Running neofetch...")

    proc = await asyncio.create_subprocess_shell(
        "neofetch --stdout",
        stdout=asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()
    output = stdout.decode()

    caption = f"**🖥 System Info**\n```\n{output}\n```"

    img = get_image()

    if img:
        await client.send_media(
            message.chat.id,
            {"mimetype": "image/png", "data": img},
            caption=caption,
            reply_to=message.id
        )
    else:
        await message.reply(caption)

    await start.delete()


# ---------------- SYS ---------------- #

@astra_command(
    name="sys",
    description="Basic system info",
    category="System",
    usage=".sys",
    is_public=True
)
async def sys_cmd(client: Client, message: Message):

    caption = f"""
**💻 System Info**

OS: `{platform.system()}`
Kernel: `{platform.release()}`
Python: `{platform.python_version()}`
Uptime: `{uptime()}`
"""

    img = get_image()

    if img:
        await client.send_media(
            message.chat.id,
            {"mimetype": "image/png", "data": img},
            caption=caption,
            reply_to=message.id
        )
    else:
        await message.reply(caption)
