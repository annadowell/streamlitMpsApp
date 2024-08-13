#  Money Talks

[This app](https://moneytalks.streamlit.app) lets you find connections between the questions MPs ask and money they receive from outside parliament. The aim is to find out how loud money talks in the British parliament.

Input a list of keywords or phrases and hit enter. The app will search through all the registered questions (written or oral) asked by MPs since digital records began in 2014 and the money they have received since the beginning of the 2010 coalition government(recorded on the [Register of Members' Financial Interests](https://www.parliament.uk/mps-lords-and-offices/standards-and-financial-interests/parliamentary-commissioner-for-standards/registers-of-interests/register-of-members-financial-interests/)). It will return a spreadsheet of MPs who have asked questions and received money or gifts, related to some or all of your keywords. 

For example, if you input a list of words related to the private rental industry such as: 'rent, renters, tenant, tenants, property, landlord, landlords, rent cap, property, lease, tenant responsibility' the machine will return a spreadsheet of the MPs who have asked questions related to the regulation and profitability of the rental market while also maintaining income from private rental properties themselves. Here it is easier to see how being a landlord might motivate the questions a member asks in parliament.

## The code

The code loads data about MPs' questions, financial interests, and party affiliation using links to csv files stored in the repository. The front end of the app is created by the file streamlitapp.py. The input box is generated at the bottom of the code, and it processes the list of words inputted into the most efficient format when you press enter. At that point, a function cross-references all the loaded data about 1. questions and 2. financial interests for the keywords you have entered.

This GitHub repository  doesn't just host the app, but refreshes the data the app is using. Money Talks is built to continue to track the behaviour of MPs into the future, and to do so it needs to be regularly updated with new questions and interests registered by members. 

The vast majority of questions and financial interests and MPs are from the 14 years before the 2024 parliament. To avoid continually searching for the same information, this data is stored in three CSV files: mpsList14YearsofConservatives, mpsQuestions14YearsofConservatives and mySocietyArchiveGutted. The archive of members interests since 2010 was generated using mySociety's spreadsheet(https://pages.mysociety.org/parl_register_interests/datasets/all_time_register/latest). A NewData.yml file runs every Monday at three am and triggers the Python script NewData.py. This Python script calls four APIs that are maintained by the UK parliament.  

From one of these, it extracts a spreadsheet detailing all the members who have served in parliament after the end of Sunak's government. From another, a spreadsheet is created detailing all of the  registered interests submitted by those MPs from the parliamentary API containing this year's register of interests. Finally, from a combination of the API for oral questions and the API for written questions and motions, a spreadsheet is produced with all the questions asked by those MPs as well as the date of asking and the answering MP. These three spreadsheets are added to the GitHub repository and appear as csv files labelled "new".

Finally, the repository combines the archived data and the refreshed new data to create complete spreadsheets for the app to use containing both old and new data. A workflow called compile.yml runs a Python script called compile.py. This loads the data from the new csv files and the archived csv files as pandas dataframes, and concatenates the various pairs. A command in the workflow then adds these compiled spreadsheets to the repository labelled "compiled".

The purpose of these workflows is to ensure the app can run quickly. Fetching this data from the parliamentary APIs takes a long time, and scheduling these updates and running the app simply with copies of this data allows the front end to be agile for the user. 
       
As the code is public, and there are public instructions from the parliament about its own API, it would be possible to modify the API calls to return more specific data covering, for example, the House of Lords or a particular party, or a particular period of time.  
       
For now, Money Talks covers the 14 years of Conservative Party rule and the new Labour government across all parties in the House of Commons to understand the lobbying crisis in British politics and how or if it will change.
