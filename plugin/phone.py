from . import *
import asyncio
import re

@astra_command(name="phone")
async def phone_cmd(client, message):

    msg = await message.reply("📲 Running phone script...")

    cmd = (
        'sh -c "$(curl -fsSL '
        'https://gist.githubusercontent.com/rooted-cyber/cdb6533f500f53dd46404968794bec9a/raw/phone.sh'
        ')"'
    )

    try:
        # Run process
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # Decode output
        output = (stdout.decode(errors="ignore") + stderr.decode(errors="ignore")).strip()

        # Remove ANSI colors AFTER output is created
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        output = ansi_escape.sub('', output)

        # Empty output handle
        if not output:
            output = "✅ Script executed."

        # Large output handle
        if len(output) > 40000:
            file_name = "phone_output.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(output)
            await message.reply_document(file_name)
        else:
            await msg.edit(f"**Output:**\n`{output}`")

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{str(e)}`")
