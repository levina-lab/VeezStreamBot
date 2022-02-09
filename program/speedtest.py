# credit to TeamYukki for this speedtest module

import os
import wget
import speedtest

from program.utils.formatters import bytes
from driver.filters import command, other_filters
from driver.decorators import sudo_users_only
from config import BOT_USERNAME as bname
from driver.veez import bot as app
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["speedtest", f"speedtest@{bname}"]) & ~filters.edited)
@sudo_users_only
async def run_speedtest(_, message: Message):
    m = await message.reply_text("⚡️ running server speedtest")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("⚡️ running download speedtest..")
        test.download()
        m = await m.edit("⚡️ running upload speedtest...")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit(e)
        return
    m = await m.edit("🔄 sharing speedtest results")
    path = wget.download(result["share"])

    output = f"""💡 **SpeedTest Results**
    
<u>**Client:**</u>
**ISP:** {result['client']['isp']}
**Country:** {result['client']['country']}
  
<u>**Server:**</u>
**Name:** {result['server']['name']}
**Country:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Latency:** {result['server']['latency']}

⚡️ **Ping:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
