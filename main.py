from bot import app, groups, scheduler, db_engine
from pyrogram.enums import ChatType
from pyrogram import idle
import logging
from db import init_db, Group, Posting
from sqlalchemy.orm import Session
from sqlalchemy import update, text
from datetime import datetime, timedelta


async def get_my_groups():
    async with app:
        async for dialog in app.get_dialogs():
            if (
                dialog.chat.type == ChatType.GROUP
                or dialog.chat.type == ChatType.SUPERGROUP
            ):
                print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)


def schedule_posting(p: Posting):
    id = str(p.id)
    if scheduler.get_job(id):
        scheduler.remove_job(id)

    scheduler.add_job(send_posting, "date", run_date=p.next_time, args=[p.id], id=id)


async def send_posting(post_id: int):
    try:
        with Session(db_engine) as session:
            p = session.query(Posting).filter(Posting.id == post_id).first()
            await app.send_message(p.group.telegram_id, "Hello world!")
            now = datetime.now()
            new_dates = (
                update(Posting)
                .where(Posting.id == p.id)
                .values(last_time=now, next_time=now + timedelta(seconds=15))
            )
            session.execute(new_dates)
        schedule_posting(p)
    except Exception as e:
        logging.error(e)


async def main():
    # initialize DB
    init_db()

    # start bot
    await app.start()

    # schedule Posts to groups
    with Session(db_engine) as session:
        # res = session.execute(text("SELECT * FROM postings"))
        # print(res.all())
        _groups = groups.replace("[", "").replace("]", "").split(", ")
        group1 = (
            session.query(Group)
            .filter(Group.telegram_id == _groups[0]).first()
        )
        if not group1:
            group1 = Group(telegram_id=_groups[0])
            session.add(group1)
            group2 = Group(telegram_id=_groups[1])
            session.add(group2)
            posting1 = Posting(
                group=group1, next_time=datetime.now() + timedelta(seconds=20)
            )
            session.add(posting1)
            posting2 = Posting(
                group=group2, next_time=datetime.now() + timedelta(seconds=35)
            )
            session.add(posting2)
            session.commit()
            postings = (posting1, posting2)
        else:
            postings = (
                session.query(Posting)
                .filter(Posting.group_id.in_(_groups))
                .all()
            )
            for p in postings:
                p.next_time = datetime.now() + timedelta(minutes=1)
                session.merge(p)

            session.commit()
        for posting in postings:
            schedule_posting(posting)

        res = session.execute(text("SELECT * FROM groups"))
        print(res.all())

    await idle()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    app.run(main())
