from . import *
import sys
import io
import traceback
import asyncio
from utils import astra_command

@astra_command(name="eval")
async def eval_cmd(client, message):

    if len(message.text.split(None, 1)) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = message.text.split(None, 1)[1]

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    env = {
        "client": client,
        "message": message,
        "m": message,
        "c": client,
        "asyncio": asyncio,
        "__name__": "__main__",
    }

    try:
        exec(
            "async def __eval_func():\n"
            + "\n".join(f"    {line}" for line in code.split("\n")),
            env,
        )

        result = await env["__eval_func"]()

        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()

        final_output = output or error or str(result) or "Success"

    except Exception:
        final_output = traceback.format_exc()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    try:
        await message.reply(f"```\n{final_output}\n```")
    except:
        print(final_output)
