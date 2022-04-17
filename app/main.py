from app.database import session, Base, engine
import datetime
from app.helpers import fetch_log_data, separate_event_list, send_slack_message, update_slack_message
from app.crud import get_user_event_by_username, create_user_event, get_user_by_username, update_user_signup_events, create_user_signup_entry
import time

log_dna_events = fetch_log_data(1649684226, 1649862237)

signup_events, other_events = separate_event_list(log_dna_events)

for user in other_events:
    event_details = {
        'username': user,
        'events': other_events[user],
        'date': datetime.datetime.today()
    }
    event_data = get_user_event_by_username(session, user,
                                            event_details['date'])
    if event_data != None:
        # Todo
        # Send event as reply slack message to parent msg
        # Update parent msg with the data
        # store in DB with new events
        # send update slack msg
        pass
    else:
        parent_msg_id = send_slack_message('events', event_details)
        event_details['msg_id'] = parent_msg_id
        create_user_event(session, event_details)
    time.sleep(1)

for user in other_events:
    if user in signup_events:
        user_details = {
            "username": signup_events[user]['name'],
            "primary_email": signup_events[user]['primary_email'],
            "other_email": signup_events[user]['other_email'],
            "fullstory_link": "",
            "mixpanel_link": "",
            "events": signup_events[user]['events'][:10],
        }
        # Todo - Make call to Fullstory API to get the details
        # Todo - Make call to Mixpanel API to get the details
        parent_msg_id = send_slack_message('signup', user_details)
        if parent_msg_id != None:
            user_details['msg_id'] = parent_msg_id
            create_user_signup_entry(session, user_details)
    else:
        new_events = other_events[user]
        user_data = get_user_by_username(session, user)
        if user_data != None:
            user_data = user_data.toDict()
            parent_msg_id = user_data['msg_id']
            old_events = user_data['events']
            events_to_update = old_events + new_events[:10 - len(old_events)]
            user_data['events'] = events_to_update
            update_slack_message('signup', parent_msg_id, user_data)
            update_user_signup_events(session, user_data['username'],
                                      user_data['events'])
        else:
            print(user + " not available !")
    time.sleep(1)
