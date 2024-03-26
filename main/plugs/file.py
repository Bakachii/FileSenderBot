import re
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.enums import ParseMode
from main import DEVS, CHANNEL, BOT_USERNAME, encode, gplinks 
from main.funcs import get_message_id 
from mongodb.users import Users   

@Client.on_message(filters.private & filters.user(DEVS)) ~filters.regex('^/'))
async def channel_post(client: Client, message: Message):
    if message.text.startswith("/"):
        return
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    base64_string = await encode(f"{BOT_USERNAME}-{post_message.id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    gplink = gplinks(link)
    reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Direct Link", url=link),
                    InlineKeyboardButton("Gplink", url=gplink)
                ]
            ]
    )
    await reply_text.edit_text(f"• Encoded links\n﹂Link:\n`{link}`\n﹂GpLink:\n`{gplink}`", reply_markup=reply_markup)


@Client.on_message(filters.private & filters.command("batch") & filters.user(DEVS), group=20)
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quote) or Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("This Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quote) or Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("This Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue
     
    string = f"{BOT_USERNAME}-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    gplink = gplinks(link)
    reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Direct Link", url=link),
                    InlineKeyboardButton("Gplink", url=gplink)
                ]
            ]
    )
    await second_message.reply_text(f"• Encoded links\n﹂Link:\n`{link}`\n﹂GpLink:\n`{gplink}`", quote=True, reply_markup=reply_markup)

@Client.on_message(filters.private & filters.user(DEVS) & filters.command("link"), group=18)    
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue
    
    base64_string = await encode(f"{BOT_USERNAME}-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    gplink = gplinks(link)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Direct Link", url=link),
                InlineKeyboardButton("Gplink", url=gplink)
            ]
        ] 
    )
    await message.edit_text(f"• Encoded links\n﹂Link:\n`{link}`\n﹂GpLink:\n`{gplink}`", reply_markup=reply_markup)
