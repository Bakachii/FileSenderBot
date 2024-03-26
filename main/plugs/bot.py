import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden, FloodWait
from pyrogram.enums import ChatMemberStatus, ParseMode
from mongodb.users import Users
from mongodb import protect_value, channel_button_value
from main import DEVS, CHANNEL, CHANNEL_NAME, BOT_USERNAME, START_MSG, START_PIC, FILE_CAPTION, DB_CHANNEL, decode
from main.funcs import get_messages, get_message_id

protect_content_value = protect_value.find_one({})["protect_content"]
disable_channel_button = channel_button_value.find_one({})["channel_button"]

CHANNEL_BUTTON = [[(InlineKeyboardButton(f"{CHANNEL_NAME}", url=f"https://t.me/{CHANNEL}"))]]

async def check_sub(Client, update):
    if not CHANNEL:
        return True
    user_id = update.from_user.id
    if user_id in DEVS:
        return True
    try:
        member = await Client.get_chat_member(CHANNEL, user_id=user_id)
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        print(f"I'm not admin in the CHANNEL chat : {CHANNEL} !")
        return True
    except ChatWriteForbidden:
        return True

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def join_message(client: Client, message: Message):
    if len(message.text)>7:
      buttons = [
                [
                 InlineKeyboardButton(f"{CHANNEL_NAME}", url=f"https://t.me/{CHANNEL}")
                ], [
                 InlineKeyboardButton("- Try Again -",url = f"https://t.me/{BOT_USERNAME}?start={message.command[1]}")
                ], ]
    else:
      buttons = CHANNEL_BUTTON

    await message.reply(
        f"You must join [this channel](https://t.me/{CHANNEL}) to use me. After joining try again !",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channels(client: Client, message: Message):   
    if not CHANNEL:
        return
    text = message.text
    if text is None:
        return
    if re.search("start".lower(), text.lower()):
      return
    if not await check_sub(client, message):
      await message.reply(
        f"You must join [this channel](https://t.me/{CHANNEL}) to use me. After joining try again !",
        reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON),
        quote=True,
        disable_web_page_preview=True
      )
      await message.stop_propagation()
        
@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    chat = message.chat
    user = message.from_user
    Users.adduser(user.id)
    text = message.text
    if await check_sub(client, message):
        pass
    else:
        await join_message(client, message)
        return

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            decoded_string = await decode(base64_string)
            argument = decoded_string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start,end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()
            for msg in messages:
                if bool(FILE_CAPTION) & bool(msg.document):
                    caption = FILE_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    sent_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=protect_content_value)
                    await asyncio.sleep(80)  # Wait for 1:20 minute
                    await sent_msg.delete()  # Delete the sent message
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    sent_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=protect_content_value)
                    await asyncio.sleep(80)  # Wait for 1:20 minute 
                    await sent_msg.delete()  # Delete the sent message
                except Exception as e:
                    print("Error in processing start command:", str(e))
        except Exception as e:
            print("Error in processing start command:", str(e))
    else:
        await client.send_photo(message.chat.id, START_PIC, caption=START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON))
