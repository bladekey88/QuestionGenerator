from requests import get
from requests import request


token = "l86zutg01F0LZKF6GWtBv1E5KIwcA5qA"
base_url = "https://www.hogwarts.wiz/tracker/api/rest/issues/"
tracker_filter = "?project_id=4&filter_id=17"


def createTicketForSubjectDelete(subject, user):
    username = str(user)
    subjectid = str(subject.subjectid)
    subject = str(subject)

    ticket_exists = checkTicketExists(subjectid)
    deletion_requested_by_user = requestExists(ticket_exists[1], user)

    if ticket_exists[0] is False:
        raw_json = (
            """{
    "summary": "Subject Deletion Request: ID"""
            + subjectid
            + """",
    "description": "Request by """
            + username
            + """ to delete the subject '"""
            + subject
            + """' (id="""
            + subjectid
            + """)",
    "additional_information": "More info about the issue",
    "project": {
        "id": 4,
        "name": "mantisbt"
    },
    "category": {
        "id": 5
    },
    "handler": {
        "name": "administrator"
    },
    "status": {
    "name": "assigned"
  },
    "reporter": {
        "name": "questiongen"
      },
    "view_state": {
        "id": 10,
        "name": "public"
    },
    "priority": {
        "name": "high"
    },
    "severity": {
        "name": "major"
    },
    "reproducibility": {
        "name": "always"
    },
    "sticky": true,
    "custom_fields": [
        {
            "field": {
                "id": 1                
            },
            "value": "None"
        }
    ],
    "tags": [
        {
            "name": "api"
        }
    ]
}"""
        )
        url = base_url
    elif deletion_requested_by_user is True:
        return None
    else:
        raw_json = (
            '{\n  "text": "Deletion also requested by \''
            + username
            + '\'.",\n  "view_state": {\n  \t"name": "public"\n  }\n}'
        )
        url = base_url + "{}/notes".format(ticket_exists[1])

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    response = request(
        "POST",
        url,
        headers=headers,
        data=raw_json,
        allow_redirects=False,
        verify=False,
    )
    return response.status_code
    # return response


def createTicketForTopicDelete(topic, user):
    username = str(user)

    topicid = str(topic.topicid)
    topic = str(topic)
    token = "bIB8EEsp7T8xhwzbcLVtHx1paBz017yx"

    ticket_exists = checkTicketExists(topicid)
    deletion_requested_by_user = requestExists(ticket_exists[1], user)

    if ticket_exists[0] is False:
        payload = (
            '{\n  "summary": "Topic Deletion Request: ID'
            + topicid
            + '",\n  "description": "Request by '
            + username
            + " to Delete Topic "
            + topic
            + " (topicid:"
            + topicid
            + ')",\n "severity": {\n        "name": "major"\n    },\n "category": {\n    "name": "Feature Request"\n  },\n  "project": {\n    "name": "TeachingPeriodically"\n   },\n    "tags": [\n        {\n            "name": "API"\n        }\n    ]\n}'
        )
        url = base_url
    elif deletion_requested_by_user is True:
        return None
    else:
        payload = (
            '{\n  "text": "Deletion also requested by \''
            + username
            + '\'.",\n  "view_state": {\n  \t"name": "public"\n  }\n}'
        )
        url = base_url + "{}/notes".format(ticket_exists[1])

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    response = request(
        "POST",
        url,
        headers=headers,
        data=payload,
        allow_redirects=False,
        verify=False,
    )
    return response.status_code
    # return response


def checkTicketExists(subjectid):
    url = f"{base_url}{tracker_filter}"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    response = get(
        url,
        headers=headers,
        allow_redirects=False,
        verify=False,
    )
    issue_summary = {}
    try:
        for issue in response.json()["issues"]:
            issue_id = issue["id"]
            issue_subject_id = issue["summary"].split(":")[1].strip()[2:]
            issue_summary[issue_subject_id] = issue_id

        if any(subjectid in x for x in issue_summary):
            return True, issue_summary[subjectid]
        else:
            return False, 0
    except ValueError:
        raise Exception(
            """
            Unable to retrieve content from tracking service.
            Is LDAP connection established and site open?
            """
        )


def requestExists(issueid, username):
    url = f"{base_url}{issueid}"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    response = get(
        url,
        headers=headers,
        allow_redirects=False,
        verify=False,
    )
    if response.status_code == 404:
        return False

    if "notes" not in response.json()["issues"][0]:
        return False
    else:
        for note in response.json()["issues"][0]["notes"]:
            user = note["text"].split("'")[1]

            if str(user).lower() == str(username).lower():
                return True
