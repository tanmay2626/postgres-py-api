from database import session, Base, engine
import helpers
import crud
import time

Base.metadata.create_all(bind=engine)

log_dba_events= helpers.fetch_log_data(1649684226, 1649862237)

signup_events, other_events = helpers.get_separate_event_list(log_dba_events)

for user in other_events:
	pass

for user in other_events:
	if user in signup_events:
		user_details = {
			"username" : signup_events[user]['name'],
			"primary_email" : signup_events[user]['primary_email'],
			"other_email" : signup_events[user]['other_email'],
			"fullstory_link" : "", 
			"mixpanel_link" : "", 
			"events" : signup_events[user]['events'][:10],
		}
		# Todo - Make call to Fullstory API to get the details
		# Todo - Make call to Mixpanel API to get the details
		parent_msg_id = helpers.send_slack_message('signup', user_details)
		user_details['msg_id'] = parent_msg_id
		crud.create_user_signup_entry(session, user_details)
	else:
		new_events = other_events[user]
		user_data = crud.get_user_by_username(session, user)
		if user_data != None:
			parent_msg_id = user_data.msg_id
			old_events = user_data.events
			events_to_update = old_events + new_events[:10-len(old_events)]
			# Todo - update slack & DB
		else:
			print(user + " not available !")
	time.sleep(1)