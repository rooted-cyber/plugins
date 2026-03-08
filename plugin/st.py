from . import *
import base64
from pyrogram import Client
from pyrogram.types import Message

@astra_command(
    name="sticker",
    description="Convert an image or video to a sticker.",
    category="Tools & Utilities",
    aliases=["st", "stkr"],
    usage="(reply to image/video)",
    is_public=True,
)
async def sticker_handler(client: Client, message: Message):

    reply = await message.get_reply_message()

    if not reply and not message.media:
        return await edit_or_reply(
            message,
            f"{UI.mono('[ ERROR ]')} Reply to an image/video."
        )

    status = await edit_or_reply(
        message,
        f"{UI.mono('[ BUSY ]')} Converting to sticker..."
    )

    target = reply if reply else message

    file_path = await client.download_media(target)

    if not file_path:
        return await status.edit("❌ Failed to download media.")

    await client.send_sticker(
        message.chat.id,
        file_path,
        reply_to_message_id=message.id
    )

    await status.delete()