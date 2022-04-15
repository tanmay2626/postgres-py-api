import pytest
from app import helpers


def test_get_separate_event_list():
    #arrage
    log_dna_events = [{
        'message':
        "[event] signed_up: SlawaShev (shevslawa@gmail.com, xyx@outlook.com, 37626862+SlawaShev@users.noreply.github.com) signed up."
    }, {
        'message':
        "[event] failed_stage: SlawaShev failed stage #2 of the redis course using Python. Delay: 4s."
    }, {
        'message':
        "[event] violated_daily_limit: Fearkin violated the daily limit when completing stage #4 of the redis challenge."
    }]
    expected_signup_events = {
        "SlawaShev": {
            "name":
            "SlawaShev",
            "primary_email":
            "shevslawa@gmail.com",
            "other_email":
            ["xyx@outlook.com", "37626862+SlawaShev@users.noreply.github.com"],
            "events":
            ["failed stage #2 of the redis course using Python. Delay: 4s."]
        }
    }
    expected_other_events = {
        "SlawaShev":
        ["failed stage #2 of the redis course using Python. Delay: 4s."],
        "Fearkin": [
            "violated the daily limit when completing stage #4 of the redis challenge."
        ]
    }

    #act
    (signup_events,
     other_events) = helpers.separate_event_list(log_dna_events)

    #assert
    assert signup_events == expected_signup_events
    assert other_events == expected_other_events
