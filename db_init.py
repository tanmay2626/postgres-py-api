from dotenv import load_dotenv
from app.models import Base
from app.database import connection

load_dotenv('.env.stage')
connection.init()
Base.metadata.create_all(bind=connection.engine)
