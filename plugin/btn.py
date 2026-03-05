from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import astra_command

@astra_command("btn")
async def btn_handler(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🌐 Google", url="https://google.com")],
            [InlineKeyboardButton("⚡ Click Me", callback_data="astra_btn")]
        ]
    )

    await message.reply_text(
        "🔥 Astra Button Test",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("astra_btn"))
async def callback_handler(client, callback_query):
    await callback_query.answer("Button Clicked ✅", show_alert=True)
