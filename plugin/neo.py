import asyncio
from astra import Client, Message
from . import astra_command

@astra_command(
    name="neo",
    description="Show system info using neofetch",
    category="System",
    usage=".neo",
    is_public=True
)
async def neofetch_cmd(client: Client, message: Message):
    try:
        proc = await asyncio.create_subprocess_shell(
            "neofetch --stdout",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if stdout:
            output = stdout.decode().strip()
            await message.reply(f"```\n{output}\n```")
        else:
            await message.reply("❌ Neofetch not installed")

    except Exception as e:
        await message.reply(f"Error: {e}")
