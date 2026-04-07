from . import *
import requests

ACCESS_TOKEN = "ya29.a0Aa7MYiok_dPG2fyYQRzyE3PCy92LpsGG-wMn8vQSNBFiT3F_WdK_1TkWGjPi8ZH1DCwSGb6kouuJCF57m9Du1mW-9Ozjj1z8JLMl0bGjh_jWcYGPMoOl-KKJQjDc_j3C-ihEreTdxQ7-IF657mbyqVzknOfTUX67zsd4YSCIr7gmMl4wz-T2VwAEkaBR_utI1NHWWWMaCgYKAcASARUSFQHGX2MiJTkBfDy6fBodcb0TTKLePA0206"

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
