from . import *
import traceback
import sys
import io

@astra_command(name="eval")
async def eval_cmd(client, message):

    if message.sender_id not in SUDO_USERS:
        return await message.reply("❌ Not Allowed")

    cmd = message.text.split(" ", 1)

    if len(cmd) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = cmd[1]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()
    except Exception:
        output = traceback.format_exc()

    sys.stdout = old_stdout

    if not output:
        output = "✅ Done"

    await message.reply(f"```\n{output}\n```")
