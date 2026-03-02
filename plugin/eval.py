from . import *
import traceback
import sys
import io
import asyncio

@astra_command(name="eval")
async def eval_cmd(client, message):

    if message.sender_id not in SUDO_USERS:
        return await message.reply("❌ Not Allowed")

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = args[1]

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()

    try:
        # async support
        exec(
            f'async def __aexec(client, message):\n'
            + '\n'.join(f'    {line}' for line in code.split('\n'))
        )

        await locals()["__aexec"](client, message)

        result = redirected_output.getvalue()

    except Exception:
        result = traceback.format_exc()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if not result:
        result = "✅ Done"

    await message.reply(f"```\n{result}\n```")
