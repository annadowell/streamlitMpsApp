#  money talks

https://moneytalks.streamlit.app

This app lets you find connections between the questions MPs ask and the donations they receive. The aim is to find out how loud money talks in the British parliament.

On screen, you will see a text input box. Input a list of keywords or phrases and hit the 'Submit' button. The app will search through all the registered questions, written or oral, asked by members of parliament since the beginning of the 2010 coalition government, and the money they have received. It will return a spreadsheet of members who have asked questions and received donations that include some or all of your keywords. 

For example, if I input a list of words related to the private rental industry such as: 'rent, renters, tenant, tenants, property, landlord, landlords, rent cap, property, lease, tenant responsibility' the machine will return a spreadsheet of many MPs who have asked questions related to the regulation and profitability of the rental market while also maintaining income from private rental properties themselves. Here it is easier to see how being a landlord might motivate the questions a member asks in parliament about landlording.

## The code

The front end of the app is created by the file streamlitapp.py. The code loads data about MPs' questions, (financial) interests, and party affiliation using links to csv files stored in the repository. The input box is generated at the bottom of the code, and it processes the list of words inputted into the most efficient format when you press submit. At that point, a function cross-references all the loaded data about 1. questions and 2. financial interests for the keywords you have entered.

The GitHub repository  doesn't just host the app, but refreshes the data the app is using. Money talks is built to continue to track the behaviour of MPs into the future, and to do so it needs to regularly update new questions and interests registered by members. 

The vast majority of questions and financial interests and MPs are from the 14 years before the 2024 parliament. To prevent continually searching for the same information, this data is stored in three CSV files labelled 2019. 

A NewData.yml file runs every Monday at three am and triggers the Python script NewData.py. This Python script calls four APIs that are maintained by the UK parliament.  

From one of these, it extracts a spreadsheet detailing all of the members who have served in parliament since its dissolution at the end of Sunak's government. From another, a spreadsheet is created detailing all of the  registered interests submitted by those members. Finally, from a combination of the API for oral questions and the API for written questions and motions, a spreadsheet is produced detailing all of the questions asked by those members as well as the date of asking and the answering member. These three spreadsheets are added to the GitHub repository and appear as csv files labelled "new".

Finally, the repository combines the archived data and the refreshed new data to create a compiled spreadsheet for the app to use. A workflow called compile.yml runs a Python script called compile.py. This loads the data from the new csv files and the archived csv files as pandas dataframes, and concatenates the various pairs. A command in the workflow then adds these compiled spreadsheets to the repository labelled "compiled".

The purpose of these workflows is to ensure the app can run quickly. Fetching this data from the parliamentary APIs takes a long time, and scheduling these updates and running the app simply with copies of this data allows the front end to be agile for the user. 
       
As the code is public, and there are public instructions from the parliament about its own API, it would be possible to modify the API calls to return more specific data covering, for example, the House of Lords or a particular party, or a particular period of time.  
       
However, Money Talks covers the 14 years of Conservative Party rule and the new Labour government across all parties in the House of Commons to understand the lobbying crisis in British politics and how or if it will change.
