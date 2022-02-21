import re
import sys
import subprocess
import traceback

from time import time
from io import StringIO
from inspect import getfullargspec

from config import BOT_USERNAME as bname
from driver.core import bot
from driver.filters import command
from pyrogram import Client, filters
from driver.database.dbchat import remove_served_chat
from driver.decorators import bot_creator, sudo_users_only, errors
from driver.utils import remove_if_exists
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@Client.on_message(command(["eval", f"eval{bname}"]) & ~filters.edited)
@sudo_users_only
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="» Give a command to execute")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "SUCCESS"
    final_output = f"`OUTPUT:`\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳", callback_data=f"runtime {t2-t1} seconds"
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"`INPUT:`\n`{cmd[0:980]}`\n\n`OUTPUT:`\n`attached document`",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        remove_if_exists(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} seconds",
                    )
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@Client.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@Client.on_message(command(["sh", f"sh{bname}"]) & ~filters.edited)
@sudo_users_only
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**usage:**\n\n» /sh echo hello world")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(message, text=f"`ERROR:`\n\n```{err}```")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"`ERROR:`\n\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await bot.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`OUTPUT`",
            )
            return remove_if_exists("output.txt")
        await edit_or_reply(message, text=f"`OUTPUT:`\n\n```{output}```")
    else:
        await edit_or_reply(message, text="`OUTPUT:`\n\n`no output`")


@Client.on_message(command(["leavebot", f"leavebot{bname}"]) & ~filters.edited)
@bot_creator
async def bot_leave_group(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**usage:**\n\n» /leavebot [chat id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await bot.leave_chat(chat)
        await remove_served_chat(chat)
    except Exception as e:
        await message.reply_text(f"❌ procces failed\n\nreason: `{e}`")
        print(e)
        return
    await message.reply_text(f"✅ Bot successfully left from the Group:\n\n💭 » `{chat}`")
