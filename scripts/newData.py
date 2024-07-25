import requests
import pandas as pd 

MpsDataframeImproved = []
MpsListImproved = []

def callApiForId(x):
    urlmembers = f'https://members-api.parliament.uk/api/Members/Search?House=1&MembershipInDateRange.WasMemberOnOrAfter=2024-06-29T00%3A00%3A00&skip={x}&take=20'
    reqids = requests.get(urlmembers, headers=my_ua)

    if reqids.status_code == 200:

        items = reqids.json().get('items', [])

        # If no items are returned, stop the recursion
        if not items:
            return

        # Process each item
        for item in items:
            member_id = item['value']['id']
            name = item['value']['nameListAs']
            party = item['value']['latestParty']['name']
            MpsDataframeImproved.append([member_id, party, name])
            MpsListImproved.append(member_id)
            
            # print(member_id)
        # Call the function recursively for the next set of results

        callApiForId(x + 20)

x = 0
my_ua = {'User-Agent': 'Your User Agent'}  # Replace with your actual user agent
callApiForId(x)


dfMpsDataframeImproved = pd.DataFrame(MpsDataframeImproved, columns = ['id', 'party_id', 'name'])

dfMpsDataframeImproved.to_csv('MpsListNew.csv', index=False)

# REGISTERED INTERESTS:
# this took 1 minute and 15 seconds on the notebook
all_party_interests = []

def LoadInterests():
    # Iterate through each id in the DataFrame
    for item in MpsListImproved:
        
        urlinterests = f'https://members-api.parliament.uk/api/Members/{item}/RegisteredInterests'
        reqinterests = requests.get(urlinterests)
        
        if reqinterests.status_code == 200:
            d = reqinterests.json()

            for x in d['value']:
                y = x['interests']
                for z in y:
                    int = z['interest']
                    small_list = [int, item]
                    all_party_interests.append(small_list)
        
        else:
            print(f"Failed to fetch data for ID {item}")

LoadInterests()
dfinterests = pd.DataFrame(all_party_interests, columns = ['interest', 'id'])
dfinterests.to_csv('InterestsNew.csv', index=False)

# QUESTIONS

big_list_questions = []


def CallingTheQuestions(id):

    # API for oral questions
    urlquestions = f'https://oralquestionsandmotions-api.parliament.uk/oralquestions/list?parameters.askingMemberIds={id}'
    req = requests.get(urlquestions, headers=my_ua)
    
    if req.status_code == 200:
        response_json = req.json()
        
        if 'Response' in response_json and response_json['Response'] is not None:
            for x in range(len(response_json['Response'])):
                try:
                    MemberID = response_json['Response'][x]['AskingMemberId']
                    questionAsked = response_json['Response'][x]['QuestionText']

                    small_list = [MemberID, questionAsked]
                    big_list_questions.append(small_list)
                except KeyError as e:
                    print(f"Key error: {e} for entry {x}")
                except Exception as e:
                    print(f"An error occurred: {e} for entry {x}")
        else:
            print(f"No 'Response' found for member ID {item}")
    else:
        print(f"Failed to fetch data for member ID {item} with status code {req.status_code}")

    # API for written questions
    urlwrittenquestions = f'https://members-api.parliament.uk/api/Members/{item}/WrittenQuestions'
    req2 = requests.get(urlwrittenquestions, headers=my_ua)

    if req2.status_code == 200:
        response_json = req2.json()

        if 'items' in response_json and response_json['items'] is not None:
            for x in range(len(response_json['items'])):
                try:
                    MemberID = response_json['items'][x]['value']['askingMemberId']
                    link = response_json['items'][x]['links'][0]['href']
                    url = f'{link}'
                    req4 = requests.get(url)
                    questionAsked = req4.json()['value']['questionText']
                    answeringName = req4.json()['value']['answeringBodyName']
                    date = req4.json()['value']['dateTabled']
                    answer = req4.json()['value']['answerText']

                    small_written_list = [MemberID, questionAsked, date, answeringName, answer]
                    big_list_questions.append(small_written_list)
                except KeyError as e:
                    print(f"Key error: {e} for entry {x}")
                except Exception as e:
                    print(f"An error occurred: {e} for entry {x}")
        else:
            print(f"No 'items' found for member ID {item}")
    else:
        print(f"Failed to fetch data for member ID {item} with status code {req2.status_code}")

for item in MpsListImproved:
    CallingTheQuestions(item)

dfquestions = pd.DataFrame(big_list_questions, columns=['id', 'question'])
dfquestions.to_csv('QuestionsNew.csv', index=False)
