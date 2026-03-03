from . import *
import sys
import io
import traceback

@astra_command(name="eval")
async def eval_cmd(client, message):

    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = parts[1]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    env = {
        "client": client,
        "message": message,
        "event" : message,
    }

    try:
        exec(
            "async def __eval_func():\n"
            + "\n".join(f"    {line}" for line in code.split("\n")),
            env
        )

        result = await env["__eval_func"]()
        output = sys.stdout.getvalue()

        if result:
            output += str(result)

    except Exception:
        output = traceback.format_exc()

    finally:
        sys.stdout = old_stdout

    #if not output:


    await message.reply(f"```\n{output}\n```")
