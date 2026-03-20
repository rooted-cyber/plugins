from transformers import pipeline
from . import *

chatbot = pipeline("text-generation", model="distilgpt2")

@astra_command("aii")
async def ai_cmd(client, message):
    text = message.text.split(maxsplit=1)

    if len(text) < 2:
        return await message.reply("Kuch pucho")

    prompt = text[1]

    result = chatbot(prompt, max_length=50, num_return_sequences=1)
    reply = result[0]["generated_text"]

    await message.reply(reply)
