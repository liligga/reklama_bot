from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from bot import db_engine


class Base(DeclarativeBase):
    pass


class Group(Base):
    """
    Чтобы можно было отдельно видеть группы
    """
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)

    postings: Mapped[list["Posting"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Group(id={self.id}, telegram_id={self.telegram_id})"


class Posting(Base):
    """
    Чтобы можно было отдельно видеть посты,
    последнее время поста в группу и тд
    """
    __tablename__ = "postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="postings")
    last_time: Mapped[datetime] = mapped_column(default=datetime.now())
    next_time: Mapped[datetime] = mapped_column(default=datetime.now())

    def __repr__(self):
        return f"Posting(id={self.id}, group_id={self.group_id}, last_time={self.last_time}, next_time={self.next_time})"


def init_db():
    Base.metadata.create_all(db_engine)

if __name__ == "__main__":
    init_db()
