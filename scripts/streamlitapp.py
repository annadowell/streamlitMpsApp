import streamlit as st
import pandas as pd
#from streamlit_gsheets import GSheetsConnection
import io

def load_data(url):
    data = pd.read_csv(url)
    return data

archive_questions_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/mpsQuestions2019.csv')
dfquestions = load_data(archive_questions_url)
#st.write(dfquestions)

archive_interests_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/mpsInterests2019.csv')
dfinterests = load_data(archive_interests_url)
#st.write(dfinterests)

archive_mps_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/mpsList2019.csv')
dfMpsDataframeImproved = load_data(archive_mps_url)
#st.write(dfMpsDataframeImproved)


archive = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/test.csv'
test1 = load_data(archive)

new = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/test2.csv'
test2 = load_data(new)

dataframes = [test1, test2]

test3 = pd.concat(dataframes)
st.write(test3)
# Save the concatenated DataFrame to a CSV file
#test3.to_csv('test3.csv', index=False)


# FILTERING FOR THE EXCEL READ DATA

# input whatever keywords you want to search in here

def CrossReferencing(keywords):
    
    dfquestions['question'] = dfquestions['question'].astype(str)
    dfinterests['interest'] = dfinterests['interest'].astype(str)
    dfquestions['question'] = dfquestions['question'].apply(lambda x: x.lower() if isinstance(x, str) else x)
    dfinterests['interest'] = dfinterests['interest'].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # this line creates a new dataframe filtering relevant qs
    gambling_questions = dfquestions[dfquestions.question.str.contains(keywords, case = False) == True]

    #  make a set of all the member ids of the questions in that dataframe
    question_member_ids = set(gambling_questions['id'].unique())

    # this line creates a filtered dataframe for interests
    gambling_interests = dfinterests[dfinterests.interest.str.contains(keywords, case = False) == True]

    # make a set of all the member ids of the interests in that dataframe
    gambling_member_ids = set(gambling_interests['id'].unique())

    # this finds the intersection, so the members who have both been flagged as talking about and receiving money from these areas
    common_member_ids = gambling_member_ids.intersection(question_member_ids)


    # slightly defamatory big list
    big_relevant_list =[]
    # looping through each member that has been flagged up by the cross-reference/intersection
    for item in common_member_ids:
        name_value = dfMpsDataframeImproved.loc[dfMpsDataframeImproved['id'] == item, 'name'].values[0]
        id = item

        # making a dataframe of this specific mps questions
        membersquestions = dfquestions.loc[dfquestions['id'] == item, 'question']
        membersquestionsdf = pd.DataFrame(membersquestions, columns = ['question'])

        # now filtering out all the questions this mp has asked for the ones which were flagged as including the keyword
        relevant_questions = membersquestionsdf[membersquestionsdf.question.str.contains(keywords, case = False) == True]
        # now turning that dataframe of relevant questions from that particular mp into a list
        relevantQuestionsList = relevant_questions['question'].tolist()

        # same deal but for the dataframe of interests 
        membersinterests = dfinterests.loc[dfinterests['id'] == item, 'interest']
        membersinterestdf = pd.DataFrame(membersinterests, columns = ['interest'])
        # filter for relevant
        relevant_interests = membersinterestdf[membersinterestdf.interest.str.contains(keywords, case = False) == True]
        # turn into a list
        relevantInterestsList = relevant_interests['interest'].tolist()

        # now putting all this information about this single mp into a list inside a big list
        big_relevant_list.append([id, name_value, relevantQuestionsList, relevantInterestsList])

    # turn this into a dataframe
    found_members_df = pd.DataFrame(big_relevant_list, columns = ['id', 'name', 'questions','interests'])
    st.write(found_members_df)
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        found_members_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Reset the buffer position to the beginning
    buffer.seek(0)

    # Create a download button for the Excel file
    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

input = st.text_input("Keywords: phrases or keywords separated by commas (no and), don't put any commas at the beginning or end of the string", "e.g. oil, gas, north sea, offshore energies uk")
def create_regex_pattern(words_list):
    pattern = '|'.join(rf'\b{word}\b' for word in words_list)
    return pattern

if st.button("Submit"):
    cleanseparates = [word.strip() for word in input.split(',')]
    keywords = create_regex_pattern(cleanseparates)
    CrossReferencing(keywords)




