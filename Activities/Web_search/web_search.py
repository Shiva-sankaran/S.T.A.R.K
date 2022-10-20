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
import wikipedia
def intialize_driver():
	fp = webdriver.FirefoxProfile("/home/shivasankaran/S.T.A.R.K/Selenium/profile")
	driver=webdriver.Firefox(fp)
	return(driver)
def basic_gsearch(search_string):
	driver = intialize_driver()
	driver.get("https://www.google.com/search?q={}".format(search_string))
	wait = WebDriverWait(driver, 20) 
def yt_search(search_string):
	driver = intialize_driver()
	driver.get("https://www.youtube.com/results?search_query={}".format(search_string))
def wiki_search(search_string,mode):
	if mode == 'summary':
		result = wikipedia.summary(search_string)
		return(result)
	elif mode == 'search':
		result = wikipedia.search(search_string)
		return(result)
	elif mode =='suggest':
		result = wikipedia.suggest(search_string)
		return(result)
	else:
		pass

search_string = "Arsenal team"
print(wiki_search(search_string,mode = 'page'))