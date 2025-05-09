from flask import Flask, request
from requests.auth import HTTPBasicAuth
import requests
import json
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def createJira():
    url = "https://anjanashaju1997.atlassian.net/rest/api/3/issue"

    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "description": {
                "content": [{
                    "content": [{
                        "text": "Order entry fails when selecting supplier.",
                        "type": "text"
                    }],
                    "type": "paragraph"
                }],
                "type": "doc",
                "version": 1
            },
            "project": {
                "key": "AB"
            },
            "issuetype": {
                "id": "10006"
            },
            "summary": "Main order flow broken"
        },
        "update": {}
    })

    response = requests.post(url, data=payload, headers=headers, auth=auth)
    return json.dumps(json.loads(response.text), indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
