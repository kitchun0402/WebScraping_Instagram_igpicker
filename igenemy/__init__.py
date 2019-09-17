from selenium import webdriver
from bs4 import BeautifulSoup
import time
from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from IPython.display import Image
from IPython.display import Video
from urllib.request import urlretrieve
import os
import re

class Igenemy:
    '''
    Date for record: 16th September 2019 by Kenneth Hau
    
    This is used to scrape images / videos from Instagam by using chrome driver.
    
    By setting those parameters, you can easily scrape either images or videos or both as well as select your designated path to save them.
    
    It will automatically create folders in a location where you stated in 'save_to_path'. Those folders are named by each username and hashtag
    
    Before scrapping, it will inform you to login your IG account in order to smoothen the scrapping process. Don't worry, it wouldn't store your username and password.
    
    ---------
    Library used:
    selenium, bs4, time, getpass, IPython, urllib, os, re
    
    --------- 
    Reminder:
    Sometimes it may not run properly after intensely scrapping. Please wait for a while and start your scrapping journey again.
    
    ---------
    Limitations:
    - Only allows scrape either by 'username' or 'hashtag' at the same time (but you can easily change 'target_is_hashtag' parameter after finishing your first scrapping)
    - Only allows chromedriver
    - Only allows to set the total number of posts you want
    
    ---------    
    Possible function that can be created in the future:
    Store each post's information (e.g. like, post time, post location, post description, users' number of followers, etc.) into dataframes, or even consolidate them into databases. Therefore, they can be used to do descriptive analysis, train up machine learning models or build up a recommendation system.
    
    
    ---------    
    Parameters & Attributes:
    (1) target : A list of string(s), default: []
            - either target username(s) or hashtag(s), if they are hashtags, 'target_is_hashtag' must be set to True
            
    (2) target_is_hashtag : Boolean, default: False
            - True: you want to scrape by using hashtags
            
    (3) chromedriver_path : String, default: './chromedriver'
            - a path of your chrome driver, you should name your driver as 'chromedrive'
    
    (4) save_to_path : String, default: '.'
            - a path where the image(s) / video(s) will be saved into
    
    (5) chromedriver_autoquit : Boolean, default: True
            - True: automatically quit the driver after finishing the scrapping
            - if you don't want it, you can quit the driver manually by using a build-in function called 'close_driver'
    
    (6) chrome_headless : Boolean, default: True
            - True: run chrome driver in the backend
            - if you want to see how the chrome driver works, you can set it to False
    
    (7) save_img : Boolean, default: True
            - True: save images
    
    (8) save_video : Boolean, default: False
            - True: save videos      
    
    (9) enable_gpu : Boolean, default: False
            - True: enable gpu in chrome driver
    
    (10) ipython_display_image : Boolean, default: False
            - True: display images, only works in notebook but not terminal
            - if you set True when using terminal to display, it will fail to scrape images
    
    ---------  
    Methods:
    (1) login : no parameter is required, return chrome_driver
            - used to access Instagram
            
    (2) scraper : two parameters (chrome_driver, num_post), return a list of all targeted url
    
        (a) chrome_driver : Selenium Webdriver
            - used for web scrapping

        (b) num_post : int, default: 10
            - the total number of posts you want to scrape
            - if this number is beyond the actual number of posts, it will stop scrapping automatically
            
    (3) close_driver : one parameters (chrome_driver)
            - manually close the web driver
    
    ---------
    Example 1 (Normal flow):
    
    igenemy = Igenemy(target = ['hkfoodtalk', 'sportscenter'], target_is_hashtag = False, chromedriver_path= './chromedriver',
                  save_to_path = './', chromedriver_autoquit = False,
                  chrome_headless= True, save_img=True, save_video=False, enable_gpu = False, 
                  ipython_display_image = True)
    
    chrome_driver = igenemy.login()
    
    all_target = igenemy.scraper(chrome_driver = chrome_driver, num_post = 10)
    
    igenemy.close_driver(chrome_driver) #manually close if 'chromedriver_autoquit' is False
    

    Example 2 (Change attributes):
    
    igenemy.save_to_path = '../' #change path
    
    igenemy.target = ['burger', 'hkmusic','pasta'] #change target
    
    igenemy.target_is_hashtag = True #is it "hashtag" page?
    
    igenemy.save_video = True
    
    igenemy.save_img = True
    
    all_target = igenemy.scraper(chrome_driver = chrome_driver, num_post = 10) 
    
    #you can run 'scraper' again after you change the parameters if you didn't close the chrome driver.
    
    '''

    def __init__(self, target = [], target_is_hashtag = False, chromedriver_path = './chromedriver', 
                 save_to_path = '.', chromedriver_autoquit = True, chrome_headless = True, save_img = True,
                 save_video = False, enable_gpu = False, ipython_display_image = False):
        if type(target) != list or len(target) == 0:
            raise ValueError('"target" must be a list and at least contains 1 target')
        else:
            self.target = target
            
        if  not os.path.exists(chromedriver_path) or re.search(r'chromedriver$', 'chromedriver_path'):
            raise FileNotFoundError('"chromedriver_path" is a invalid path, e.g "./chromedriver"')
        else:
            self.chromedriver_path = chromedriver_path
        
        if type(target_is_hashtag) != bool:
            raise ValueError('"target_is_hashtag" must be a boolean')
        else:
            self.target_is_hashtag = target_is_hashtag
            
        if  not os.path.exists(save_to_path):
            raise FileNotFoundError('"save_to_path" is a invalid path')
        else:
            self.save_to_path = save_to_path.rstrip('/')
        
        if type(chromedriver_autoquit) != bool:
            raise ValueError('"chromedriver_autoquit" must be a boolean')
        else:
            self.chromedriver_autoquit = chromedriver_autoquit
        
        if type(chrome_headless) != bool:
            raise ValueError('"chrome_headless" must be a boolean')
        else:
            self.chrome_headless = chrome_headless
        
        if type(save_img) != bool:
            raise ValueError('"save_img" must be a boolean')
        else:
            self.save_img = save_img

        if type(save_video) != bool:
            raise ValueError('"save_video" must be a boolean')
        else:
            self.save_video = save_video
        
        if type(enable_gpu) != bool:
            raise ValueError('"enable_gpu" must be a boolean')
        else:
            self.enable_gpu = enable_gpu
       
        if type(ipython_display_image) != bool:
            raise ValueError('"ipython_display_image" must be a boolean')
        else:
            self.ipython_display_image = ipython_display_image
        
            
    def login(self):
        chrome_driver= self.activate_driver()
        user, password = self.click_login_icon(chrome_driver)
        user_name, pwd = self.username_password(user, password, chrome_driver)
        login_check = False
        login_loop = 0
        while login_check == False and login_loop <= 2:
            login_loop += 1
            try:
                err_msg = chrome_driver.find_element_by_css_selector('.eiCW- #slfErrorAlert')
            except:
                login_check = True
                break
            else:
                print(f"\nAttempt {login_loop}: {[err_msg.text]}") #return the error msg inside the tag, incorrect password or name

                for i in range(len(user_name)):
                    user.send_keys(Keys.BACKSPACE)

                for i in range(len(pwd)): #macbook cannot use Keys.COMMAND !!!
                    password.send_keys(Keys.BACKSPACE)
                time.sleep(0.2)
                user_name, pwd = self.username_password(user, password, chrome_driver)
        else:
            print("\n[Failed]")
            chrome_driver.quit()
            print('\nChromedriver is Closed')
   
        if login_check == True:
            sc_check = self.security_code(chrome_driver)
#             if sc_check == True:
#                 self.scraper(chrome_driver)              
        else:
            print('\n[Nothing happened]')
        return chrome_driver
        
           
        
    def activate_driver(self):
        if self.chrome_headless:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            if self.enable_gpu:
                chrome_options.add_argument('disable--gpu')
            print('[Chrome Driver is now in headless mode]\n')
        else:
            chrome_options = Options()
        print('Opening Chrome Broswer')
        time.sleep(1.5)
        chrome_driver = webdriver.Chrome(self.chromedriver_path, options = chrome_options)
        chrome_driver.get('https://www.instagram.com/accounts/login')
#         html_ = chrome_driver.page_source
#         soup = BeautifulSoup(html_, 'html.parser')
        print('\nSuccessful')
        return chrome_driver
    
    def click_login_icon(self, chrome_driver):
#         click_login = chrome_driver.find_element_by_css_selector('.tdiEy button')
#         click_login.click()

        time.sleep(1.5)

        user = chrome_driver.find_element_by_name('username')
        user.clear()

        password = chrome_driver.find_element_by_name('password')
        password.clear()
        
        return user, password
        
        
    def username_password(self, user, password, chrome_driver):
        
        user_name = input("\nUsername: ")
        user.send_keys(user_name)

        pwd = getpass("\nPassword: ")
        password.send_keys(pwd)

        submit_button = chrome_driver.find_element_by_tag_name('button')
        submit_button.submit()
        print("\nLoading.........")
        time.sleep(1)
        print("\nLoading.........")
        time.sleep(1)
        print("\nLoading.........")
        time.sleep(1)
        return user_name, pwd


        
    def security_code(self, chrome_driver):
        try:
            time.sleep(2)
            err_msg2 = chrome_driver.find_element_by_class_name('O4QwN').text
            print(f'\n[{err_msg2}]') #Suspicious Login Attempt
            print('\nYou will receive a notification email from Instagram in no time. Please Check!')
            chrome_driver.find_element_by_css_selector('button._5f5mN.jIbKX.KUBKM.yZn4P').click() #send security code
            print("\nLoading.........")
            time.sleep(0.5)
            print("\nLoading.........")
            time.sleep(1.0)
            print("\nLoading.........")
            time.sleep(1.0)

            security_code = chrome_driver.find_element_by_name('security_code') #the place where 
            security_code.clear() #clear output

            sc_check = False
            sc_loop = 0
            while sc_check == False and sc_loop <= 2:
                sc_loop += 1
                sc = getpass("\nSecurity Code (6 digits) sent to your desingated email: ")
                if len(sc) == 6:
                    security_code.send_keys(sc) #send security code, 6 digits only
                    chrome_driver.find_element_by_css_selector('button._5f5mN.jIbKX.KUBKM.yZn4P').click() #submit button
                    print("\nLoading.........")
                    time.sleep(2)
                    print("\nLoading.........")
                    time.sleep(2)
                    print("\nLoading.........")
                    time.sleep(1)

                    try:
                        err_msg3 = chrome_driver.find_element_by_css_selector('#form_error p').text
                        print(f"\n[Attempt {sc_loop}: {err_msg3}]")
                        time.sleep(0.3)
                        for i in range(len(sc)): #macbook cannot use Keys.COMMAND !!!
                            security_code.send_keys(Keys.BACKSPACE)
                    except:
                        sc_check = True
                        print('\n[Successfully Login!]')
                        break
            else:
                print("\n[Failed]")
                chrome_driver.quit()
                print('\nChromedriver is Closed')

        except:
            print('\n[Successfully Login!]')
            sc_check = True
        return sc_check
            
    def scraper(self, chrome_driver, num_post = 10):
        """
        Parameters:
        (1) chrome_driver : Selenium Webdriver
                - used for web scrapping
                
        (2) num_post : int, default: 10
                - the total number of posts you want to scrape
                - if this number is beyond the actual number of posts, it will stop scrapping automatically
                
        """
        if type(num_post) != int:
            raise ValueError("'num_post' must be an integer")
        all_target = []
        for t in self.target: #loop thru each url
            if self.target_is_hashtag:
                target_url = 'https://www.instagram.com/explore/tags/' + t
                all_target.append(target_url)
            else:
                target_url = 'https://www.instagram.com/' + t
                all_target.append(target_url)
            chrome_driver.get(target_url)
            time.sleep(2)
            html_ = chrome_driver.page_source
            soup = BeautifulSoup(html_, 'html.parser')
            
            if not os.path.exists(f'{self.save_to_path}/{t}'):
                os.mkdir(f'{self.save_to_path}/{t}') #create new directory according to the username or tag name
            checker = []
            start_post = 1
            while True:
                posts = chrome_driver.find_elements_by_css_selector('.Nnq7C div.v1Nh3.kIKUG._bz0w div._9AhH0') #(find the frame) return a list, show each post
                end_post = len(posts)
                print(f'\n-------------\n[Target: {t}]\n-------------\n')
                time.sleep(1)
#                 print(len(checker))
#                 print(start_post)
#                 print(end_post)
                html_changed_for_checking = chrome_driver.page_source #check if we ara at the bottom of the page. Then, stop scraping
                chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #scroll down the page
                time.sleep(1.5)

                for post in range(0, len(posts)): #must be started from 0 due to IG structure
            #         print(print(posts[post]))
                    if posts[post] not in checker:
                        repeater=0
                        trigger = True #prevent the driver from not loading the page source successfully

                        while trigger == True:
                            try:
                                posts[post].click() #go into a post
                                checker.append(posts[post])
                                trigger = False
                            except:
                                print(f'failed {repeater + 1}\n-------------')
                                repeater += 1
                                if repeater == 3:
                                    break
                                time.sleep(0.3)
                                html_changed = chrome_driver.page_source #load the page source again
                                soup_changed = BeautifulSoup(html_changed, "html.parser")
                                
                    else:
                        continue #skip the post that already existed

                    time.sleep(0.5)
                    html_changed = chrome_driver.page_source #update page_source after clicking into the post
                    soup_changed = BeautifulSoup(html_changed, "html.parser")
                    print(f"--------\n[Post: {len(checker)}]")

                    repeater=0
                    trigger = True #prevent the driver from not loading the page source successfully
                    while trigger == True:
                        try:
                            posttime = soup_changed.select('.c-Yi7 time')[0]['datetime'] #show posting time
                            print(posttime)
                            trigger = False
                        except:
                            print(f'failed {repeater + 1}\n-------------')
                            repeater += 1
                            if repeater == 3:
                                posttime = 'na'
                                break
                            time.sleep(0.5)
                            html_changed = chrome_driver.page_source #load the page source again
                            soup_changed = BeautifulSoup(html_changed, "html.parser")
                            

                    posttime = posttime.replace(':', '_') #replace : to _, so that the image can be saved
                    if soup_changed.select('._97aPb .YlNGR li') != []: #if more than 1 pics,  there are 'li' tags
                        print('More than 1 items')
                        for pic in range(len(soup_changed.select('._97aPb .YlNGR li'))): 
                            #loop thru each pic in the post, keep updating 'html'
                            if soup_changed.find(name = 'button', class_ = "_6CZji") != None: #check if there is 'next' button
                                try:
                                    chrome_driver.find_element_by_css_selector('.coreSpriteRightChevron').click() #click it
                                    time.sleep(0.3)
                                    html_changed = chrome_driver.page_source #load the page source after turning to next pic in the same post
                                    time.sleep(0.3)
                                    soup_changed = BeautifulSoup(html_changed, "html.parser")
                                except:
                                    print('\nThere is no "next" button\n')
                            
                            try:
                                if soup_changed.select('._97aPb .YlNGR li')[pic].find("video") == None: #exclude videos
                                    print(f"Item: {pic + 1}")
                                    if self.save_img:
                                        img_url = soup_changed.select('._97aPb .YlNGR li')[pic].find("img")['src']
                                        if self.ipython_display_image:
                                            display(Image(url = img_url,  width = 100))
                                        urlretrieve(img_url, f'{self.save_to_path}/{t}/{posttime}_{pic}.jpg')
                                    else:
                                        print('\n[Skipped]\n')
                                        continue
                                else:
                                    print(f"Item: {pic + 1}, this is a video")
                                    if self.save_video:
                                        for v in range(3): #prevent the driver from not loading the page source successfully
                                            video_url = soup_changed.select('._97aPb .YlNGR li')[pic].find("video")['src']
                                            if video_url == None:
                                                time.sleep(0.2)
                                                html_changed = chrome_driver.page_source #load the page source after turning to next pic in the same post
                                                time.sleep(0.2)
                                                soup_changed = BeautifulSoup(html_changed, "html.parser")
                                                print('\nNo url')
                                            else:
                                                print(video_url)
                                                urlretrieve(video_url, f'{self.save_to_path}/{t}/{posttime}_{pic}.mp4')
                                                break


                            except:
                                print(f"Item: {pic + 1}")
                                print('failed\n-------------')


                    else:
                        print("Only 1 item")
                        if soup_changed.select('.PdwC2._6oveC.Z_y-9 ._5wCQW') == []:
                            repeater = 0
                            trigger = True #prevent the driver from not loading the page source successfully
                            while trigger == True: 
                                try:
                                    print(f"Item: 1")
                                    if self.save_img:
                                        result = soup_changed.select('.PdwC2._6oveC.Z_y-9 .KL4Bh img.FFVAD')[0] #only 1 pic there
                                        if self.ipython_display_image:
                                            display(Image(url = result['src'], width = 100))#show the image
                                        urlretrieve(result['src'], f'{self.save_to_path}/{t}/{posttime}.jpg') #save the image into jpg format
                                        trigger = False
                                    else:
                                        print('\n[Skipped]\n')
                                        break
                                except:
                                    print(f'failed {repeater + 1}\n-------------')
                                    repeater += 1
                                    if repeater == 3:
                                        break
                                    time.sleep(0.5)
                                    html_changed = chrome_driver.page_source #load the page source again
                                    soup_changed = BeautifulSoup(html_changed, "html.parser")
                                    

                        else:
                            print('This post only contains video(s)\n-------------')
                            if self.save_video:
                                result = soup_changed.select('.PdwC2._6oveC.Z_y-9 ._5wCQW video')[0]['src']
                                print(result)
                                urlretrieve(result, f'{self.save_to_path}/{t}/{posttime}.mp4')
    #                             time.sleep(0.3)


                    time.sleep(0.3)
                    repeater = 0
                    trigger = True #prevent the driver from not loading the page source successfully
                    while trigger == True:
                        try:
                            chrome_driver.find_element_by_css_selector('.ckWGn').click() #click the "x" at the right corner
                            trigger = False
                        except:
                            print(f'failed {repeater + 1}\n-------------')
                            repeater += 1
                            if repeater == 3:
                                break
                                
                            time.sleep(0.5)
                            html_changed = chrome_driver.page_source #load the page source again
                            soup_changed = BeautifulSoup(html_changed, "html.parser")
                            


                    if len(checker) == num_post: #limit to 50 posts, break for loop
                        break

                if len(checker) == num_post: #break while loop
                    print(f"Finished: {len(checker)} post(s)")
                    break



                start_post = end_post + 1
                
                time.sleep(1.5)
                html_changed = chrome_driver.page_source #update page_source after going back to the home page
                
                
                if html_changed == html_changed_for_checking:
                    print(f"Last Post: {len(checker)}")
                    break
                soup_changed = BeautifulSoup(html_changed, "html.parser")
            
        if self.chromedriver_autoquit: #auto close
            chrome_driver.quit()
            print('\nChromedriver is Closed')
        return all_target
    
    def close_driver(self, chrome_driver): #manually close
        try:
            chrome_driver.quit()
            print('\nChromedriver is Closed')
        except:
            print('\nChromedriver is Closed')
