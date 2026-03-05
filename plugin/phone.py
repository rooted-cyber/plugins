from . import *
import asyncio
import os
import sys

@astra_command(name="phone")
async def phone_cmd(client, message):

    msg = await message.reply("📲 Running phone script...")

    cmd = (
        'sh -c "$(curl -fsSL '
        'https://gist.githubusercontent.com/rooted-cyber/cdb6533f500f53dd46404968794bec9a/raw/phone.sh'
        ')"'
    )

    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        output = stdout.decode().strip() + stderr.decode().strip()

        if not output:
            output = "✅ Script executed."

        if len(output) > 4000:
            with open("phone_output.txt", "w") as f:
                f.write(output)
            await message.reply_document("phone_output.txt")
        else:
            await msg.edit(f"**Output:**\n`{output}`")

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{e}`")
