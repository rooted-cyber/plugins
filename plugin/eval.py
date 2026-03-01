from . import *
import traceback
import sys
import io
import asyncio

@astra_command(name="eval")
async def cpp_handler(okbclient, message):

    if message.sender_id not in SUDO_USERS:
        return await message.reply("❌ You are not allowed to use this command.")

    code = message.text.split(maxsplit=1)

    if len(code) < 2:
        return await message.reply("Usage: `.cpp print('hello')`")

    cmd = code[1]

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()

    async def aexec(code, event, client):
        exec(
            f'async def __aexec(event, client):\n'
            + ''.join(f'\n {line}' for line in code.split('\n'))
        )
        return await locals()['__aexec'](event, client)

    try:
        await aexec(cmd, message, client)
        result = redirected_output.getvalue()
        error = redirected_error.getvalue()

        if error:
            await message.reply(f"❌ Error:\n`{error}`")
        elif result:
            await message.reply(f"✅ Output:\n`{result}`")
        else:
            await message.reply("✅ Code Executed Successfully")

    except Exception:
        await message.reply(f"❌ Exception:\n`{traceback.format_exc()}`")

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
