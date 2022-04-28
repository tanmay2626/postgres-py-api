from app import main
from dotenv import load_dotenv


def test_slack_output_expected_behaviour(setup):
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

    main.process(log_dna_events)
