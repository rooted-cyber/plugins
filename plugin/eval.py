from . import *
import sys
import io
import traceback

@astra_command(name="eval")
async def eval_cmd(client, message):

    # SUDO check
    if message.sender_id not in SUDO_USERS:
        return await message.reply("❌ Not Allowed")

    # Get code
    parts = message.text.split(" ", 1)

    if len(parts) < 2:
        return await message.reply("Usage: .eval print('hi')")

    code = parts[1]

    # Capture output
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()

        result = output if output else error

    except Exception:
        result = traceback.format_exc()

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    if not result:
        result = "✅ Done"

    await message.reply(f"```\n{result}\n```")
