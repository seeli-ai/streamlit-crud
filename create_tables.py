from models import Base
from database import engine
from repository import create_user


print('Creating tables')
#  Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

create_user('ms', 'Markus Seeli', 63, True)
create_user('ls', 'Leon Seeli', 20, True)
create_user('mas', 'Maura Seeli', 23, True)