# InstaBot
An Instagram automation bot using Selenium. The bot can login, like, follow and comment on the posts

# Setup
- Install pip, it is used for downloading further python packages/libraries easily (you can install pip alongwith Python)
- Once you have pip, you need to install required libraries. Open command prompt or terminal depending on your OS, and run the following command
- There's a sample user_list attached, it contains usernames of the profiles bot would lookup and like, comment and follow. Format of the file should be single username per line. 

````
pip3 install selenium python-dotenv pandas

````
- Install Geckodriver from the drivers listed here. Here, we are using Firefox
- Optionally, change the configuration variables of number of posts you want to engage per user 
- Don't forget to change your instagram id and password in `.env` to add your credentials as shown below:
````
id='yourusername'
pass='yourpassword'
````
# Running the script
All set, open command prompt or terminal and run the following code, the bot will start its job
````
python3 instabot.py

````

# Contribution
If you would like to improve the script, feel free to create a pull request


