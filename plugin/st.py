import base64
from pyrogram import Client
from pyrogram.types import Message

@astra_command(
    name="sticker",
    description="Convert an image or video to a sticker.",
    category="Tools & Utilities",
    aliases=["s", "stkr"],
    usage="(reply to image/video)",
    is_public=True,
)
async def sticker_handler(client: Client, message: Message):
    """Sticker creation plugin."""

    reply = message.reply_to_message

    if not reply and not message.media:
        return await edit_or_reply(
            message,
            f"{UI.mono('[ ERROR ]')} Reply to an image/video."
        )

    status_msg = await edit_or_reply(
        message,
        f"{UI.mono('[ BUSY ]')} Converting to sticker..."
    )

    target = reply if reply else message

    # download media
    file_path = await client.download_media(target)

    if not file_path:
        return await status_msg.edit("❌ Failed to download media.")

    # send sticker
    await client.send_sticker(
        message.chat.id,
        file_path,
        reply_to_message_id=message.id
    )

    await status_msg.delete()
