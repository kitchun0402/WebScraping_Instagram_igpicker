# WebScraping_Instagram_igpicker <a href="https://pypi.org/project/igpicker/"><img src="https://img.shields.io/pypi/v/igpicker.svg" alt="latest release" /></a>

   
**Date for record: 6th October 2019 by Kenneth Hau**

**Renamed the package from igenemy to igpicker**

**Updated: Hashtag combination, Starting post**
## About
This is used to scrape images / videos from Instagam by using chrome driver.

By setting those parameters, you can easily scrape either images or videos or both as well as select your designated path to save them.

It will automatically create folders in a location where you stated in 'save_to_path'. Those folders are named by each username and hashtag.

Before scrapping, you will be informed to login your IG account in order to smoothen the scrapping process. Don't worry, it wouldn't store your username and password.
## Please follow the instructions below to install chrome driver on Colab
```
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!apt-get update
set chromedriver_path = 'chromedriver'
set chrome_headless = True
```
## Install
```
pip install igpicker
```
## Upgrade
```
pip install igpicker --upgrade
```
## Library used
selenium, bs4, time, getpass, IPython, urllib, os, re, tqdm, wget, ssl
## Reminder
Sometimes it may not run properly after an intensive scrapping. Please wait for a while and start your scrapping journey again.
## Limitations
- Only allows scrapping either by 'username' or 'hashtag' at the same time (but you can easily change 'target_is_hashtag' parameter after finishing your first scrapping)
- Only allows chromedriver
- Only allows to set the total number of posts you want
## Possible function that can be created in the future
Store each post's information (e.g. like, post time, post location, post description, users' number of followers, etc.) into dataframes, or even consolidate them into databases. Therefore, they can be used to do descriptive analysis, train up machine learning models or build up a recommendation system.  
## Parameters & Attributes
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
## Methods
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
## Import Library
```
from igpicker import IGpicker
```
## Example 1 (Normal flow):
```
igpicker = IGpicker(target = ['hkfoodtalk', 'sportscenter'], target_is_hashtag = False, chromedriver_path= './chromedriver',
         save_to_path = './', chromedriver_autoquit = False,
         chrome_headless= True, save_img=True, save_video=False, enable_gpu = False, 
         ipython_display_image = True)

chrome_driver = igpicker.login()

all_target = igpicker.scraper(chrome_driver = chrome_driver, num_post = 10, start_from = 1)

igpicker.close_driver(chrome_driver) #manually close if 'chromedriver_autoquit' is False
```
## Example 2 (Hashtag Combination):
```
igpicker = IGpicker(target = ['pizza'], target_is_hashtag = True, chromedriver_path= 'chromedriver',
       save_to_path = './', chromedriver_autoquit = False,
       chrome_headless= True, save_img=True, save_video=True, enable_gpu = False, 
       ipython_display_image = False)

chrome_driver = igpicker.login()

all_target = igpicker.scraper(chrome_driver = chrome_driver, num_post = 10, start_from = 10, hashtag_combination= ['cheesy', 'cheese'])
```
## Example 3 (Change attributes):
```
igpicker.save_to_path = '../' #change path

igpicker.target = ['burger', 'hkmusic','pasta'] #change target

igpicker.target_is_hashtag = True #is it "hashtag" page?

igpicker.save_video = True

igpicker.save_img = True

all_target = igpicker.scraper(chrome_driver = chrome_driver, num_post = 10) 
```
**You can run 'scraper' again after you change the parameters if you haven't closed the chrome driver.**
