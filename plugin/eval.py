from . import *
import sys
import io
import traceback
import asyncio

@astra_command(name="eval")
async def eval_cmd(client, message):

    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = parts[1]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Wrap code inside async function
        exec(
            f"async def __eval_func(client, message):\n"
            + "\n".join(f"    {line}" for line in code.split("\n"))
        )

        result = await locals()["__eval_func"](client, message)
        output = sys.stdout.getvalue()

        if result:
            output += str(result)

    except Exception:
        output = traceback.format_exc()

    finally:
        sys.stdout = old_stdout

    if not output:
        output = "✅ Done"

    await message.reply(f"```\n{output}\n```")
