from database import session, Base, engine
import helpers
import crud
import time

Base.metadata.create_all(bind=engine)

logDNAEventList = helpers.fetch_log_data(1649684226, 1649862237)

signUpEventList, otherEventList = helpers.get_separate_event_list(logDNAEventList)

for user in otherEventList:
	pass

for user in otherEventList:
	if user in signUpEventList:
		userDetails = {
			"username" : signUpEventList[user]['name'],
			"primary_email" : signUpEventList[user]['primary_email'],
			"other_email" : signUpEventList[user]['other_email'],
			"fullstory_link" : "", 
			"mixpanel_link" : "", 
			"events" : signUpEventList[user]['events'][:10],
		}
		# Todo - Make call to Fullstory API to get the details
		# Todo - Make call to Mixpanel API to get the details
		parent_msg_id = helpers.send_slack_message('signup', userDetails)
		userDetails['msg_id'] = parent_msg_id
		crud.create_user_signup_entry(session, userDetails)
		time.sleep(1)
	else:
		newEvents = otherEventList[user]
		userData = crud.get_user_by_username(session, user)
		if userData != None:
			parent_msg_id = userData.msg_id
			oldEvents = userData.events
			eventsToUpdate = oldEvents + newEvents[:10-len(oldEvents)]
			# Todo - update slack & DB
		else:
			print(user + " not available !")
		time.sleep(1)