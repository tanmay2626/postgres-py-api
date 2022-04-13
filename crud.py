from sqlalchemy import func
from sqlalchemy.orm import Session
import models

def create_user_signup_entry(db: Session, userDetails):
    db_user = models.User(
        username=userDetails['username'], 
        fullstory_link=userDetails['fullstory_link'], 
        mixpanel_link=userDetails['mixpanel_link'], 
        events = userDetails['events'],
        msg_id = userDetails['msg_id'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username, func.cardinality(models.User.events) < 10).first()

def update_user_signup_events(db: Session, username: str, events ):
    user = db.query(models.User).filter(models.User.username == username).first()
    user.events = events
    db.commit()