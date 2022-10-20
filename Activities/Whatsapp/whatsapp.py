
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import cv2
import pytesseract as pyte
import os
import shutil
import selenium.webdriver.support.ui as ui

message = "This is a test message"
fp = webdriver.FirefoxProfile("/home/shivasankaran/S.T.A.R.K/Activities/Whatsapp/profile") # mzdir should be your profile directory
driver=webdriver.Firefox(fp)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 20) 
  
# Replace 'Friend's Name' with the name of your friend  
# or the name of a group  
target = '"Appa"'
  
# Replace the below string with your own message 
string = "Message sent using Python!!!"
  
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located(( 
    By.XPATH, x_arg))) 
time.sleep(2)
group_title.click() 
inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
input_box = wait.until(EC.presence_of_element_located(( 
    By.XPATH, inp_xpath))) 
print("!!!!!!")

input_box.send_keys(string + Keys.ENTER) 
time.sleep(1) 
'''
#wait.until(lambda driver: driver.find_element_by_id('pane-side'))
print("ready")
#target = '"Amma"'
x_arg = '//span[contains(@title,Amma)]'
group_title = wait.until(EC.presence_of_element_located(( By.XPATH, x_arg))) 

group_title.click() 

inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located(( By.XPATH, inp_xpath))) 
input_box.send_keys(message)


#/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[7]/div/div/div[2]
#/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[23]/div/div/div[2]
'''