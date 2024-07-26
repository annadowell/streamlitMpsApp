#  money talks

 Welcome to my app that lets you find connections  between the questions members of parliament ask and the donations they receive.  The aim is to find out how loud money talks in the british parliament.

  On screen, you will see a text input box. Input a list of key words or phrases. My code will search through all of the registered questions, written or oral,  asked by members of parliament since the beginning of the 2010  coalition government, and the money they have received.  it will return a spreadsheet of members who have asked questions and received donations that include some or all of your keywords. 

   for example,  if I input a list of words related to the private rental industry such as: 'rent , renters , tenant , tenants , property , landlord , landlords , rent cap ,property , lease , tenant responsibility'  the machine will return a spreadsheet of many mps who  have asked questions related to the regulation and profitability of the rental market whilst also maintaining income from private rental properties themselves.  put beside one another, it is easier to see how being a landlord might be motivating the questions members ask about landlording in Parliament.

 explanation of the code:

  the front end of the app which you see is created by the file streamlitapp.py.  the code loads data about mps questions, interests, and party affiliation using links to csvs stored in the repository. The input box is generated at the bottom of the code, and it processes the list of words inputted into the most efficient format when you press submit. At that point, the cross-referencing function is triggered which cross-references all of the loaded data about questions and interests for the keywords you have inputted, and produces a downloadable spreadsheet to display on the website of the flagged MPs.

   However, the GitHub repository  doesn't just host the app, but refreshes the data the app is cross-referencing against. Money talks is built to continue to track the behaviour of members of parliament into the future, and to do so it needs to periodically add new questions and interests  registered by members now. 

    the vast majority of questions and interests and mps are from the 14 years before the current parliament. To prevent continually searching for the same information, these fourteen years of data are stored in three CSV files labelled 2019. 
     a yml  workflow file called NewData.yml  runs every Monday at three am.  it triggers the Python script NewData.py.  this Python script calls four APIs  run and maintained by the uk parliament.  from one of these, it extracts a  spreadsheet detailing all of the members who have served in parliament  since its dissolution at the end of Sunak's government.  from another aPI, a spreadsheet is created detailing all of the  registered interests submitted by those members. Finally, from a combination of the API for oral questions and the API for written questions and motions, a spreadsheet is produced detailing all of the questions asked by those members as well as the date of asking and the answering member. These three spreadsheets are added to the GitHub repository by a command in the workflow  and appear as csv files labelled new.
      finally,  the repository needs to combine the archived data and the refreshed new data  to create a compiled spreadsheet for the app to use. A workflow called compile.yml  runs a  Python script called compile.py. This loads the data from the new csv files and the archived csv files as pandas dataframes,  and concatenates the various pairs.  a command in the workflow then adds these compiled spreadsheets to the repository labelled compiled.

       the purpose of these ongoing workflows and compilations is to ensure that the app can run with speed. Fetching this complex data from the parliamentary apis takes a long time, and scheduling these updates and running the app simply with accessing public copies of this data, allows the front end to be agile for the user. 
       
       As the code is public, and there are public instructions from the parliament about its own api, it would be possible to modify the api calls to return more specific data for example covering the house of Lords, or a particular party, or a particular period of time.  
       
       however, money talks covers the fourteen years of conservative rule and the new labour government across all parties in the house of commons to understand the lobbying crisis in British politics and how or if it will change.
