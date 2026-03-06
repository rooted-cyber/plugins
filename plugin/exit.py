import os
from utils.plugin_utils import astra_command

@astra_command("exit")
async def exit_cmd(client, message):
    await message.reply("🚪 Astra exiting...")
    os._exit(0)
