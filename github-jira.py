from flask import Flask, request
from requests.auth import HTTPBasicAuth
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def createJira():
    try:
        # Get JSON payload from GitHub webhook
        data = request.get_json()
        print("Received payload:", json.dumps(data, indent=2))

        # Only act on 'opened' issue events
        if data.get('action') != 'opened' or 'issue' not in data:
            return {"message": "Not an issue creation event"}, 200

        issue_title = data['issue']['title']
        issue_body = data['issue'].get('body', 'No description provided.')

        # Jira API configuration
        jira_url = "https://anjanashaju1997.atlassian.net/rest/api/3/issue"
        email = os.getenv("JIRA_EMAIL")
        api_token = os.getenv("JIRA_API_TOKEN")
        auth = HTTPBasicAuth(email, api_token)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Construct Jira issue payload
        payload = {
            "fields": {
                "project": { "key": "AN" },  # Replace with your project key
                "summary": issue_title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": issue_body
                        }]
                    }]
                },
                "issuetype": { "id": "10006" }  # Replace with your issue type ID
            }
        }

        # Send POST request to Jira
        response = requests.post(jira_url, headers=headers, auth=auth, json=payload)
        print("Jira response:", response.status_code, response.text)

        return json.dumps(response.json(), indent=4)

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

   

   

  
