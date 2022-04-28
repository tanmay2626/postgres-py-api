new_line = '\n'


def signup_message(user_details):
    return {
        "attachments": [{
            "fallback":
            f"Message for {user_details['username']} errored",
            "color":
            "#396",
            "blocks": [{
                "type": "section",
                "text": {
                    "type":
                    "mrkdwn",
                    "text":
                    f"<https://github.com/{user_details['username']}|{user_details['username']}> signed up.\n\n *Primary Email*\n <mailto:{user_details['primary_email']}|{user_details['primary_email']}>\n\n*Other Emails*{''.join([f'{new_line} <mailto:{x}|{x}>' for x in user_details['other_email']])}"
                },
                "accessory": {
                    "type": "image",
                    "image_url":
                    f"https://github.com/{user_details['username']}.png",
                    "alt_text": f"{user_details['username']} avatar"
                }
            }, {
                "type": "section",
                "text": {
                    "type":
                    "mrkdwn",
                    "text":
                    f"*First events*\n{''.join([f'{new_line}•{x}' for x in user_details['events']])}"
                }
            }, {
                "type":
                "actions",
                "elements": [{
                    "type":
                    "button",
                    "text": {
                        "type": "plain_text",
                        "text": "GitHub Profile"
                    },
                    "url":
                    f"https://github.com/{user_details['username']}"
                }]
            }]
        }]
    }
