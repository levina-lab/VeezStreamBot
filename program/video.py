# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021


import os
import re
import asyncio
# repository stuff
from config import BOT_USERNAME, IMG_1, IMG_2, IMG_5
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.core import calls, user, bot
from driver.database.dbpunish import is_gbanned_user
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbqueue import add_active_chat, remove_active_chat, music_on
# pyrogram stuff
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message
# py-tgcalls stuff
from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
# youtube-dl stuff
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = data["thumbnails"][0]["url"]
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    user_xd = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if chat_id in await blacklisted_chats():
        await m.reply(
            "❗️ This chat has blacklisted by sudo user and You're not allowed to use me in this chat."
        )
        return await bot.leave_chat(chat_id)
    if await is_gbanned_user(user_id):
        await m.reply_text(f"❗️ {user_xd} **You've blocked from using this bot!**")
        return
    if m.sender_chat:
        return await m.reply_text(
            "you're an __Anonymous__ user !\n\n» revert back to your real user account to use this bot."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Delete messages__\n\nOnce done, try again."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Add users__\n\nOnce done, try again."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )
    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 downloading video...")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» only 720, 480, 360 allowed\n\n💡 now streaming video in **720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                    duration = convert_seconds(replied.video.duration)
                elif replied.document:
                    songname = replied.document.file_name[:70]
                    duration = convert_seconds(replied.document.duration)
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                await loser.edit("🔄 Queueing Track...")
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({link}) | `video`\n⏱️ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                )
                os.remove(image)
            else:
                await loser.edit("🔄 Joining Group Call...")
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await music_on(chat_id)
                await add_active_chat(chat_id)
                await calls.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🗂 **Name:** [{songname}]({link}) | `video`\n⏱️ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                )
                await idle()
                os.remove(image)
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» reply to an **video file** or **give something to search.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍 **Loading...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **no results found.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            await loser.edit("🔄 Queueing Track...")
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                            )
                            os.remove(image)
                        else:
                            try:
                                await loser.edit("🔄 Joining Group Call...")
                                await music_on(chat_id)
                                await add_active_chat(chat_id)
                                await calls.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                                )
                                await idle()
                                os.remove(image)
                            except Exception as ep:
                                await loser.delete()
                                await remove_active_chat(chat_id)
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an **video file** or **give something to search.**"
            )
        else:
            loser = await c.send_message(chat_id, "🔍 **Loading...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **no results found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        await loser.edit("🔄 Queueing Track...")
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                        )
                        os.remove(image)
                    else:
                        try:
                            await loser.edit("🔄 Joining Group Call...")
                            await music_on(chat_id)
                            await add_active_chat(chat_id)
                            await calls.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                            )
                            await idle()
                            os.remove(image)
                        except Exception as ep:
                            await loser.delete()
                            await remove_active_chat(chat_id)
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    user_xd = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if chat_id in await blacklisted_chats():
        await m.reply(
            "❗️ This chat has blacklisted by sudo user and You're not allowed to use me in this chat."
        )
        return await bot.leave_chat(chat_id)
    if await is_gbanned_user(user_id):
        await m.reply_text(f"❗️ {user_xd} **You've blocked from using this bot!**")
        return
    if m.sender_chat:
        return await m.reply_text(
            "you're an __Anonymous__ user !\n\n» revert back to your real user account to use this bot."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Delete messages__\n\nOnce done, try again."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Add users__\n\nOnce done, try again."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔍 **Loading...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» only 720, 480, 360 allowed\n\n💡 now streaming video in **720p**"
                )
            loser = await c.send_message(chat_id, "🔍 **Loading...**")
        else:
            await m.reply("`/vstream` {link} {720/480/360}")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                await loser.edit("🔄 Queueing Track...")
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 Joining Group Call...")
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await calls.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"💡 **[Video Live]({link}) stream started.**\n\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await remove_active_chat(chat_id)
                    await m.reply_text(f"🚫 error: `{ep}`")
