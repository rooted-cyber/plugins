#api link: https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/drive.readonly&response_type=token&client_id=407408718192.apps.googleusercontent.com&redirect_uri=https://developers.google.com/oauthplayground
from . import *
import requests

ACCESS_TOKEN = "ya29.a0Aa7MYiqNMSuFMfRu-Y0mNyeTBPw1Y_1iZLf4743xiQAT7UVPNs7hvKm5G7PhzntfEAZj238C1T4sJoh7Ujkb_IjhedDg2UZ-E2ekxwsDY73GVsIA8ENIbH5uTTN1tLGS73WuqMDERvkap1PJTlYLd-k5eToegdWFnd6lV5yWdoc18QaQ39Hh9W4k8sscgQJ8A4hiumUj83114aH-DSpbjAeSsxm8hzD4m2LQkhW6YM7CSn2sLJFD_R6lDLqnWBh5ibUUuo9G1j5VLPo_XfAYQK2dTtcz_gaCgYKAaUSARUSFQHGX2MiZiqugU-X2DCzuj5NDx2Cvw0293"

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
