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
2) ```python3 get_posts.py```

## Caution:-
This project violates [Linkedin's User Agreement Section 8.2](https://www.linkedin.com/legal/user-agreement),
and because of this, Linkedin may (and will) temporarily or permantly ban the account.So never a good choice to use the 
credentials of the LinkedIn Account you use often. Also from legal terms we cannot store the data provided by it.