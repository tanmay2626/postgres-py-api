from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

postgres_url = os.getenv('POSTGRES_URL')

engine = create_engine(postgres_url, echo=False)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = session_local()
Base = declarative_base()
