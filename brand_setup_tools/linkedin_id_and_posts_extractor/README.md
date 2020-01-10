# ID Extractor
### Follow the commands to install the tool in your system:

1) ```python3 -m venv venv```
2) ```source ./venv/bin/activate```
3) The .gitignore file is already present in the folder which will protect the accidental committing of the venv folder
and credentials.json file. But in case you change the name of your virtual environment dont forget to put that name 
in your .gitignore file.
4) ###### The best would be to use virtualwrapper in order to avoid any accidental committing of venv (that could possibly happen in creating the virtual environment inside the repo.)
5) ```pip install -r requirements.txt```
6) ```python3 linkedin_id.py```
7) We are using the the linked account credentials which has been created specifically for this purpose and need to be 
configured in credentials.json file.

### Note: In case for some reason Linkedin block this account , a new account has to be setup.

# Posts Extractor:-
1) Assuming  the virtual environment has been setup and requirements has been installed by following the steps 1 to 3
 mentioned above in ID Extractor.
2) Maximum posts to be fetched has been set to latest `500` and this number can be changed by changing the constant `POSTS_MAX_RESULT` in constants.py
2) ```python3 get_posts.py```

# Engagements Extractor:- 
1) Assuming  the virtual environment has been setup and requirements has been installed by following the steps 1 to 3
 mentioned above in ID Extractor.
2) ```python3 linkedin_engagements.py```

# Web App:-
1) The tool can be accessed through webapp interface at : ```http://rss.concured.com:9090/linkedin_form```
2) On interface three services can be accessed, each being labelled under its title e.g : Fetch IDs, Fetch Posts and Fetch Engagements.
3) Fetch IDs can take company identifier which is either URN (e.g concured), URID(e.g 10036373) or Company's LinkedIn url(e.g ```https://www.linkedin.com/company/concured/``` )
4) Fetch Posts can take company identifier which is either URN (e.g concured), URID(e.g 10036373) or Company's LinkedIn url(e.g ```https://www.linkedin.com/company/concured/``` )
5) Fetch Engagements can take company identifier which is either URN (e.g concured), URID(e.g 10036373) or Company's LinkedIn url(e.g ```https://www.linkedin.com/company/concured/``` ) 
6) Fetch Engagements can compare the engagements of multiple companies and company identifiers  are provided separated by "," . E.g concured,deloitte,kpmg

## Caution:-
This project violates [Linkedin's User Agreement Section 8.2](https://www.linkedin.com/legal/user-agreement),
and because of this, Linkedin may (and will) temporarily or permantly ban the account.So never a good choice to use the 
credentials of the LinkedIn Account you use often. Also from legal terms we cannot store the data provided by it.