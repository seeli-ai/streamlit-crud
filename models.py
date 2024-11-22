# -*- coding: utf-8 -*-
from sqlmodel import SQLModel, Field
from datetime import datetime, date


class User(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    userid: str
    name: str | None = None
    age: int = 20
    is_active: bool = True
    created_at: datetime = datetime.now()

    def __repr__(self):
        return f'<User(name={self.userid}, fullname={self.name}, age={self.age})>'