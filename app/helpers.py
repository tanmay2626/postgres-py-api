import requests
import json
from app.crud import get_user_last_activity_date
from app.database import session
from collections import OrderedDict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.templates.signup import signup_message
from app.templates.event import event_message
import re

channel_list = {
    'signup': 'C036L0W9R46',
    'events': 'C036L0W9R46',
}

client = WebClient(
    token="xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7")


def get_signup_content_block(user_details):
    return signup_message(user_details)


def get_event_content_block(event_details):
    user_last_activity_date = get_user_last_activity_date(
        session, event_details['username'])
    # Todo - Get user signup date from DB
    new_line = '\n'
    return event_message(event_details, user_last_activity_date)


def get_event_reply_content_block(event_list):
    new_line = '\n'
    return [{
        "color":
        "#396",
        "blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{''.join([f'{new_line}•{x}' for x in event_list])}"
            }
        }]
    }]


def fetch_log_data(from_time, to_time, pagination_id=None):
    local_data = []
    log_dna_export_url = 'https://api.logdna.com/v2/export'
    params = {
        'from': from_time,
        'to': to_time,
        'size': 100,
        'query':
        'host:codecrafters-server app:app[web] [event] -host:codecrafters-server-stg',
        'prefer': 'head',
        'pagination_id': pagination_id
    }
    response = requests.get(log_dna_export_url,
                            params=params,
                            auth=('slack-bot',
                                  'd36cf2076a8f4e61a1f1cec926ed1ff5'))
    log_data = response.json()

    local_data.extend(log_data['lines'])

    if log_data['pagination_id'] == None:
        return local_data
    else:
        local_data += fetch_log_data(from_time, to_time,
                                     log_data['pagination_id'])

    return local_data


def send_slack_message(channel_type, details):
    channel = channel_list[channel_type]
    message_content = get_signup_content_block(details) if (
        channel_type == 'signup') else get_event_content_block(details)
    try:
        result = client.chat_postMessage(
            channel=channel, attachments=message_content["attachments"])
        return result.get("thread_ts")
    except SlackApiError as e:
        print(f"Error: {e}")
        return None


def send_slack_reply_message(channel_type, parent_msg_id, events_list):
    channel = channel_list[channel_type]
    message_content = get_event_reply_content_block(events_list)
    slack_post_msg_url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization":
        "Bearer xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7"
    }
    data = {
        "channel": channel,
        "thread_ts": parent_msg_id,
        "attachments": json.dumps(message_content)
    }
    response = requests.post(slack_post_msg_url, headers=headers, data=data)
    response_data = response.json()
    if "ok" in response_data and response_data["ok"] is True:
        msg_id = response_data['ts']
        return msg_id
    else:
        pass


def update_slack_message(channel_type, parent_msg_id, details):
    channel = channel_list[channel_type]
    message_content = get_signup_content_block(details) if (
        channel_type == 'signup') else get_event_content_block(details)
    try:
        result = client.chat_postMessage(
            channel=channel,
            ts=parent_msg_id,
            attachments=message_content["attachments"])
        return result.get("thread_ts")
    except SlackApiError as e:
        print(f"Error: {e}")
        return None


def separate_event_list(log_dna_event_list):
    signup_events = OrderedDict()
    other_events = OrderedDict()
    for log_item in log_dna_event_list:
        log_message = log_item['message']
        event_message = log_message[log_message.index(":") + 1:].strip()
        user_name, event_message = event_message.split(" ", 1)
        if "signed_up" in log_message:
            user_primary_email, *user_other_email, _ = [
                x.replace('(', '').replace(')', '').replace(',', '')
                for x in event_message.rsplit('signed up.', 1)[0].split(" ")
            ]
            signup_events[user_name] = {
                "name": user_name,
                "primary_email": user_primary_email,
                "other_email": user_other_email,
                "events": []
            }
        else:
            if user_name in other_events:
                other_events[user_name].append(event_message)
            else:
                other_events[user_name] = [event_message]
            if user_name in signup_events:
                signup_events[user_name]['events'].append(event_message)
    return (signup_events, other_events)
