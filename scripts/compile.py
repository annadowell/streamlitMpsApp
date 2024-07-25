import pandas as pd

def load_data(url):
    data = pd.read_csv(url)
    return data

archive1 = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/mpsList2019.csv'
archiveMps = load_data(archive)

new1 = 'https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/MpsListNew.csv'
newMps = load_data(new)

Mpdataframes = [archiveMps, newMps]

CompiledMps = pd.concat(Mpdataframes)

# Save the concatenated DataFrame to a CSV file
CompiledMps.to_csv('CompiledMps.csv', index=False)
