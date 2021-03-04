from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import config


database_url = config.DATABASE_URL
connect_args = {"check_same_thread": False} if config.DEFAULT_DATABASE_URL == config.DATABASE_URL else None
engine = create_engine(database_url, connect_args={"check_same_thread": False})  # connect args for sqlite3

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
