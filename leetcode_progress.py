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
    "Cookie": 'Your cookie here',
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

