from models import User
from sqlmodel import Session, select
from typing import List
from database import engine


def get_db_session():
    session = Session(engine)
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
    return session.get(User, user_id)


def get_user_by_userid(userid: str, session = None) -> User:
    if session is None:
        session = next(get_db_session())
    return session.exec(select(User).where(User.userid == userid)).first()


def get_all_users(session = None) -> List[User]:
    if session is None:
        session = next(get_db_session())
    return session.exec(select(User)).all()

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
    session.refresh(new_user)
    return new_user

# Update


def update_user(user_id: int, session = None, **kwargs) -> User:
    if session is None:
        session = next(get_db_session())
    user = get_user_by_id(user_id, session=session)
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Delete


def delete_user(user_id: int, session = None) -> None:
    if session is None:
        session = next(get_db_session())
    user = get_user_by_id(user_id, session=session)
    session.delete(user)
    session.commit()
    return None