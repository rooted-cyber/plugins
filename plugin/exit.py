import os
from utils.plugin_utils import astra_command

@astra_command("e")
async def exit_cmd(client, message):
    await message.reply("🚪 Astra exiting...")
    print("""h""")
    os._exit(0)
