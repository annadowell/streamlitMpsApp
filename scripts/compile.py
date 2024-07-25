import pandas as pd

def load_data(url):
    data = pd.read_csv(url)
    return data

archive = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/test.csv'
test1 = load_data(archive)

new = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/MpsListNew.csv'
test2 = load_data(new)

dataframes = [test1, test2]

test3 = pd.concat(dataframes)

# Save the concatenated DataFrame to a CSV file
test3.to_csv('test3.csv', index=False)
