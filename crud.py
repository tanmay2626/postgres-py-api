from sqlalchemy import func
from sqlalchemy.orm import Session
import models

# get_parent_event_msg
# update_parent_event_msg
# create_parent_event_msg

# create_signup_event
# get_signup_event
# update_signup_event

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

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
    return

# def create_user(db: Session, user: models.User):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: models.Item, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item