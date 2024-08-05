import streamlit as st
import pandas as pd
import io
import xlsxwriter

st.title('Money Talks')
st.write('This app lets you find connections between the questions MPs ask and money they receive outside parliament. The aim is to find out how loud money talks in the British parliament.')

def load_data(url):
    data = pd.read_csv(url)
    return data

archive_questions_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/CompiledQuestions.csv')
dfquestions = load_data(archive_questions_url)
#st.write(dfquestions)

archive_interests_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/CompiledInterests.csv')
dfinterests = load_data(archive_interests_url)
#st.write(dfinterests)

archive_mps_url = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/CompiledMps.csv')
dfMpsDataframeImproved = load_data(archive_mps_url)
#st.write(dfMpsDataframeImproved)


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
        party = dfMpsDataframeImproved.loc[dfMpsDataframeImproved['id'] == item, 'party'].values[0]
        
        # making a dataframe of this specific mps questions
        membersquestions = dfquestions.loc[dfquestions['id'] == item]
        membersquestionsdf = pd.DataFrame(membersquestions, columns = ['question', 'date','answeringMember', 'answer'])

        # now filtering out all the questions this mp has asked for the ones which were flagged as including the keyword
        relevant_questions = membersquestionsdf[membersquestionsdf.question.str.contains(keywords, case = False) == True]
        # now turning that dataframe of relevant questions from that particular mp into a list
        relevantQuestionsList = relevant_questions['question'] + relevant_questions['date'] + 'The Answer:' +relevant_questions['answeringMember'] + relevant_questions['answer']
        MpsQs = relevantQuestionsList.tolist()

        # same deal but for the dataframe of interests 
        membersinterests = dfinterests.loc[dfinterests['id'] == item]
        membersinterestdf = pd.DataFrame(membersinterests, columns = ['interest', 'date'])
        # filter for relevant
        relevant_interests = membersinterestdf[membersinterestdf.interest.str.contains(keywords, case = False) == True]
        # turn into a list
        relevantInterestsList = relevant_interests['interest'] +relevant_interests['date']
        MpsInterests = relevantInterestsList.tolist()

        # now putting all this information about this single mp into a list inside a big list
        big_relevant_list.append([id, name_value, party, MpsQs, MpsInterests])

    # turn this into a dataframe
    found_members_df = pd.DataFrame(big_relevant_list, columns = ['id', 'name', 'party', 'questions','interests'])
    
    st.dataframe(
        data = found_members_df, 
        column_config={
        "id": st.column_config.NumberColumn(
            "Member's ID",
            width="small", 
            ),
        "name": st.column_config.TextColumn(
            "Name",
            width="small", 
            ),
        "party": st.column_config.TextColumn(
            "Party",
            width="small", 
            ),
        "questions": st.column_config.TextColumn(
            "Questions",
            width="large", 
            ),
        "interests": st.column_config.TextColumn(
            "Interests",
            width="large", 
            ),
        },
        hide_index=True, 
    )
    
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

input = st.text_input("Keywords or phrases separated by commas:", "rent, renters, tenant, tenants, property, landlord, landlords, rent cap, property, lease, tenant responsibility")
def create_regex_pattern(words_list):
    pattern = '|'.join(rf'\b{word}\b' for word in words_list)
    return pattern

if st.button("Submit"):
    cleanseparates = [word.strip() for word in input.split(',')]
    keywords1 = create_regex_pattern(cleanseparates)
    keywords = keywords1.lower()
    CrossReferencing(keywords)

st.link_button("About", "https://github.com/annadowell/streamlitMpsApp?tab=readme-ov-file#money-talks")



