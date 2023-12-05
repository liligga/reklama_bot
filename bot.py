import asyncio
from pyrogram.client import Client
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
groups = os.getenv('GROUPS')
app = Client('Arzybek', api_id=API_ID, api_hash=API_HASH)
db_engine = create_engine(os.getenv('SQLITE_DB_NAME'))
scheduler = AsyncIOScheduler(
    jobstores={'default': SQLAlchemyJobStore(engine=db_engine)}
)
