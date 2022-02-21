from typing import List
from pyrogram.types import Chat
from cache.admins import get as gett, set

async def get_administrators(chat: Chat) -> List[int]:
    get = gett(chat.id)

    if get:
        return get
    administrators = await chat.get_members(filter="administrators")
    to_set = []

    for administrator in administrators:
        if administrator.can_manage_voice_chats:
            to_set.append(administrator.user.id)

    set(chat.id, to_set)
    return await get_administrators(chat)
