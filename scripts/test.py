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
