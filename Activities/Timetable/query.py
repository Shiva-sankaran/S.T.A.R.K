from Activities.PA.Alert import *
import os
import random
import schedule
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date
import json
import hashlib



def write_json(to_add, filename='/home/shivasankaran/ex_json2.txt'): 

	with open(filename,'w') as f: 
		json.dump(to_add, f, indent=4)

def get_json_data(d,task,start_time,end_time):
	return {
			"date": d,
			"task": task,
			"start time": start_time,
			"end time":end_time
		}


def add_task(task,date_of_task,start_time,end_time):
	d = get_json_data(date_of_task,task,start_time,end_time)

	with open('/home/shivasankaran/ex_json2.txt') as json_file: 
	    data = json.load(json_file) 
	    temp = data['activities']
	    print(d)
	    if(d not in temp):
	    	temp.append(d)
	    	temp.append(d) 
	    	write_json(data)
	    else:
	    	print("already exisists")
	    

q = input(">>")
if(q=="add task"):
	task = input("task name:")
	date_of_task = datetime.strftime(datetime.strptime(input("date of task:"),"%d-%m-%Y"),"%d-%m-%Y")
	start_time = datetime.strftime(datetime.strptime(input("start time:"),"%I:%M %p"),"%I:%M %p")
	end_time  = datetime.strftime(datetime.strptime(input("end time:"),"%I:%M %p"),"%I:%M %p")
	#start_time = input("start time:")
	#end_time = input("end time:")
	add_task(task,date_of_task,start_time,end_time)
