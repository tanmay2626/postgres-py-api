from app.models import Base
from app.database import connection

connection.init()
Base.metadata.create_all(bind=connection.engine)
