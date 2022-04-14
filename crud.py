from sqlalchemy import func
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
