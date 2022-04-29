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
    slack_token = None
    logdna_token = None
    logdna_key = None

    def __init__(self):
        self.postgres_url = os.getenv('POSTGRES_URL')
        self.signup_channel_id = os.getenv('SIGNUP_CHANNEL_ID')
        self.event_channel_id = os.getenv('EVENT_CHANNEL_ID')
        self.logdna_token = os.getenv('LOGDNA_TOKEN')
        self.logdna_key = os.getenv('LOGDNA_KEY')
        self.slack_token = os.getenv('SLACK_TOKEN')


config = Config()
