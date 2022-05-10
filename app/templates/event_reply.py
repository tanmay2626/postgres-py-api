new_line = '\n'


def event_reply(event_details):
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
                    f"{''.join([f'{new_line}•{x}' for x in event_details['events']])}"
                }
            }]
        }]
    }
