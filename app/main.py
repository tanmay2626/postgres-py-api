from app.database import connection
from app.helpers import fetch_log_data, separate_event_list, send_slack_message, update_slack_message, send_slack_reply_message
from app.crud import get_user_event_by_username, create_user_event, get_user_by_username, update_user_signup_events, create_user_signup_entry, update_user_events, create_error
import time
from datetime import datetime, timedelta, date
from dataclasses import dataclass
from app.models import Job
import sys
import pytz
import logging

timezone = pytz.utc
event_count = 0


def process(log_dna_events):
    signup_events, other_events = separate_event_list(log_dna_events)
    process_signin_events(signup_events, other_events)
    process_other_events(other_events)


def process_other_events(other_events):
    global event_count
    for user in other_events:
        try:
            event_count = event_count + len(other_events[user])
            event_details = {
                'username': user,
                'events': other_events[user],
                'parent_event_count': len(other_events[user]),
                'date': date.today()
            }
            existing_event_data = get_user_event_by_username(
                connection.session, user, event_details['date'])
            if existing_event_data != None:
                existing_event_data = existing_event_data.toDict()
                parent_msg_id = existing_event_data['msg_id']
                event_list = event_details['events']
                send_slack_reply_message('events', parent_msg_id,
                                         event_details)
                time.sleep(1)
                existing_event_data[
                    'events'] = existing_event_data['events'] + event_list
                update_slack_message('events', parent_msg_id,
                                     existing_event_data)
                update_user_events(connection.session, existing_event_data)
            else:
                parent_msg_id = send_slack_message('events', event_details)
                event_details['msg_id'] = parent_msg_id
                create_user_event(connection.session, event_details)
            time.sleep(1)
        except Exception as e:
            connection.session.rollback()
            create_error(connection.session, 'other_events', e)


def process_signin_events(signup_events, other_events):
    global event_count
    for user in other_events:
        try:
            if user in signup_events:
                event_count = event_count + 1
                user_details = {
                    "username": signup_events[user]['name'],
                    "primary_email": signup_events[user]['primary_email'],
                    "other_email": signup_events[user]['other_email'],
                    "fullstory_link": "",
                    "mixpanel_link": "",
                    "events": signup_events[user]['events'][:10],
                    "timestamp": signup_events[user]['signup_timestamp']
                }
                # Todo - Make call to Fullstory API to get the details
                # Todo - Make call to Mixpanel API to get the details
                parent_msg_id = send_slack_message('signup', user_details)
                user_details['msg_id'] = parent_msg_id
                create_user_signup_entry(connection.session, user_details)
            else:
                new_events = other_events[user]
                user_data = get_user_by_username(connection.session, user)
                if user_data != None:
                    user_data = user_data.toDict()
                    parent_msg_id = user_data['msg_id']
                    old_events = user_data['events']
                    events_to_update = old_events + new_events[:10 -
                                                               len(old_events)]
                    user_data['events'] = events_to_update
                    update_slack_message('signup', parent_msg_id, user_data)
                    update_user_signup_events(connection.session,
                                              user_data['username'],
                                              user_data['events'])
                else:
                    logging.warning(user + " not available !")
            time.sleep(1)
        except Exception as e:
            connection.session.rollback()
            create_error(connection.session, 'user_events', e)


def demo_run():
    connection.init()
    current_time_sec = time.time_ns() // 1_000_000_000
    log_dna_events = fetch_log_data(current_time_sec - 86400, current_time_sec)
    process(log_dna_events)


def run():
    global event_count
    connection.init()
    current_time_ms = time.time_ns() // 1_000_000
    job = Job(
        logdna_start_time=current_time_ms - 60_000,  #10min 
        logdna_end_time=current_time_ms,
        start_time=datetime.now(timezone),
        status='running')
    while (True):
        try:
            event_count = 0
            connection.session.add(job)
            connection.session.commit()

            log_dna_events = fetch_log_data(int(job.logdna_start_time),
                                            int(job.logdna_end_time))
            process(log_dna_events)

            job.end_time = datetime.now(timezone)
            job.status = 'success'
            job.duration = job.end_time - job.start_time
            job.logdna_duration = (int(job.logdna_end_time) -
                                   int(job.logdna_start_time)) / 1000
            job.event_count = event_count
            connection.session.commit()

            current_time_ms = time.time_ns() // 1_000_000
            if current_time_ms - int(job.logdna_end_time) < 60_000:  #1min
                time.sleep(
                    (60_000 -
                     (current_time_ms - int(job.logdna_end_time))) / 1000)

            current_time_ms = time.time_ns() // 1_000_000
            job = Job(logdna_start_time=int(job.logdna_end_time),
                      logdna_end_time=current_time_ms,
                      start_time=datetime.now(timezone),
                      status='running')
        except Exception as e:
            connection.session.rollback()
            create_error(connection.session, 'job', e)


if __name__ == "__main__":

    try:
        if not (len(sys.argv) == 2 and sys.argv[1] == 'prod'):
            demo_run()
            exit()
        run()
    except Exception as e:
        logging.error("process error: " + str(e))
        connection.session.rollback()
        create_error(connection.session, 'process', e)
