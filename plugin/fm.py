from . import *

@astra_cmd("fm")
async def fm(client, message):
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a user")

    user = message.reply_to_message.from_user

    first = user.first_name or "None"
    last = user.last_name or "None"
    username = f"@{user.username}" if user.username else "None"
    uid = user.id

    text = f"""
👤 **User Info**

First Name: {first}
Last Name: {last}
Username: {username}
ID: `{uid}`
"""

    await message.reply(text)
