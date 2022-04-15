from sqlalchemy import func, desc
from sqlalchemy.orm import Session
import models


def create_user_signup_entry(db: Session, user_details):
    db_user = models.User(username=user_details['username'],
                          fullstory_link=user_details['fullstory_link'],
                          mixpanel_link=user_details['mixpanel_link'],
                          primary_email=user_details['primary_email'],
                          other_email=user_details['other_email'],
                          events=user_details['events'],
                          msg_id=user_details['msg_id'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username,
        func.cardinality(models.User.events) < 10).first()


def update_user_signup_events(db: Session, username: str, events):
    user = db.query(
        models.User).filter(models.User.username == username).first()
    user.events = events
    db.commit()


def create_user_event(db: Session, event_details):
    db_event = models.Event(username=event_details['username'],
                            date=event_details['date'],
                            events=event_details['events'],
                            msg_id=event_details['msg_id'])
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_user_event_by_username(db: Session, username: str, date):
    return db.query(models.Event).filter(models.Event.username == username,
                                         models.Event.date == date).first()


def update_user_events(db: Session, username: str, msg_id: str, events):
    user_event = db.query(models.Event).filter(
        models.Event.username == username,
        models.Event.msg_id == msg_id).first()
    user_event.events = events
    db.commit()


def get_user_last_activity_date(db: Session, username: str):
    last_event_date = db.query(
        models.Event).filter(models.Event.username == username).order_by(
            desc(models.Event.date)).limit(1).first()
    if last_event_date:
        return last_event_date.date
    else:
        return last_event_date
