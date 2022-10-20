import speech_recognition as sr  
import pygame
import playsound
import time
from gtts import gTTS # google text to speech 
import os # to save/open files 
from selenium import webdriver # to control browser operations 
num = 1
pygame.init()
pygame.mixer.init()
def speak_out(file):
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
	print(pygame.mixer.get_busy())
	while pygame.mixer.get_busy() == 0:
		time.sleep(10)
		print("!!",pygame.mixer.get_busy())
	return
def tony_speaks(output):
	global num 
  
	# num to rename every audio file  
	# with different name to remove ambiguity 
	num += 1
	print("PerSon : ", output) 
  
	toSpeak = gTTS(text = output, lang ='en', slow = False) 
	# saving the audio file given by google text to speech 
	file = str(num)+".wav"  
	toSpeak.save(file) 
	  
	# playsound package is used to play the same file. 
	playsound.playsound(file, True)  
	os.remove(file) 

tony_speaks("Hello i am tony")