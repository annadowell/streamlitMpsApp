import pandas as pd

def load_data(url):
    data = pd.read_csv(url)
    return data

#MPS
archive1 = 'https://github.com/annadowell/streamlitMpsApp/blob/main/mpsList14YearsofConservatives.xlsx'
archiveMps = load_data(archive1)

new1 = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/MpsListNew.csv'
newMps = load_data(new1)

Mpdataframes = [archiveMps, newMps]

CompiledMps = pd.concat(Mpdataframes)

# Save the concatenated DataFrame to a CSV file
CompiledMps.to_csv('CompiledMps.csv', index=False)

#INTERESTS

archive2 = 'https://github.com/annadowell/streamlitMpsApp/blob/main/mpsInterests14YearsofConservatives.xlsx'
archiveInterests = load_data(archive2)

new2 = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/InterestsNew.csv'
newInterests = load_data(new2)

Interestsdataframes = [archiveInterests, newInterests]

CompiledInterests = pd.concat(Interestsdataframes)

# Save the concatenated DataFrame to a CSV file
CompiledInterests.to_csv('CompiledInterests.csv', index=False)

#QUESTIONS

archive3 = 'https://github.com/annadowell/streamlitMpsApp/blob/main/mpsQuestions14YearsofConservatives.xlsx'
archiveQuestions = load_data(archive3)

new3 = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/QuestionsNew.csv'
newQuestions = load_data(new3)

Questionsdataframes = [archiveQuestions, newQuestions]

CompiledQuestions = pd.concat(Questionsdataframes)

# Save the concatenated DataFrame to a CSV file
CompiledQuestions.to_csv('CompiledQuestions.csv', index=False)
