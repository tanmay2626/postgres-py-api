from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.models import User, Event


def create_user_signup_entry(db: Session, user_details):
    db_user = User(username=user_details['username'],
                   fullstory_link=user_details['fullstory_link'],
                   mixpanel_link=user_details['mixpanel_link'],
                   primary_email=user_details['primary_email'],
                   other_email=user_details['other_email'],
                   events=user_details['events'],
                   msg_id=user_details['msg_id'],
                   timestamp = user_details['timestamp']
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username,
                                 func.cardinality(User.events) < 10).first()

def get_user_signup_date(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return "Not available"
    else:
        return user.timestamp.date().isoformat()

def update_user_signup_events(db: Session, username: str, events):
    user = db.query(User).filter(User.username == username).first()
    user.events = events
    db.commit()


def create_user_event(db: Session, event_details):
    db_event = Event(username=event_details['username'],
                     date=event_details['date'],
                     parent_event_count=event_details['parent_event_count'],
                     events=event_details['events'],
                     msg_id=event_details['msg_id'])
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_user_event_by_username(db: Session, username: str, date):
    return db.query(Event).filter(Event.username == username,
                                  Event.date == date).first()


def update_user_events(db: Session, event_details):
    user_event = db.query(Event).filter(
        Event.username == event_details['username'],
        Event.msg_id == event_details['msg_id']).first()
    user_event.events = event_details['events']
    db.commit()


def get_user_last_activity_date(db: Session, username: str):
    last_event_date = db.query(Event).filter(
        Event.username == username).order_by(desc(
            Event.date)).limit(1).first()
    if last_event_date:
        return last_event_date.date
    else:
        return last_event_date
