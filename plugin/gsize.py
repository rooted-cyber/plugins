from . import *
import requests

ACCESS_TOKEN = "ya29.a0Aa7MYiok_dPG2fyYQRzyE3PCy92LpsGG-wMn8vQSNBFiT3F_WdK_1TkWGjPi8ZH1DCwSGb6kouuJCF57m9Du1mW-9Ozjj1z8JLMl0bGjh_jWcYGPMoOl-KKJQjDc_j3C-ihEreTdxQ7-IF657mbyqVzknOfTUX67zsd4YSCIr7gmMl4wz-T2VwAEkaBR_utI1NHWWWMaCgYKAcASARUSFQHGX2MiJTkBfDy6fBodcb0TTKLePA0206"


def get_files(folder_id):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    files = []
    page_token = None

    while True:
        params = {
            "q": f"'{folder_id}' in parents and trashed=false",
            "fields": "nextPageToken, files(id,name,mimeType,size)",
            "pageSize": 1000
        }

        if page_token:
            params["pageToken"] = page_token

        res = requests.get(url, params=params, headers=headers)
        data = res.json()

        # ❗ Debug error check
        if "error" in data:
            print(data)
            return []

        files.extend(data.get("files", []))
        page_token = data.get("nextPageToken")

        if not page_token:
            break

    return files

def get_size(folder_id, level=0):
    total = 0
    output = ""

    files = get_files(folder_id)

    for f in files:
        if f["mimeType"] == "application/vnd.google-apps.folder":
            size, text = get_size(f["id"], level + 1)
            total += size
            output += "  " * level + f"📁 {f['name']} → {size/1024**3:.2f} GB\n" + text
        else:
            total += int(f.get("size", 0))

    return total, output

@astra_command(name="gsize")
async def gsize_cmd(client, message):
    msg = await message.reply("📦 Calculating Google Drive size...")

    try:
        total, details = get_size("root")
        gb = total / (1024**3)

        text = f"💾 Total Drive Size: {gb:.2f} GB\n\n"
        text += "📊 Folder Breakdown:\n\n"
        text += details[:4000]

        await msg.edit(text)

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{e}`")