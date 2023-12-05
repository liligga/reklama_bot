
def create_group(telegram_id):
    with Session(db_engine) as session:
        existing_group = session.query(Group).filter(Group.telegram_id == telegram_id).first()
        if not existing_group:
            new_group = Group(telegram_id=telegram_id)
            session.add(new_group)
            session.commit()

def create_posting(group_id):
    with Session(db_engine) as session:
        existing_group = session.query(Group).filter(Group.id == group_id).first()
        if not existing_group:
            new_group = Group(id=group_id)
            session.add(new_group)
            session.commit()