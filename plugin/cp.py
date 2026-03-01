from . import *
import asyncio
import os
import sys

@astra_command(name="cp")
async def cppcurl_cmd(client, message):
    msg = await message.reply("🔄 Running update script...")

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

        # ✅ Real failure only if returncode != 0
        if process.returncode != 0:
            return await msg.edit(
                f"❌ Failed (code {process.returncode}):\n```{error or output}```"
            )

        # ✅ Success
        combined = (output + "\n" + error).strip()
        await msg.edit(f"✅ Update Completed:\n```{combined}```")

        # 🔥 Auto Restart After Success
        await asyncio.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        await msg.edit(f"❌ Exception:\n`{e}`")
