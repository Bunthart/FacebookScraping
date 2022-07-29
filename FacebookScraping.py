#THIS CODE USE TO SCRAP PHOTO AND PICTURE ID FROM FACEBOOK

from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import time
from selenium import webdriver
from facebook_scraper import get_posts
import locale
import os
from selenium.common.exceptions import ElementClickInterceptedException
from PIL import Image
import io
import requests
import wget
from bs4 import BeautifulSoup
import pandas as pd

listposts = []
products=[] 
prices=[]
ratings=[] 
#RUN WEB
#DOWNLOAD CHROME DRIVER BEFORE RUN THIS SCRIPT
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
driver.get("https://www.facebook.com")
time.sleep(2)

#INERT SIGN ON FACEBOOK
email = ""
password = ""
txtEmail = driver.find_element_by_id('email')
txtEmail.send_keys(email)
txtPassword = driver.find_element_by_id('pass')
txtPassword.send_keys(password)
time.sleep(2)

#LOG IN TO FACEBOOK AS KHMER LANGUAGE
btnLogin = driver.find_element_by_xpath('//*[text()="ចូល"]')
btnLogin.click()
time.sleep(2)

#INSERT FACEBOOK PAGE LINK
driver.get("")

time.sleep(5)
images = [] 
captions = []
picIds = []
for j in range(0,100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    #target all the link elements on the page
    anchors = driver.find_elements_by_tag_name('a')
    linkVideo = driver.find_elements_by_tag_name('video')
    anchors = [a.get_attribute('href') for a in anchors]
    linkVideo =[a.get_attribute('src') for a in linkVideo]
    #narrow down all links to image links only
extendtion = ".jpg"
baseDir = os.getcwd()
baseDir = os.path.join(baseDir, "FB_SCRAPED")
for i, url in enumerate(anchors):
    if(url != None):
         if(url.find('fbid=') != -1):
            img = driver.get(url)
            time.sleep(2)
            content = driver.page_source
            soup = BeautifulSoup(content)
            links = driver.find_elements_by_tag_name('img')
            links = [a.get_attribute('src') for a in links]
            name = url.split('fbid=',1)
            file_name = name[1].split('&',1)
            file_name = file_name[0] + extendtion  
            for a in soup.findAll('div', attrs={'class':'a8nywdso j7796vcc rz4wbd8a l29c1vbm'}):
                status = a.find('span', attrs={'class':'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id'})
                if(status):
                    captions.append(status.text)
                    picIds.append(file_name)
            for j ,link in enumerate(links):
                try:
                    if(str(link) != '[]'):
                        image_content = requests.get(link).content
                    else:
                        continue
                except Exception as e:
                        print(f"ERROR - COULD NOT DOWNLOAD {link} - {e}")

                try:
                    image_file = io.BytesIO(image_content)
                    image = Image.open(image_file).convert('RGB')
                    
                    file_path = os.path.join(baseDir, file_name)
                    
                    with open(file_path, 'wb') as f:
                        image.save(f, "JPEG", quality=85)
                    print(f"SAVED - {link} - AT: {file_path}")
                except Exception as e:
                    print(f"ERROR - COULD NOT SAVE {url} - {e}")
            df = pd.DataFrame({'captions':captions,'PicId':picIds}) 
            df.to_csv('ResultScrape.csv', index=False, encoding='utf-16')