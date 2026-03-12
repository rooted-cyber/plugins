import asyncio
from astra import Client, Message
from . import astra_command

IMAGE_PATH = "/storage/emulated/0/Download/ub.png"

@astra_command(
    name="neo",
    description="Show system info with image",
    category="System",
    usage=".neo",
    is_public=True
)
async def neofetch_cmd(client: Client, message: Message):
    try:
        start = await message.reply("⚡ Starting Astra Neofetch...")

        proc = await asyncio.create_subprocess_shell(
            "neofetch --stdout",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        output = stdout.decode().strip()

        caption = f"**🖥 Astra System Info**\n```\n{output}\n```"

        await message.reply_photo(
            photo=IMAGE_PATH,
            caption=caption
        )

        await start.delete()

    except Exception as e:
        await message.reply(f"❌ Error: {e}")