from app.main import process
from app.helpers import client
from app.config import config
from app.templates.event import event_message
from app.templates.signup import signup_message
from app.templates.event_reply import event_reply
from app.crud import create_user_event, create_user_signup_entry
from freezegun import freeze_time

# TODO add only sigup test case


def test_signup_and_event_message(database, mocker):
    #arrage
    log_dna_events = [{
        'message':
        "[analytics_event] signed_up: Test_SlawaShev (shevslawa@gmail.com, xyx@outlook.com, 37626862+SlawaShev@users.noreply.github.com) signed up.",
        'timestamp': '2022-05-21T12:54:50.605805+00:00'
    }, {
        'message':
        "[analytics_event] failed_stage: Test_SlawaShev failed stage #2 of the redis course using Python. Delay: 4s.",
        'timestamp': '2022-05-21T12:54:50.605805+00:00'
    }, {
        'message':
        "[analytics_event] violated_daily_limit: Test_Fearkin violated the daily limit when completing stage #4 of the redis challenge.",
        'timestamp': '2022-05-21T12:54:50.605805+00:00'
    }]
    client.chat_postMessage = mocker.Mock(side_effect=[{
        'ts': 123
    }, {
        'ts': 124
    }, {
        'ts': 125
    }])

    #act
    process(log_dna_events)

    #assert
    user_detail_user1 = {
        'username':
        'Test_SlawaShev',
        'primary_email':
        'shevslawa@gmail.com',
        'other_email':
        ['xyx@outlook.com', '37626862+SlawaShev@users.noreply.github.com'],
        'fullstory_link':
        '',
        'mixpanel_link':
        '',
        'events':
        ['failed stage #2 of the redis course using Python. Delay: 4s.'],
    }
    event_detail_user1 = {
        'username': 'Test_SlawaShev',
        'events':
        ['failed stage #2 of the redis course using Python. Delay: 4s.'],
        'parent_event_count': 1,
        'user_last_activity_date': None
    }
    event_detail_user2 = {
        'username':
        'Test_Fearkin',
        'events': [
            'violated the daily limit when completing stage #4 of the redis challenge.'
        ],
        'parent_event_count':
        1,
        'user_last_activity_date':
        None
    }

    signup_call = mocker.call(
        channel=config.signup_channel_id,
        attachments=signup_message(user_detail_user1)["attachments"])

    event_call1 = mocker.call(channel=config.event_channel_id,
                              attachments=event_message(
                                  event_detail_user1, None,
                                  '2022-05-21')["attachments"])
    event_call2 = mocker.call(channel=config.event_channel_id,
                              attachments=event_message(
                                  event_detail_user2, None,
                                  'Not available')["attachments"])

    assert client.chat_postMessage.call_args_list == [
        signup_call, event_call1, event_call2
    ]
    assert client.chat_postMessage.call_count == 3


@freeze_time("2022-05-21")
def test_event_reply_message(database, mocker):

    event_record = {
        'username': 'Test_Fearkin',
        'events':
        ['failed stage #2 of the redis course using Python. Delay: 4s.'],
        'parent_event_count': 1,
        'date': '2022-05-21',
        'msg_id': 122,
    }
    signin_record = {
        'username': 'Test_Fearkin',
        'events':
        ['failed stage #2 of the redis course using Python. Delay: 4s.'],
        'primary_email': 'fearkin@gmail.com',
        'other_email': [],
        'msg_id': 1,
        'fullstory_link': '',
        'mixpanel_link': '',
        'timestamp': '2022-05-19T09:33:43.716806+00:00'
    }
    create_user_event(database.session, event_record)
    create_user_signup_entry(database.session, signin_record)

    #arrage
    log_dna_events = [{
        'message':
        "[analytics_event] viewed: Test_Fearkin viewed the course list page.",
        'timestamp': '2022-05-21T12:54:50.605805+00:00'
    }, {
        'message':
        "[analytics_event] violated_daily_limit: Test_Fearkin violated the daily limit when completing stage #4 of the redis challenge.",
        'timestamp': '2022-05-21T12:54:50.605805+00:00'
    }]
    client.chat_postMessage = mocker.Mock(side_effect=[{'ts': 123}])

    client.chat_update = mocker.Mock(side_effect=[{'ts': 124}, {'ts': 125}])

    #act
    process(log_dna_events)

    #assert
    event_detail = {
        'username':
        'Test_Fearkin',
        'events': [
            'failed stage #2 of the redis course using Python. Delay: 4s.',
            'viewed the course list page.',
            'violated the daily limit when completing stage #4 of the redis challenge.'
        ],
        'parent_event_count':
        1,
    }
    event_reply_detail = {
        'username':
        'Test_Fearkin',
        'events': [
            'viewed the course list page.',
            'violated the daily limit when completing stage #4 of the redis challenge.'
        ],
    }
    signin_detail = {
        'username':
        'Test_Fearkin',
        'primary_email':
        'fearkin@gmail.com',
        'other_email': [],
        'fullstory_link':
        '',
        'mixpanel_link':
        '',
        'events': [
            'failed stage #2 of the redis course using Python. Delay: 4s.',
            'viewed the course list page.',
            'violated the daily limit when completing stage #4 of the redis challenge.'
        ],
    }

    reply_call = mocker.call(
        channel=config.event_channel_id,
        thread_ts='122',
        attachments=event_reply(event_reply_detail)["attachments"])

    update_event_call = mocker.call(channel=config.event_channel_id,
                                    ts='122',
                                    attachments=event_message(
                                        event_detail, '2022-05-21',
                                        '2022-05-19')["attachments"])
    update_signup_call = mocker.call(
        channel=config.event_channel_id,
        ts='1',
        attachments=signup_message(signin_detail)["attachments"])

    assert client.chat_postMessage.call_args_list == [reply_call]
    assert client.chat_postMessage.call_count == 1

    assert client.chat_update.call_args_list == [
        update_signup_call, update_event_call
    ]
    assert client.chat_update.call_count == 2
