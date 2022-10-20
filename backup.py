from Activities.PA.Alert import *
import os
import random
import schedule
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date
import json

curr_date  =  date.today()
curr_day  = datetime.now().strftime("%A")

version = "1.0.0v"
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
	'Discrete Mathematic':None,
	'Introduction to Materials': None,
	'Introduction to Materials Tutorial': None,
	'Mathematics IV Tutorial':None,
	'Mathematics IV':None,
	'Data Structures and Algorithms II Tutorial': None,
	'Data Structures and Algorithms II':None,
	'Physics Lab':None


}
def intilise():
	everyday_act()
	tasks = get_todays_timetable()
	tasks = order_tasks(tasks)
	for (start_ti,end_ti),(task,category) in tasks.items():
		print("(",start_ti,"to",end_ti,") ",":-",task)
		Remind(category,task,start_ti)
	return tasks
	#print(type(schedule.jobs),"!!!!!!!!!!!!!!!!!")
		


def get_todays_timetable():
	d = get_academic_schedule()
	with open('/home/shivasankaran/ex_json2.txt', 'r') as infile:
		data = infile.read()
		json_data = json.loads(data)
	act_list = json_data['activities']
	for act in act_list:
		if(act['date'] == curr_date):
			d[(act['start time'],act['end time'])] = (act['task'],'esrever')

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
					#print(timetable[curr_day][t]!= timetable[curr_day][t2],(not isinstance(timetable[curr_day][t2],str)))
					t2 = timings[j-1]
					break
		
			#print("(",t,"to",t2,") ",":-",timetable[curr_day][t])

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
	

	
intilise()
while True:
	schedule.run_pending() 
	time.sleep(10) 
