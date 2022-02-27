""" inline section button """

from pyrogram.types import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)


def stream_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="𓆩👑❛ 𝗩ᴊɪɪ", url=f"https://t.me/vjii_world"),
      InlineKeyboardButton(text="𝐖ᴏʀʟᴅ᭄ ❜👑𓆪⁩", url=f"https://t.me/vjii_world"),
    ],
  ]
  return buttons


def menu_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="⏹", callback_data=f'set_stop | {user_id}'),
      InlineKeyboardButton(text="⏸", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="▶️", callback_data=f'set_resume | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔇", callback_data=f'set_mute | {user_id}'),
      InlineKeyboardButton(text="🔊", callback_data=f'set_unmute | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔙 Go Back", callback_data='stream_home_panel'),
    ]
  ]
  return buttons


close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🗑 Close", callback_data="set_close"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🔙 Go Back", callback_data="stream_menu_panel"
      )
    ]
  ]
)
