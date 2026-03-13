import os
import asyncio
from astra import Client, Message
from . import astra_command


@astra_command(
    name="up",
    description="Upload large file to Telegram",
    category="Tools",
    usage=".upload /path/file",
    is_public=True
)
async def upload_cmd(client: Client, message: Message):

    args = message.text.split(maxsplit=1)

    # reply file upload
    if message.reply_to_message and message.reply_to_message.document:

        status = await message.reply("⬇ Downloading file...")

        file_path = await message.reply_to_message.download()

        await status.edit("⬆ Uploading...")

        await client.send_document(
            message.chat.id,
            file_path,
            reply_to_message_id=message.id
        )

        os.remove(file_path)

        await status.edit("✅ Upload complete")
        return

    # path upload
    if len(args) > 1:
        path = args[1]

        if not os.path.exists(path):
            await message.reply("❌ File not found")
            return

        status = await message.reply("⬆ Uploading file...")

        await client.send_document(
            message.chat.id,
            path,
            reply_to_message_id=message.id
        )

        await status.edit("✅ Upload complete")
        return

    await message.reply("❌ Reply to file ya path do")