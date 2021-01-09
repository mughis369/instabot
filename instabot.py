from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv 
import datetime


load_dotenv()
########## Change the below configuration variables

comments_list = ['Really cool!', 'Nice work ❤️', '👏👏', 'wow 👏', 'well said', 
            'so cool! 🙌', '❤️', 'lovely 😍', 'amazing 👌', 'amazing', 
            'wow ❤️', 'well said 👏', '👏👏👏👏', 'Nice!', 'nice 🔥',
            'feels good 😍', 'Good job! 😊', '❤️🔥🔥😍', 'thoughtful 👌', 'thatz deep',
            'intense 💯', '😊😊', 'i will take it as quote of the day','too much motivation 👌','very inspiring ❤️🔥'
            ]

total_posts = 5 # per user

########## Change above configuration variables


print('===>Script started!')

user_f = open('user_list.txt', 'r')
user_list = user_f.readlines()
user_f.close()

uname = os.environ.get('id')
pwd = os.environ.get('pass')

if (uname == None or pwd == None):
    print ('===>Failed! Create a file named .env if not already, and enter your login credentials in id and pass variables. Read the setup instructions for details')
    print('===>Exiting...')
    exit()

# else

print('===>Opening Browser')
# uncomment below line if you want to use chrome instead of firefox
# webdriver = webdriver.Chrome(executable_path=chromedriver_path)
webdriver = webdriver.Firefox(executable_path='./geckodriver')
webdriver.implicitly_wait(15) #will wait until the element appears: for all the elements we find below in the file
sleep(1)

print('===>Opening Instagram')
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(2)

print('===>Entering login details')
username = webdriver.find_element_by_name('username')
username.send_keys(uname) 
sleep(1)

password = webdriver.find_element_by_name('password')
password.send_keys(pwd) 
sleep(1)

button_login = webdriver.find_element_by_xpath("//div[text()='Log In']")
button_login.click()
sleep(randint(3,5))

try:
    print("===>Bypassing, saving info screen, if present")
    notnow = webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
    notnow.click() 
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print (message)
    pass

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for user in user_list:
    user = user.strip()
    print('===>On User: ', user)
    tag += 1
    webdriver.get('https://www.instagram.com/'+ user + '/')
    sleep(randint(2,4))
    try:
        
        #follow if not already following the user
        try:
            print('===>Following the user if we have follow button')
            button_follow = webdriver.find_element_by_xpath("//button[text()='Follow']")

            if button_follow.text == 'Follow' :
                print("===following user now in few seconds")
                sleep(randint(4,6))
                button_follow.click()
                followed += 1
            else: 
                print("===>No follow button available, so skipping the following")
        except:
            print("===>Follow button not availabe")

        #clicking the first picture
        first_thumbnail = webdriver.find_element_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
        print("===>Clicking first post of the user",user)
        first_thumbnail.click()
        sleep(randint(1,2))

        try:
            for x in range(1, total_posts+1):
                print('User: ', user, 'Post: ', x)

                # If we already like, then do nothing with the post, go to next post
                alreadyLike = webdriver.find_elements_by_xpath( "//section/span/button/div/span[*[local-name()='svg']/@aria-label='Like']")
                if len(alreadyLike) == 1:

                    # Liking the picture
                    print('===>Liking the picture')
                    sleep(randint(1,2))
                    button_like = webdriver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                    button_like.click()
                    likes += 1

                    # Comments and tracker
                    waitTime = randint(1,8)
                    print('===>So commenting')
                    sleep(randint(1,8))                                                    
                    webdriver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()
                    sleep(randint(2,4))
                    comment_box = webdriver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                    commentIndex = randint(0, len(comments_list)-1)
                    print('===>printing comment number {0}, which is {1}'.format(commentIndex+1, comments_list[commentIndex]))
                    comment_box.send_keys(comments_list[commentIndex])
                    sleep(1)
                    comment_box.send_keys(Keys.ENTER)
                    comments += 1
                    print('===>Commented! now waiting few seconds')
                    sleep(randint(3,6))
                else:
                    print('===>Post already liked, so skipping the post')

                # Next picture
                print('===>Moving next')
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(2,5))
            
        # Some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
        except Exception as ex:
            print ("An error occured: User has no posts")
            continue

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        continue

print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
