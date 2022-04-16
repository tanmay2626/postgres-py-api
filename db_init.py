from app.database import engine
from app.models import *

Base.metadata.create_all(bind=engine)