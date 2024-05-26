from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f"sqlite:///products-phinder.db")
session_maker = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = session_maker()
    Base.metadata.create_all(engine)
    return db