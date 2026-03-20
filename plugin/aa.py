import google.generativeai as genai
from . import *

API_KEY = "AIzaSyB_qKhQviCuH5qxKUvhP6fc8b9rrPRE6yc"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")

@astra_command("aa")
async def ai_cmd(client, message):
    text = message.text.split(maxsplit=1)

    if len(text) < 2:
        return await message.reply("Kuch pucho bro")

    query = text[1]

    try:
        import asyncio

        response = await asyncio.to_thread(model.generate_content, query)
        #response = model.generate_content(query)
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    await message.reply(reply)
