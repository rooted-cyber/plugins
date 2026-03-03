from utils.plugin_utils import astra_command
import sys
import io
import traceback

@astra_command(name="eval")
async def eval_cmd(client, message):
    if not message.from_user.is_self:
        return

    cmd = message.text.split(" ", 1)
    if len(cmd) < 2:
        return await message.reply("Usage: .eval <code>")

    code = cmd[1]

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    env = {
        "client": client,
        "message": message,
        "asyncio": __import__("asyncio"),
        "__name__": "__main__",
    }

    try:
        exec(
            "async def __eval_func__():\n"
            + "\n".join(f"    {line}" for line in code.split("\n")),
            env,
        )

        result = await env["__eval_func__"]()
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()

        if output:
            final_output = output
        elif error:
            final_output = error
        elif result is not None:
            final_output = str(result)
        else:
            final_output = "Success ✅"

    except Exception:
        final_output = traceback.format_exc()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if len(final_output) > 4000:
        final_output = final_output[:4000] + "\n\n...Output Truncated..."

    await message.reply(f"```\n{final_output}\n```")import sys
import io
import traceback

@astra_command(name="eval")
async def eval_cmd(client, message):
    if not message.from_user.is_self:
        return

    cmd = message.text.split(" ", 1)
    if len(cmd) < 2:
        return await message.reply("Usage: .eval <code>")

    code = cmd[1]

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    env = {
        "client": client,
        "message": message,
        "asyncio": __import__("asyncio"),
        "__name__": "__main__",
    }

    try:
        exec(
            "async def __eval_func__():\n"
            + "\n".join(f"    {line}" for line in code.split("\n")),
            env,
        )

        result = await env["__eval_func__"]()
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()

        if output:
            final_output = output
        elif error:
            final_output = error
        elif result is not None:
            final_output = str(result)
        else:
            final_output = "Success ✅"

    except Exception:
        final_output = traceback.format_exc()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if len(final_output) > 4000:
        final_output = final_output[:4000] + "\n\n...Output Truncated..."

    await message.reply(f"```\n{final_output}\n```")
