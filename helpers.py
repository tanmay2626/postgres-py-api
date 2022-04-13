import requests
import json

channelList = {
	'signup': 'C036L0W9R46',
	'events': '',
}

def get_signup_content_block(userDetails):
	user_name = userDetails['username']
	user_primary_email = userDetails['primary_email']
	user_other_email = userDetails['other_email']
	eventList = userDetails['events']
	new_line = '\n'
	return [
		{
			"color": "#396",
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"<https://github.com/{user_name}|{user_name}> signed up.\n\n *Primary Email*\n <mailto:{user_primary_email}|{user_primary_email}>\n\n*Other Emails*{''.join([f'{new_line} <mailto:{x}|{x}>' for x in user_other_email])}"
					},
					"accessory": {
						"type": "image",
						"image_url": f"https://github.com/{user_name}.png",
						"alt_text": f"{user_name} avatar"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"*First events*\n{''.join([f'{new_line}•{x}' for x in eventList])}"
					}
				},
				{
					"type": "actions",
					"elements": [
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"text": "GitHub Profile"
							},
							"url": f'https://github.com/{user_name}'
						},
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"text": "Mixpanel Events"
							},
							"url": f'https://github.com/{user_name}'
						},
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"text": "Fullstory Sessions"
							},
							"url": f'https://github.com/{user_name}'
						}
					]
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "plain_text",
							"text": "pymetrics Sep 2021 - Present | Bluecore Nov 2020 - Sep 2021"
						}
					]
				}
			]
		}
	]

def get_signup_update_content_block(eventList):
	new_line = '\n'
	return {"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"*First events*\n{''.join([f'{new_line}•{x}' for x in eventList])}"
					}
}

def fetch_log_data(fromTime, toTime, paginationId=None):
	localData = []
	logDNAExportURL = 'https://api.logdna.com/v2/export'
	params = {
		'from': fromTime,
		'to': toTime,
		'size': 100,
		'query': 'host:codecrafters-server app:app[web] [event] -host:codecrafters-server-stg',
		'prefer': 'head',
		'pagination_id': paginationId
		}
	response = requests.get(logDNAExportURL, params=params, auth=('slack-bot', 'd36cf2076a8f4e61a1f1cec926ed1ff5'))
	logData =  response.json()
	
	localData.extend(logData['lines'])
	
	if logData['pagination_id'] == None:
		return localData
	else:
		localData += fetch_log_data(fromTime, toTime, logData['pagination_id'])
	
	return localData

def send_slack_message(channelType, userDetails):
	channel = channelList[channelType]
	logDNAExportURL = 'https://slack.com/api/chat.postMessage'
	headers = {"Authorization": "Bearer xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7"}
	data = {
		"channel": channel,
		"attachments": json.dumps(get_signup_content_block(userDetails))
		}
	response = requests.post(logDNAExportURL, headers=headers, data=data)
	responseData =  response.json()
	print(responseData)
	if "ok" in responseData and responseData["ok"] is True:
		print("In True")
		msg_id = responseData['ts']
		return msg_id
	else:
		print("In false")
		pass

# Todo - Incomplete function
def update_slack_message(channelType, parent_msg_id, eventList):
	channel = channelList[channelType]
	logDNAExportURL = 'https://slack.com/api/chat.update'
	headers = {"Authorization": "Bearer xoxb-3232981397716-3354861731686-fmcWNRZNxW1bgGW1XZOQBfa7"}
	data = {
		"channel": channel,
		"ts": parent_msg_id,
		"attachments": json.dumps(get_signup_update_content_block(eventList))
		}
	response = requests.post(logDNAExportURL, headers=headers, data=data)
	responseData =  response.json()
	if "ok" in responseData == True:
		msg_id = responseData['ts']
		return msg_id
	else:
		pass

def get_separate_event_list(logDNAEventList):
	signUpEventList = {}
	otherEventList = {}

	for logItem in logDNAEventList:
		logItemInside = logItem['message'].split("[event] ", 1)[1]
		eventType, eventMessage = [x.strip() for x in logItemInside.split(":", 1)]
		user_name, eventMessage  = eventMessage.split(" ", 1)
		if eventType == "signed_up":
			eventMessage = [x.replace('(','').replace(')','').replace(',','') for x in eventMessage.rsplit(' ', 2)[0].split(" ")]
			user_primary_email = eventMessage[0]
			user_other_email = eventMessage[1:]
			signUpEventList[user_name] = {
				"name" : user_name,
				"primary_email" : user_primary_email,
				"other_email" : user_other_email,
				"events" : []
				}
		else:
			if user_name in otherEventList:
				otherEventList[user_name].append(eventMessage)
			else:
				otherEventList[user_name] = [eventMessage]
			
			if user_name in signUpEventList:
				signUpEventList[user_name]['events'].append(eventMessage)
	
	return (signUpEventList, otherEventList)