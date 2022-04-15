from sqlalchemy import Column, Integer, String, ARRAY, DATE
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    fullstory_link = Column(String, nullable=True)
    mixpanel_link = Column(String, nullable=True)
    primary_email = Column(String, nullable=True)
    other_email = Column(ARRAY(String), nullable=True)
    events = Column(ARRAY(String), nullable=True)
    msg_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<User(id='%d, username='%s', fullstory_link='%s', mixpanel_link='%s, msg_id='%s')>" % (
            self.id, self.username, self.fullstory_link, self.mixpanel_link,
            self.msg_id)

    def toDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullstory_link': self.fullstory_link,
            'mixpanel_link': self.mixpanel_link,
            'primary_email': self.primary_email,
            'other_email': self.other_email,
            'events': self.events,
            'msg_id': self.msg_id,
        }


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE, nullable=False)
    username = Column(String, nullable=False)
    events = Column(ARRAY(String), nullable=False)
    msg_id = Column(String, unique=True)
