import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from mongodb.users import Users
from main import DEVS

@Client.on_message(filters.command(["ping", "speed"]) & filters.private & filters.user(DEVS), group=12)
async def pong(_, message: Message):   
   start = datetime.datetime.now()
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await message.reply(f"**PONG:** {ms}ms")

@Client.on_message(filters.command(["stats", "stat", "users"]) & filters.private & filters.user(DEVS), group=14)
async def status(_, message: Message):   
   x = await message.reply("fetching stats....")
   await x.edit_text(f"**Total Users in bot:** `{Users.count()}`")

@Client.on_message(filters.command(["broadcast", "gcast"]) & filters.private & filters.user(DEVS), group=19)
async def gcast_(_, e: Message):
    txt = ' '.join(e.command[1:])
    if txt:
        msg = str(txt)
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
    else:
        await e.reply_text("Give Message for Broadcast or reply to any msg")
        return

    Han = await e.reply_text("Broadcasting...")
    err = 0
    dn = 0
    data = Users.get_all_users()
    for x in data:
       try:
          await arc.send_message(chat_id=x.user_id, text=msg)
          await asyncio.sleep(1)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")


@Client.on_message(filters.command(["fcast", "fmsg", "forward", "forwardmessage"]) & filters.user(DEVS), group=69)
async def forward_(_, e: Message):
    Siu = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 1)
    if len(Siu) == 2:
       from_chat = str(Siu[0])
       Msg_id = int(Siu[1])      
    else:
       await e.reply_text("Wrong Usage! \n\n Syntax: /forward (from chat id) (message id) \n\nNote: Must add bot in from message Channel!")
       return

    Han = await e.reply_text("forwarding...")
    err = 0
    dn = 0
    data = Users.get_all_users()
    for x in data:
       try:
          await arc.forward_messages(x.user_id, from_chat, message_ids=Msg_id)
          await asyncio.sleep(0.5)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
