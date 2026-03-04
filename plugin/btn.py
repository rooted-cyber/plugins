from . import *
import os

@astra_command(name="btn")
async def whtsp_bot(client, message):

    await message.reply("⚙ Creating WhatsApp bot...")

    code = """
const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys")

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState("session")

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    })

    sock.ev.on("creds.update", saveCreds)

    sock.ev.on("messages.upsert", async ({ messages }) => {
        const msg = messages[0]
        if (!msg.message) return

        const text = msg.message.conversation

        if (text === ".menu") {
            await sock.sendMessage(msg.key.remoteJid, {
                text: "Choose option 👇",
                footer: "Astra Bot",
                buttons: [
                    { buttonId: "owner", buttonText: { displayText: "👑 Owner" }, type: 1 },
                    { buttonId: "help", buttonText: { displayText: "📜 Help" }, type: 1 }
                ],
                headerType: 1
            })
        }
    })
}

startBot()
"""

    # Create folder
    os.makedirs("whtsp_bot", exist_ok=True)

    # Write JS file
    with open("whtsp_bot/index.js", "w") as f:
        f.write(code)

    # Install dependency
    #os.system("cd whtsp_bot && npm init -y")
    #.system("cd whtsp_bot && npm install @whiskeysockets/baileys")

    await message.reply("🚀 Starting WhatsApp bot... Scan QR in terminal.")

    # Run bot
    os.system("cd whtsp_bot && node index.js")
