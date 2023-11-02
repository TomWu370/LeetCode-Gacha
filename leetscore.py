import leetcode

DIFFICULTY =  {1:'Easy',
               2:'Medium',
               3:'Hard'}

leetcode_session = "" # "yyy"
csrf_token = "" # "xxx"

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

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
print(api_instance.graphql_post(body=graphql_request))

# print all solved algorithm questions, fetch solved questions along with difficulty
api_response=api_instance.api_problems_topic_get(topic="all")
solved_questions=[]
counter = 0
for questions in api_response.stat_status_pairs:
    if questions.status=="ac":
       solved_questions.append(questions.stat.question__title)
    if counter <= 5:
        print(f'difficulty: ',DIFFICULTY[questions.difficulty.level])
        print(f'status: ',str(questions.status))
        counter += 1




print(solved_questions)
print("Total number of solved questions ",len(solved_questions))
#
# api_response=api_instance.api_problems_topic_get_with_http_info(num_solved)
# print(f'total unsolved: ', len(api_response.stat_status.pairs))
