from . import *
import requests

ACCESS_TOKEN = "PASTE_YOUR_TOKEN_HERE"

def get_files(folder_id):
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"'{folder_id}' in parents",
        "fields": "files(id,name,mimeType,size)"
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    res = requests.get(url, params=params, headers=headers)
    return res.json().get("files", [])

def get_size(folder_id):
    total = 0
    files = get_files(folder_id)

    for f in files:
        if f["mimeType"] == "application/vnd.google-apps.folder":
            total += get_size(f["id"])
        else:
            total += int(f.get("size", 0))

    return total

@astra_command(name="gsize")
async def gsize_cmd(client, message):
    msg = await message.reply("📦 Calculating Google Drive size...")

    try:
        total = get_size("root")
        gb = total / (1024**3)

        await msg.edit(f"💾 Total Drive Size: {gb:.2f} GB")

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{e}`")
