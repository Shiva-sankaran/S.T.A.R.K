from Activities.Timetable.timetable import *
from Activities.Time_logger.timelogger import *
from threading import Thread
import schedule
import asyncio

version = "1.1.0v"



print("Running S.T.A.R.K {}\n\n".format(version))


t1 = Thread( target = time_logger)
t1.start()







everyday_act()
while True:
	q = input(" >>>")
	if(q == 'timetable'):
		show_timetable()
		print(schedule.get_jobs())
	elif(q == "free time"):
		print(show_free_time())
	elif(q == "timelogger"):
		summarize()



		

