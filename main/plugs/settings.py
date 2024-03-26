from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from mongodb import protect_value, channel_button_value
from main import DEVS

@Client.on_callback_query()
async def handle_callback_query(client: Client, query: CallbackQuery):
    data = query.data

    if data == "protect":
        text = "Protect Content Settings."
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Enable", callback_data="enable")],
                [InlineKeyboardButton("Disable", callback_data="disable")]
            ]
        )
        await query.answer(text)
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    elif data == "enable":
        protect_value.update_one({}, {"$set": {"protect_content": True}}, upsert=True)
        await query.answer("Content protection enabled!")
        await query.edit_message_text("Content protection enabled!")

    elif data == "disable":
        protect_value.update_one({}, {"$set": {"protect_content": False}}, upsert=True)
        await query.answer("Content protection disabled!")
        await query.edit_message_text("Content protection disabled!")            
        
    elif data == "channel":
        text = "Channel Button Settings."
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Off", callback_data="off")],
                [InlineKeyboardButton("On", callback_data="on")]
            ]
        )
        await query.answer(text)
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    elif data == "on":
        channel_button_value.update_one({}, {"$set": {"channel_button": True}}, upsert=True)
        await query.answer("On!")
        await query.edit_message_text("Channel Button Is Now On.")
        
    elif data == "off":
        channel_button_value.update_one({}, {"$set": {"channel_button": False}}, upsert=True)
        await query.answer("Off!")
        await query.edit_message_text("Channel Button Is Now Off.")


@Client.on_message(filters.command("settings", prefixes="/") & filters.user(DEVS))
async def protect_content(client: Client, message: Message):
    protect_content_value = protect_value.find_one({})["protect_content"]
    disable_channel_button = channel_button_value.find_one({})["channel_button"]
    
    text = "Bot Settings👇"
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Protect Content", callback_data="protect")],
            [InlineKeyboardButton("Channel Button", callback_data="channel")]
        ]
    )
    await message.reply(text, reply_markup=reply_markup)
