from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class Connection:
    engine = None
    session = None

    def init(self):
        postgres_url = os.getenv('POSTGRES_URL')
        self.engine = create_engine(postgres_url, echo=False)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = session_local()

connection = Connection()