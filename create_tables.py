from sqlmodel import SQLModel, Session
from models import User
from database import engine


print('Creating tables')
#  Base.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)

user1 = User(userid='ms', name='Markus Seeli', age=63, is_active=True)
user2 = User(userid='ls', name='Leon Seeli', age=20, is_active=True)
user3 = User(userid='mas', name='Maura Seeli', age=23, is_active=True)

with Session(engine) as session:
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
    print('Data inserted')
