import pickle
import speech_recognition as sr  # this gives waste error disable them first those alsa err that interferes with hotkey 
def get_audio(): 
  
    rObject = sr.Recognizer() 
    audio = '' 

    with sr.Microphone() as source: 
        rObject.adjust_for_ambient_noise(source,duration = 1)
        print("TALK")
        audio = rObject.listen(source, phrase_time_limit = 10)  
        print(audio)
        print("OVER")
  
    try: 
  
        text = rObject.recognize_google(audio, language ='en-US') 
        with open('STARK/logs/test1.txt', 'w') as f:
                    f.write(text)
                    print("Written success")
  
    except: 
  
        text = "Could not understand your audio, PLease try again !"
        with open('STARK/logs/test1.txt', 'w') as f:
                    f.write(text)
                    print("FAILED")

get_audio()

