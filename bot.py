import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pyrogram.client import Client
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
groups = os.getenv('GROUPS')
app = Client('Arzybek', api_id=API_ID, api_hash=API_HASH)
db_engine = create_engine(os.getenv('SQLITE_DB_NAME'))
scheduler = AsyncIOScheduler(
    jobstores={'default': SQLAlchemyJobStore(engine=db_engine)}
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
