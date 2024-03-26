import os
import sys
import base64
import requests
import logging
import pyromod.listen
from pyrogram.enums import ParseMode
from datetime import datetime
from config import vars, keys, db
from pyrogram import Client

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string   

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    try:
        DEVS = {int(x) for x in os.environ.get("DEVS", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    FILE_CAPTION = os.environ.get("FILE_CAPTION", None)
    DB_URL = os.get_environ.get("DB_URL", None)
    CHANNEL = os.get_environ.get("CHANNEL", None)
    CHANNEL_NAME = os.get_environ.get("CHANNEL_NAME", None)
    DB_CHANNEL = os.get_environ.get("DB_CHANNEL", None)
    START_MSG = os.get_environ.get("START_MSG", None)
    START_PIC = os.get_environ.get("START_PIC", None)
    API_ID = os.get_environ.get("API_ID", None)
    API_HASH = os.get_environ.get("API_HASH", None)
    shortner_api = os.get_environ.get("shortner_api", None)
else:
    try:        
        OWNER_ID = int(vars.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")
    try: 
        DEVS = {int(x) for x in vars.DEV_USERS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")
    
    FILE_CAPTION = vars.FILE_CAPTION
    BOT_USERNAME = vars.BOT_USERNAME
    DB_URL = db.DB_URL
    CHANNEL = vars.CHANNEL
    CHANNEL_NAME = vars.CHANNEL_NAME
    DB_CHANNEL = vars.DB_CHANNEL
    START_MSG = vars.START_MSG
    START_PIC = vars.START_PIC
    API_ID = vars.API_ID
    API_HASH = vars.API_HASH
    TOKEN = vars.TOKEN
    shortner_api = keys.shortner_api

DEVS.append(OWNER_ID)

def gplinks(query):
    x = requests.get(f'https://gplinks.in/api?api={shortner_api}&url={query}', headers=keys.s_header).json()
    if x.get('status') == 'success':
        return x.get('shortenedUrl')              
        
ENV = bool(os.environ.get("ENV", False))
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler(f"{BOT_USERNAME}.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

def log(name: str) -> logging.Logger:
    return logging.getLogger(name)
    
class arc(Client):
    def __init__(self):
        super().__init__(
            name="File-Bot",
            api_hash=API_HASH,
            api_id=API_ID,            
            bot_token=TOKEN,
            plugins=dict(root="main.plugs")
        )
        self.log = log

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        try:
            db_channel = await self.get_chat(DB_CHANNEL)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Connected to Database Channel✅")        
        except Exception as e:
            self.log(__name__).warning(e)
            self.log(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the DB channel id Value, Current Value {DB_CHANNEL}")
            sys.exit()

        self.set_parse_mode(ParseMode.MARKDOWN)
        self.log(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/UnchainedCodes")
        self.log(__name__).info("Running...")
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.log(__name__).info("Bot stopped.")
