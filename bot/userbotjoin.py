import asyncio
from helpers.filters import command
from pyrogram import Client, filters
from config import BOT_USERNAME, SUDO_USERS
from pyrogram.errors import UserAlreadyParticipant
from helpers.decorators import authorized_users_only, errors

@Client.on_message(
    command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>• **i'm not have permission:**\n\n» ❌ __Add Users__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "🤖: i'm joined here for playing music on voice chat"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>✅ userbot already joined chat</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n User {user.first_name} couldn't join your group due to heavy join requests for userbot."
            "\n\nor manually add assistant to your Group and try again</b>",
        )
        return
    await message.reply_text(
        f"<b>✅ userbot successfully joined chat</b>",
    )


@Client.on_message(
    command(["userbotleave", f"userbotleave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot successfully left chat")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>user couldn't leave your group, may be floodwaits.\n\nor manually kick me from your group</b>"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **userbot** leaving all chats !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot leaving all group...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats.\nFailed {failed} chats."
    )
