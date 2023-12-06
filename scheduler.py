from bot import scheduler, session, app
from db import Group, Posting
import logging
from datetime import datetime, timedelta


def schedule_posting(p: Posting):
    id = str(p.id)
    if scheduler.get_job(id):
        scheduler.remove_job(id)

    scheduler.add_job(send_posting, "date", run_date=p.next_time, args=[p.id], id=id)


async def send_posting(post_id: int):
    try:
        post = Posting.query.filter(Posting.id == post_id).first()
        await app.send_message(post.group.telegram_id, "Hello world!")
        now = datetime.now()
        post.next_time = now + timedelta(seconds=15)
        # post.update({"last_time": now, "next_time": now + timedelta(seconds=15)})
        session.commit()
        schedule_posting(post)
    except Exception as e:
        logging.error(e)
