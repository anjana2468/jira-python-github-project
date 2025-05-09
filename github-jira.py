@app.route('/createJira', methods=['POST'])
def createJira():
    data = request.get_json()

    # Log the payload for debugging
    print("GitHub payload:", json.dumps(data, indent=2))

    # Extract GitHub issue title and body
    issue_title = data.get('issue', {}).get('title', 'No title')
    issue_body = data.get('issue', {}).get('body', 'No description')

    # Jira config
    url = "https://anjanashaju1997.atlassian.net/rest/api/3/issue"
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Construct the Jira issue payload
    payload = {
        "fields": {
            "project": {
                "key": "AB"  # Replace with your actual Jira project key
            },
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
            "issuetype": {
                "id": "10006"  # Replace with actual issue type ID (e.g., Task or Bug)
            }
        }
    }

    # Send request to Jira
    response = requests.post(url, headers=headers, auth=auth, json=payload)

    # Log response
    print("Jira response:", response.status_code, response.text)

    return json.dumps(response.json(), indent=4)

  
