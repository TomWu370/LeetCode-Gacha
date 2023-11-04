import leetcode
import database

DIFFICULTY = {1: 'Easy',
              2: 'Medium',
              3: 'Hard'}

leetcode_session = ""  # "yyy"
csrf_token = ""  # "xxx"

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))


def getUsername():
    # get username
    graphql_request = leetcode.GraphqlQuery(
        query="""
         {
           user {
                username
             }
         }
         """,
        variables=leetcode.GraphqlQueryVariables(),
    )
    raw_data = api_instance.graphql_post(body=graphql_request)
    return raw_data.data.user.username


def getQuestions():
    # print all solved algorithm questions, fetch solved questions along with difficulty
    api_response = api_instance.api_problems_topic_get(topic="all")
    solved_questions = {'Easy': 0, 'Medium': 0, 'Hard': 0}

    for questions in api_response.stat_status_pairs:
        if questions.status == "ac":
            solved_questions[DIFFICULTY[questions.difficulty.level]] += 1
    return solved_questions


if __name__ == '__main__':
    print(getUsername())
    print(getQuestions())
    print(database.read())