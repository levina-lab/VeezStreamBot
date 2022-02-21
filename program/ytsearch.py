from config import BOT_USERNAME
from driver.decorators import check_blacklist
from driver.filters import command
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch


@Client.on_message(command(["search", f"search@{BOT_USERNAME}"]))
@check_blacklist()
async def ytsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("/search **needs an argument !**")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🔎 **Searching...**")
    results = YoutubeSearch(query, max_results=5).to_dict()
    text = ""
    for i in range(5):
        try:
            text += f"🏷 **Name:** __{results[i]['title']}__\n"
            text += f"⏱ **Duration:** `{results[i]['duration']}`\n"
            text += f"👀 **Views:** `{results[i]['views']}`\n"
            text += f"📣 **Channel:** {results[i]['channel']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
        except IndexError:
            break
    await m.edit_text(
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗑 Close", callback_data="close_panel")]]
        ),
    )
