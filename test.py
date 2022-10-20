from Activities.PA.Alert import *
from inputimeout import inputimeout, TimeoutOccurred
import os
import random
import schedule
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date
import json
import hashlib


curr_date  =  date.today()
curr_day  = datetime.now().strftime("%A")
curr_date_str = datetime.strftime(curr_date,"%d-%m-%Y")

img_dir = "/home/shivasankaran/STARK/res/images/"

def_messages = {'water':['If there is magic on this planet, it is contained in water.','In time and with water, everything changes.','Thousands have lived without love, not one without water.',"Water is life's matter and matrix, mother and medium. \nThere is no life without water."],
'lunch':["All you need is love, but sometimes, a lunch break works, too.","Time for lunch!!","GTFO to lunch","??? I know ur hungry dont wait for the remainder"],
'snack':['Everyone I know is looking for solace, hope and a tasty snack.','The road to enlightenment is long and difficult, and you should try not to forget snacks and magazines.','Lets go eat a God damn snack'],
'dinner':['Time for the last meal of the day','Whats up for dinner?','Just go',"Should I drag u ??"],
'esrever':['Life is all about moving on','Its time','dont fall back','time for the next one']

}
def_timings = {
	'water':30,
	'lunch':'1:00 PM',
	'snack':'5:00 PM',
	'dinner':'8:30 PM'

}

def_title = {
	'water':'time for a sip',
	'lunch':'Lunch time !!!',
	'snack':'snack time !!!',
	'dinner':'dinner time !!!'


}

links = {
	'Computer Organization and Architecture': None,
	'Computer Organization and Architecture Tutorial': None,
	'World Civilizations and Cultures': None,
	'Discrete Mathematic':'https://meet.google.com/dse-gigw-xry',
	'Introduction to Materials': 'https://iitgn-ac-in.zoom.us/j/98304712675?pwd=OFBMSHJURmEyUUxTOFNkUTZIL0JpQT09',
	'Introduction to Materials Tutorial': 'https://iitgn-ac-in.zoom.us/j/94766609689?pwd=elpvVzE0S0hYamY3dVFRNjJCT3N4UT09',
	'Mathematics IV Tutorial':None,
	'Mathematics IV':None,
	'Data Structures and Algorithms II Tutorial': None,
	'Data Structures and Algorithms II':None,
	'Physics Lab':None


}
def intilise():
	
	tasks = get_todays_timetable()
	tasks = order_tasks(tasks)
	for (start_ti,end_ti),(task,category) in tasks.items():
		print("(",start_ti,"to",end_ti,") ",":-",task)
		Remind(category,task,start_ti)
	return tasks
		


def get_todays_timetable():
	d = get_academic_schedule()
	d2 = get_personal_timetable()
	d.update(d2)
	return d

	
def get_personal_timetable():
	d  = {}
	with open('/home/shivasankaran/ex_json2.txt', 'r') as infile:
		data = infile.read()
		json_data = json.loads(data)
	act_list = json_data['activities']
	for act in act_list:
		if(act['date'] == curr_date_str):
			if ((act['start time'],act['end time']), (act['task'],'esrever')) not in list(d.items()):
				print("adding task",act['task'])
				d[(act['start time'],act['end time'])] = (act['task'],'esrever')
			else:
				print(act['task'], 'already present \n')

	return d

def get_academic_schedule():
	academic_dict = {}
	timetable = pd.read_csv('/home/shivasankaran/schedule.csv',index_col = 0)

	timings = timetable.index.values

	i =0
	while i<len(timings):
		
		t = timings[i]
		if(isinstance(timetable[curr_day][t],str)):
			j = i
			while True:
				j = j+1
				if(j>=len(timings)):
					t2 = timings[-1]
					break
				t2 = timings[j]
				if(timetable[curr_day][t]!= timetable[curr_day][t2] or (not isinstance(timetable[curr_day][t2],str))):
					t2 = timings[j-1]
					break
		

			academic_dict[(t,(datetime.strptime(t2,"%I:%M %p") + timedelta(minutes=30)).strftime("%I:%M %p"))] = (timetable[curr_day][t],'esrever')
			i = j
		else:
			i = i+1
	return academic_dict


def time_converter_12to24(s,Min=0):
	in_time = datetime.strptime(s, "%I:%M %p")-timedelta(minutes=Min)
	out_time = datetime.strftime(in_time, "%H:%M")
	return out_time
def time_converter_24to12(s):
	d = datetime.strptime(s, "%H:%M")
	return d.strftime("%I:%M %p")

def everyday_act():
	Remind('water')
	Remind('lunch')
	Remind('snack')
	Remind('dinner')

def Remind(category,task = None,ti = None): 
	random.seed(datetime.now())
	catimg_path = img_dir +category
	messages = def_messages[category]
	image_paths = [catimg_path+'/'+ s for s in os.listdir(catimg_path)]
	message = random.choice(messages)
	image_path = random.choice(image_paths)
	if(category == 'esrever'):
		link = None
		if task in links.keys():
			link = links[task]
		
		schedule.every().day.at(time_converter_12to24(ti,Min = 15)).do(alert_popup,task,message,image_path,link) 


	else:
		t = def_timings[category]
		title = def_title[category]
		if category == 'water':
			schedule.every(t).minutes.do(alert_popup,title,message,image_path)
		else:
			schedule.every().day.at(time_converter_12to24(t,Min = 15)).do(alert_popup,task,message,image_path) 
	
def order_tasks(tasks):


	time_slots = list(tasks.keys())
	l=[]
	for i in range(len(time_slots)):
		l.append((time_converter_12to24(time_slots[i][0]),time_converter_12to24(time_slots[i][1])))
	l.sort()
	new_dict = {}
	for i in range(len(l)):
		new_dict[(time_converter_24to12(l[i][0]),time_converter_24to12(l[i][1]))] = tasks[(time_converter_24to12(l[i][0]),time_converter_24to12(l[i][1]))]
	return new_dict

def show_free_time(scheduled_tasks):
	filled_timeslots = list(scheduled_tasks.keys())
	free_slots = []
	for i in range(len(filled_timeslots)):
		if(i+1 >= len(filled_timeslots)):
			break
		else:
			if(filled_timeslots[i][1] != filled_timeslots[i+1][0]):
				free_slots.append((filled_timeslots[i][1],filled_timeslots[i+1][0]))
	return free_slots

print(curr_date_str,"!!!!")
everyday_act()
scheduled_tasks = intilise()

with open("ex_json2.txt", "rb") as f:
    old_hash = hashlib.md5(f.read()).hexdigest()
while True:
	query = None
	schedule.run_pending() 
	with open("ex_json2.txt", "rb") as f:
	    new_hash = hashlib.md5(f.read()).hexdigest()
	if new_hash!=old_hash:
		print("A new task has been added\n\n\n")
		schedule.clear()
		intilise()

	old_hash = new_hash

	time.sleep(10) 

So will the answer for Q3 be changed to "No"? As the empty set does not belong to 