import asyncio
from pyrogram.client import Client
from dotenv import load_dotenv
import os


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
app = Client('Arzybek', api_id=API_ID, api_hash=API_HASH)