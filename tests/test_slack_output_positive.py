from app.main import process
from app.helpers import client
from app.config import config
from app.templates.event import event_message
from app.templates.signup import signup_message


def test_slack_output_expected_behaviour(setup, mocker):
    #arrage
    log_dna_events = [{
        'message':
        "[analytics_event] signed_up: Test_SlawaShev (shevslawa@gmail.com, xyx@outlook.com, 37626862+SlawaShev@users.noreply.github.com) signed up."
    }, {
        'message':
        "[analytics_event] failed_stage: Test_SlawaShev failed stage #2 of the redis course using Python. Delay: 4s."
    }, {
        'message':
        "[analytics_event] violated_daily_limit: Test_Fearkin violated the daily limit when completing stage #4 of the redis challenge."
    }]
    client.chat_postMessage = mocker.Mock(side_effect = [{'ts': 123},{'ts': 124},{'ts': 125}])
    
    #act
    process(log_dna_events)

    #assert
    user_details_user1 = {
        "username": 'Test_SlawaShev',
        "primary_email": 'shevslawa@gmail.com',
        "other_email": ['xyx@outlook.com', '37626862+SlawaShev@users.noreply.github.com'],
        "fullstory_link": '',
        "mixpanel_link": '',
        "events": ['failed stage #2 of the redis course using Python. Delay: 4s.'],
    }
    event_details_user1 = {
            'username': 'Test_SlawaShev',
            'events': ['failed stage #2 of the redis course using Python. Delay: 4s.'],
            'parent_event_count': 1,
            'user_last_activity_date': None
    }
    event_details_user2 = {
            'username': 'Test_Fearkin',
            'events': ['violated the daily limit when completing stage #4 of the redis challenge.'],
            'parent_event_count': 1,
            'user_last_activity_date': None
    }
    call1 = mocker.call(channel=config.event_channel_id, attachments=event_message(event_details_user1, None)["attachments"])
    call2 = mocker.call(channel=config.event_channel_id, attachments=event_message(event_details_user2, None)["attachments"])
    call3 = mocker.call(channel=config.signup_channel_id, attachments=signup_message(user_details_user1)["attachments"])
    
    client.chat_postMessage.assert_has_calls([call1,call2,call3],any_order=True)
    assert client.chat_postMessage.call_count == 3