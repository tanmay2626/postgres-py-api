new_line = '\n'


def event_message(event_details, user_last_activity_date):
    return {
        "attachments": [{
            "fallback":
            f"Message for {event_details['username']} errored",
            "color":
            "#396",
            "blocks": [{
                "type": "section",
                "text": {
                    "type":
                    "mrkdwn",
                    "text":
                    f"<https://github.com/{event_details['username']}|{event_details['username']}> performed *{len(event_details['events'])}* events today.\n\n*Last Activity*\n {user_last_activity_date}\n\n*Signed Up*\n {'x'} years ago"
                },
                "accessory": {
                    "type":
                    "overflow",
                    "options": [{
                        "text": {
                            "type": "plain_text",
                            "text": "GitHub Profile"
                        },
                        "url":
                        f"https://github.com/{event_details['username']}"
                    }, {
                        "text": {
                            "type": "plain_text",
                            "text": "Mixpanel Events"
                        },
                        "url":
                        f"https://github.com/{event_details['username']}"
                    }, {
                        "text": {
                            "type": "plain_text",
                            "text": "Fullstory Sessions"
                        },
                        "url":
                        f"https://github.com/{event_details['username']}"
                    }]
                }
            }, {
                "type": "section",
                "text": {
                    "type":
                    "mrkdwn",
                    "text":
                    f"*Events Today*\n{''.join([f'{new_line}•{x}' for x in event_details['events']])}"
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type": "image",
                    "image_url":
                    f"https://github.com/{event_details['username']}.png",
                    "alt_text": f"{event_details['username']} avatar"
                }, {
                    "type": "plain_text",
                    "text": "pymetrics Sep 2021 - Present"
                }]
            }]
        }]
    }
