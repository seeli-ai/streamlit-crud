from models import Base, User
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from database import engine
from datetime import datetime
import streamlit as st

Session = sessionmaker(bind=engine)


def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# User

# Read


def get_user_by_id(user_id: int, session = None) -> User:
    if session is None:
        session = next(get_db_session())
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_userid(userid: str, session = None) -> User:
    if session is None:
        session = next(get_db_session())
    return session.query(User).filter(User.userid == userid).first()


def get_all_users(session = None) -> List[User]:
    if session is None:
        session = next(get_db_session())
    return session.query(User).all()

# Create

def create_empty_user(session = None) -> User:
    new_user = create_user(userid="new", name="new User", session=session)

    return new_user

def create_user(userid: str, name: str, age: int=20, is_active: bool = True, session = None) -> User:
    if session is None:
        session = next(get_db_session())
    new_user = User(userid=userid, name=name,
                    age=age, is_active=is_active)
    session.add(new_user)
    session.commit()
    return new_user

# Update


def update_user(user_id: int, session = None, **kwargs) -> User:
    if session is None:
        session = next(get_db_session())
    user = get_user_by_id(user_id, session=session)
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()
    return user

# Delete


def delete_user(user_id: int, session = None) -> User:
    if session is None:
        session = next(get_db_session())
    user = get_user_by_id(user_id, session=session)
    session.delete(user)
    session.commit()
    return user