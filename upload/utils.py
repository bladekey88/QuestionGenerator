from requests import get
from requests import request



def createTicketForSubjectDelete(subject,user):
    username =str(user)
    
    subjectid = str(subject.subjectid)
    subject = str(subject)
    token = 'bIB8EEsp7T8xhwzbcLVtHx1paBz017yx'
   


    ticket_exists = checkTicketExists(subjectid)
    deletion_requested_by_user =  requestExists(ticket_exists[1],user)
    
    if ticket_exists[0] is False:
        payload = "{\n  \"summary\": \"Subject Deletion Request: ID" + subjectid + "\",\n  \"description\": \"Request by " + username + " to Delete Subject " + subject + " (subjectid:" + subjectid + ")\",\n \"severity\": {\n        \"name\": \"major\"\n    },\n \"category\": {\n    \"name\": \"Feature Request\"\n  },\n  \"project\": {\n    \"name\": \"TeachingPeriodically\"\n   },\n    \"tags\": [\n        {\n            \"name\": \"API\"\n        }\n    ]\n}"
        # payload = "{\n  \"summary\": \"Subject Deletion Request: ID" + subjectid + "\",\n  \"description\": \"Request by " + username + " to Delete Subject " + subject + " (subjectid:" + subjectid + ")\",\n \"severity\": {\n        \"name\": \"major\"\n    },\n \"category\": {\n    \"name\": \"Feature Request\"\n  },\n  \"project\": {\n    \"name\": \"TeachingPeriodically\"\n   },\n    \"tags\": [\n        {\n            \"name\": \"API\"\n        }\n    ]\n}"
        url = "https://www.teachingperiodically.com/tracking/api/rest/issues/"
        # raise Exception(payload)
    elif deletion_requested_by_user is True:
        return None       
    else:
        payload = "{\n  \"text\": \"Deletion also requested by '" + username + "'.\",\n  \"view_state\": {\n  \t\"name\": \"public\"\n  }\n}"
        url = "https://www.teachingperiodically.com/tracking/api/rest/issues/{}/notes".format(ticket_exists[1])

    headers = {
        "Authorization" : token,
        "Content-Type" : "application/json",    
    }
    response = request("POST", url, headers=headers, data = payload, allow_redirects = False)
    return response.status_code
    # return response

     
def createTicketForTopicDelete(topic,user):
    username =str(user)
    
    topicid = str(topic.topicid)
    topic = str(topic)
    token = 'bIB8EEsp7T8xhwzbcLVtHx1paBz017yx'



    ticket_exists = checkTicketExists(topicid)
    deletion_requested_by_user =  requestExists(ticket_exists[1],user)
    
    if ticket_exists[0] is False:
        payload = "{\n  \"summary\": \"Topic Deletion Request: ID" + topicid + "\",\n  \"description\": \"Request by " + username + " to Delete Topic " + topic + " (topicid:" + topicid + ")\",\n \"severity\": {\n        \"name\": \"major\"\n    },\n \"category\": {\n    \"name\": \"Feature Request\"\n  },\n  \"project\": {\n    \"name\": \"TeachingPeriodically\"\n   },\n    \"tags\": [\n        {\n            \"name\": \"API\"\n        }\n    ]\n}"
        url = "https://www.teachingperiodically.com/tracking/api/rest/issues/"
    elif deletion_requested_by_user is True:
        return None       
    else:
        payload = "{\n  \"text\": \"Deletion also requested by '" + username + "'.\",\n  \"view_state\": {\n  \t\"name\": \"public\"\n  }\n}"
        url = "https://www.teachingperiodically.com/tracking/api/rest/issues/{}/notes".format(ticket_exists[1])

    headers = {
        "Authorization" : token,
        "Content-Type" : "application/json",    
    }
    response = request("POST", url, headers=headers, data = payload, allow_redirects = False)
    return response.status_code
    # return response





def checkTicketExists(subjectid):
    
    token = 'bIB8EEsp7T8xhwzbcLVtHx1paBz017yx'
    url = "https://www.teachingperiodically.com/tracking/api/rest/issues?filter_id=6" 

    headers = {
        "Authorization" : token,
        "Content-Type" : "application/json",    
    }

    response = get(url, headers = headers, allow_redirects=False)

    issue_summary = {}
    for issue in response.json()["issues"]:
        issue_id = issue['id']
        issue_subject_id = issue["summary"].split(":")[1].strip()[2:]
        issue_summary[issue_subject_id] = issue_id

    
    
    if any(subjectid in x for x in issue_summary):
       return True, issue_summary[subjectid]
    else:
        return False,0
    
def requestExists(issueid,username):
    token = 'bIB8EEsp7T8xhwzbcLVtHx1paBz017yx'
    url = "https://www.teachingperiodically.com/tracking/api/rest/issues/{}".format(issueid) 

    headers = {
        "Authorization" : token,
        "Content-Type" : "application/json",    
    }

    response = get(url, headers = headers, allow_redirects=False)

    if response.status_code == 404:
        return False

    if "notes" not in  response.json()['issues'][0]:
        return False
    else:
        for note in response.json()['issues'][0]['notes']:
            user = (note['text'].split("\'")[1])

            if str(user).lower() == str(username).lower():
            
                return True
            else:
                return False
          
