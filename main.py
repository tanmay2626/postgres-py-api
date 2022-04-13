from database import session, Base, engine
import helpers
import crud
import time

Base.metadata.create_all(bind=engine)

logDNAEventList = helpers.fetch_log_data(1649684226, 1649862237)
# logDNAEventList = ["[event] signed_up: SlawaShev (shevslawa@gmail.com, 37626862+SlawaShev@users.noreply.github.com) signed up.", "[event] failed_stage: KrishnaPapana failed stage #2 of the redis course using Python. Delay: 4s.", "[event] attempted_stage: KrishnaPapana attempted stage #2 of the redis course using Python.", "[event] violated_daily_limit: Fearkin violated the daily limit when completing stage #4 of the redis challenge.", "[event] violated_daily_limit: SlawaShev violated the daily limit when completing stage #4 of the redis challenge."]

signUpEventList, otherEventList = helpers.get_separate_event_list(logDNAEventList)

for user in otherEventList:
	pass
	# Fetch user parent msg ID from DB
		# If present
			# send event as reply msg with parent id
			# update event array in DB with new events
			# retrieve parent msg from slack
			# send update for parent msg in slack with details
		# If not present
			# send event as parent msg
			# create entry in DB with details 

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
		print("Parent Msg Id : ,", parent_msg_id)
		userDetails['msg_id'] = parent_msg_id
		print("Response received from slack", userDetails)
		# Make call to DB to store the signup event for the User
		crud.create_user_signup_entry(session, userDetails)
		print('User Sign Up Entry created in DB')
		time.sleep(1)
	else:
		newEvents = otherEventList[user]
		userData = crud.get_user_by_username(session, user)
		if userData != None:
			parent_msg_id = userData.msg_id
			oldEvents = userData.events
			eventsToUpdate = oldEvents + newEvents[:10-len(oldEvents)]
			# helpers.update_slack_message('signup', parent_msg_id, eventsToUpdate)
			# crud.update_user_signup_events(session, user, eventsToUpdate)
		else:
			print(user + " not available !")
		time.sleep(1)