import requests
from datetime import datetime

# Define the GraphQL query and variables
query = """
    query progressList($pageNo: Int, $numPerPage: Int, $filters: ProgressListFilterInput) {
      isProgressCalculated
      solvedQuestionsInfo(pageNo: $pageNo, numPerPage: $numPerPage, filters: $filters) {
        currentPage
        pageNum
        totalNum
        data {
          totalSolves
          question {
            questionFrontendId
            questionTitle
            questionDetailUrl
            difficulty
            topicTags {
              name
              slug
            }
          }
          lastAcSession {
            time
            wrongAttempts
          }
        }
      }
    }
"""

variables = {
    "pageNo": 1,
    "numPerPage": 10,
    "filters": {}
}

# Define the URL and headers
url = "https://leetcode.com/graphql/"
headers = {
    "Host": "leetcode.com",
    "Content-Type": "application/json",
    "Cookie": 'NEW_PROBLEMLIST_PAGE=1; _gid=GA1.2.1806238382.1693576222; gr_user_id=3ffae3ef-d9bd-4fce-9d3e-9cb9bbfb1a88; 87b5a3c3f1a55520_gr_session_id=a9838799-65e9-4d12-9661-c84ecc1d9c1d; 87b5a3c3f1a55520_gr_session_id_sent_vst=a9838799-65e9-4d12-9661-c84ecc1d9c1d; csrftoken=bm6BXW2UfvrQJ6CJbI3U6hTdbNL0l8fWgibNB1i4Hv9HzX4Tx9e6UpZ1ATQwRXf2; messages="5defe2066c63df796bf1e893c2fe7e50f9b42773$[[\"__json_message\"\0540\05425\054\"Successfully signed in as adidhande39.\"]]"; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMjMwNzE5NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMTZjMWRiZjQ1YmNkNGUzZTRmMzRmZTAyNmRjMjYxMGE3ZDk1ZmQiLCJpZCI6MjMwNzE5NiwiZW1haWwiOiJhZGlkaGFuZGUzOUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImFkaWRoYW5kZTM5IiwidXNlcl9zbHVnIjoiYWRpZGhhbmRlMzkiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYWRpZGhhbmRlMzkvYXZhdGFyXzE1NzA0NjM2MjMucG5nIiwicmVmcmVzaGVkX2F0IjoxNjkzNTc2NDg1LCJpcCI6IjIyMy4xNzguMjEzLjU0IiwiaWRlbnRpdHkiOiJmYjEyMTU4YmI5ODcwOTJkZDkyMmFiZjVkYjUwN2VjYyIsInNlc3Npb25faWQiOjQ1NDMyODk5fQ.sh0LMa3UrnUKSMo4A7-yKrS0LwcCJga_f5kzAoE3auA; _ga=GA1.1.1366968427.1693576222; _dd_s=rum=0&expire=1693577649727; _ga_CDRWKZTDEX=GS1.1.1693576221.1.1.1693576751.60.0.0',
    # Add your cookies here
    "Authorization": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
}

# Define the request payload
payload = {
    "query": query,
    "variables": variables,
    "operationName": "progressList"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    solved_questions = data['data']['solvedQuestionsInfo']['data']

    for question in solved_questions:
        last_ac_session = datetime.strptime(question['lastAcSession']['time'], '%Y-%m-%dT%H:%M:%S+00:00')
        question_id = question['question']['questionFrontendId']
        question_title = question['question']['questionTitle']
        question_detail_url = "https://leetcode.com" + question['question']['questionDetailUrl']
        difficulty = question['question']['difficulty']
        tags = [tag['name'] for tag in question['question']['topicTags']]
        wrong_attempts = question['lastAcSession']['wrongAttempts']
        total_solves = question['totalSolves']

        # Format and print the information in one row
        print(
            f"{last_ac_session.strftime('%b %d, %Y')} | {question_id}. {question_title} | {' '.join(tags)} | {difficulty} | Wrong Attempts: {wrong_attempts} | Total Solves: {total_solves} | {question_detail_url}")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

