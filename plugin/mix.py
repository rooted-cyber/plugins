import base64
import os
from astra import Client, Message
from . import astra_command


@astra_command(
    name="mix",
    description="Encode / decode text (base64, hex, random mix).",
    usage=".mix <text>",
    category="Tools",
)
async def mix_cmd(client: Client, message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        return await message.reply("Usage: `.mix text`")

    text = args[1]

    try:
        b64 = base64.b64encode(text.encode()).decode()
        b64d = base64.b64decode(b64).decode()
        hexv = text.encode().hex()
        rnd = os.urandom(16).hex()

        msg = f"""
🔀 **Mix Result**

**Text:** `{text}`

**Base64 Encode:**  
`{b64}`

**Base64 Decode:**  
`{b64d}`

**Hex:**  
`{hexv}`

**Random Mix:**  
`{rnd}`
"""
        await message.reply(msg)

    except Exception as e:
        await message.reply(f"Error: {e}")
