from app.database import connection
import datetime
from app.helpers import fetch_log_data, separate_event_list, send_slack_message, update_slack_message, send_slack_reply_message
from app.crud import get_user_event_by_username, create_user_event, get_user_by_username, update_user_signup_events, create_user_signup_entry, update_user_events
import time
from dotenv import load_dotenv

def process(log_dna_events):
    signup_events, other_events = separate_event_list(log_dna_events)
    process_other_events(other_events)
    process_signin_events(signup_events,other_events)

def process_other_events(other_events):
    for user in other_events:
        event_details = {
            'username': user,
            'events': other_events[user],
            'parent_event_count': len(other_events[user]),
            'date': datetime.date.today()
        }
        existing_event_data = get_user_event_by_username(connection.session, user,
                                                        event_details['date'])
        if existing_event_data != None:
            existing_event_data = existing_event_data.toDict()
            parent_msg_id = existing_event_data['msg_id']
            event_list = event_details['events']
            send_slack_reply_message('events', parent_msg_id, event_list)
            time.sleep(1)
            existing_event_data[
                'events'] = existing_event_data['events'] + event_list
            update_slack_message('events', parent_msg_id, existing_event_data)
            update_user_events(connection.session, existing_event_data)
        else:
            parent_msg_id = send_slack_message('events', event_details)
            event_details['msg_id'] = parent_msg_id
            create_user_event(connection.session, event_details)
        time.sleep(1)

def process_signin_events(signup_events,other_events):
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
                create_user_signup_entry(connection.session, user_details)
        else:
            new_events = other_events[user]
            user_data = get_user_by_username(connection.session, user)
            if user_data != None:
                user_data = user_data.toDict()
                parent_msg_id = user_data['msg_id']
                old_events = user_data['events']
                events_to_update = old_events + new_events[:10 - len(old_events)]
                user_data['events'] = events_to_update
                update_slack_message('signup', parent_msg_id, user_data)
                update_user_signup_events(connection.session, user_data['username'],
                                        user_data['events'])
            else:
                print(user + " not available !")
        time.sleep(1)

if __name__ == "__main__":
    load_dotenv()
    connection.init()
    log_dna_events = fetch_log_data(1650782283, 165082571)
    process(log_dna_events)
    