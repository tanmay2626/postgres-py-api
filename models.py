from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    fullstory_link = Column(String, nullable=True)
    mixpanel_link = Column(String, nullable=True)
    events = Column(ARRAY(String), nullable=True)
    msg_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<User(id='%d, username='%s', fullstory_link='%s', mixpanel_link='%s, msg_id='%s')>" % (
            self.id, self.username, self.fullstory_link, self.mixpanel_link,
            self.msg_id)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True))
    username = Column(String, unique=True, nullable=False)
    events = Column(ARRAY(String))
    msg_id = Column(String, unique=True)
