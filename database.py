from sqlmodel import create_engine

engine = create_engine('sqlite:///data.db', echo=True)