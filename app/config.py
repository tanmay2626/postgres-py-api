import os
from dotenv import load_dotenv

if os.getenv('ENV') == 'test':
    load_dotenv('.env.test')
else:
    load_dotenv()


class Config:
    postgres_url = None
    signup_channel_id = None
    event_channel_id = None
    slack_bot_auth = None
    bearer_token = None

    def __init__(self):
        self.postgres_url = os.getenv('POSTGRES_URL')
        self.signup_channel_id = os.getenv('SIGNUP_CHANNEL_ID')
        self.event_channel_id = os.getenv('EVENT_CHANNEL_ID')
        self.slack_bot_auth = os.getenv('SLACK_BOT_AUTH')
        self.bearer_token = os.getenv('BEARER_TOKEN')


config = Config()
