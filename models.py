# -*- coding: utf-8 -*-
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String
from datetime import datetime, date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    userid: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    age: Mapped[int] = mapped_column(default=20)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[date] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User(name={self.userid}, fullname={self.name}, age={self.age})>'