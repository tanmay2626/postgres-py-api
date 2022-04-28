from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config
import os


class Connection:
    engine = None
    session = None

    def init(self):
        self.engine = create_engine(config.postgres_url, echo=False)
        session_local = sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=self.engine)
        self.session = session_local()


connection = Connection()
