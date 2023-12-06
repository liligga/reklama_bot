import logging
from datetime import datetime, timedelta

from pyrogram import idle
from pyrogram.enums import ChatType

from bot import app, groups, scheduler, session
from db import Group, Posting, init_db
from scheduler import schedule_posting


async def get_my_groups():
    async with app:
        async for dialog in app.get_dialogs():
            if (
                dialog.chat.type == ChatType.GROUP
                or dialog.chat.type == ChatType.SUPERGROUP
            ):
                print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)



async def main():
    # initialize DB
    init_db()

    # start bot
    await app.start()
    _groups = groups.replace("[", "").replace("]", "").split(", ")
    if not Group.query.first():
        for gr in _groups:
            session.add(Group(telegram_id=gr))
        session.commit()
        for gr in Group.query.all():
            posting = Posting(
                group=gr,
                next_time=datetime.now() + timedelta(seconds=15),
            )
            session.add(posting)
        session.commit()
        postings = Posting.query.all()
    else:
        postings = Posting.query.filter(Posting.group_id.in_(_groups)).all()
        for p in postings:
            p.next_time = datetime.now() + timedelta(minutes=1)
            session.merge(p)

        session.commit()
    for posting in postings:
        schedule_posting(posting)

    await idle()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    app.run(main())
