import requests
import json

channel_list = {
    'signup': 'C036L0W9R46',
    'events': '',
}


def get_signup_content_block(user_details):
    user_name = user_details['username']
    user_primary_email = user_details['primary_email']
    user_other_email = user_details['other_email']
    event_list = user_details['events']
    new_line = '\n'
    return [{
        "color":
        "#396",
        "blocks": [{
            "type": "section",
            "text": {
                "type":
                "mrkdwn",
                "text":
                f"<https://github.com/{user_name}|{user_name}> signed up.\n\n *Primary Email*\n <mailto:{user_primary_email}|{user_primary_email}>\n\n*Other Emails*{''.join([f'{new_line} <mailto:{x}|{x}>' for x in user_other_email])}"
            },
            "accessory": {
                "type": "image",
                "image_url": f"https://github.com/{user_name}.png",
                "alt_text": f"{user_name} avatar"
            }
        }, {
            "type": "section",
            "text": {
                "type":
                "mrkdwn",
                "text":
                f"*First events*\n{''.join([f'{new_line}•{x}' for x in event_list])}"
            }
        }, {
            "type":
            "actions",
            "elements": [{
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "GitHub Profile"
                },
                "url": f'https://github.com/{user_name}'
            }, {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Mixpanel Events"
                },
                "url": f'https://github.com/{user_name}'
            }, {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Fullstory Sessions"
                },
                "url": f'https://github.com/{user_name}'
            }]
        }, {
            "type":
            "context",
            "elements": [{
                "type":
                "plain_text",
                "text":
                "pymetrics Sep 2021 - Present | Bluecore Nov 2020 - Sep 2021"
            }]
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


def send_slack_message(channel_type, user_details):
    channel = channel_list[channel_type]
    slack_post_msg_url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization":
        "Bearer xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7"
    }
    data = {
        "channel": channel,
        "attachments": json.dumps(get_signup_content_block(user_details))
    }
    response = requests.post(slack_post_msg_url, headers=headers, data=data)
    response_data = response.json()
    if "ok" in response_data and response_data["ok"] is True:
        msg_id = response_data['ts']
        return msg_id
    else:
        pass


def update_slack_signup_message(channel_type, parent_msg_id, user_details):
    channel = channel_list[channel_type]
    slack_update_msg_url = 'https://slack.com/api/chat.update'
    headers = {
        "Authorization":
        "Bearer xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7"
    }
    data = {
        "channel": channel,
        "ts": parent_msg_id,
        "attachments": json.dumps(get_signup_content_block(user_details))
    }
    response = requests.post(slack_update_msg_url, headers=headers, data=data)
    response_data = response.json()
    if "ok" in response_data and response_data["ok"] is True:
        pass
    else:
        pass


def get_separate_event_list(log_dna_event_list):
    signup_events = {}
    other_events = {}

    for log_item in log_dna_event_list:
        log_item_inside = log_item['message'].split("[event] ", 1)[1]
        event_type, event_message = [
            x.strip() for x in log_item_inside.split(":", 1)
        ]
        user_name, event_message = event_message.split(" ", 1)
        if event_type == "signed_up":
            event_message = [
                x.replace('(', '').replace(')', '').replace(',', '')
                for x in event_message.rsplit(' ', 2)[0].split(" ")
            ]
            user_primary_email = event_message[0]
            user_other_email = event_message[1:]
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
