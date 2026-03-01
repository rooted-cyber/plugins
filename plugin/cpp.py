from . import *
import os
import asyncio

URL = "https://gist.githubusercontent.com/rooted-cyber/509190613bafda0a30539e3e10932877/raw/cpp"

@astra_command(name="cppcurl")
async def cppcurl_handler(client, message):

    if message.sender_id not in SUDO_USERS:
        return await message.reply("❌ You are not allowed to use this command.")

    msg = await message.reply("⚡ Running remote script...")

    try:
        process = await asyncio.create_subprocess_shell(
            f'curl -fsSL {URL} -o cpp_script.sh && bash cpp_script.sh',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if error:
            await msg.edit(f"❌ Error:\n`{error[:4000]}`")
        elif output:
            await msg.edit(f"✅ Output:\n`{output[:4000]}`")
        else:
            await msg.edit("✅ Script Executed Successfully")

    except Exception as e:
        await msg.edit(f"❌ Exception:\n`{str(e)}`")
