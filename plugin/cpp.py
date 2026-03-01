from . import *
import asyncio
import os

@astra_command(name="cppcurl")
async def cppcurl_cmd(client, message):
    msg = await message.reply("🔄 Downloading & running script...")

    cmd = (
        'bash -c "$(curl -fsSL '
        'https://gist.githubusercontent.com/rooted-cyber/'
        '509190613bafda0a30539e3e10932877/raw/cpp'
        ')"'
    )

    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if error:
            await msg.edit(f"❌ Error:\n```{error}```")
        else:
            await msg.edit(f"✅ Output:\n```{output}```")

    except Exception as e:
        await msg.edit(f"❌ Failed:\n`{e}`")
