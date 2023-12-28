import watchdog.events
import watchdog.observers
import time
from datetime import date

#global file_status
file_status = 0

class Handler (watchdog. events. PatternMatchingEventHandler) :
	def __init_(self):
    	#  Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*'], ignore_directories=True, case_sensitive=false)

def on_created(self, event):
	print("Watchdog received created event - % s." % event.src_path)
	# Event is created, you can process it now
	global file_status
	file_status = 1

def on_modified(self, event):
	print("Watchdog received modified event - % s."% event.src_path)
	# Event is modified, you can process it now
	global file_status
	file_status = 1


def readcsv():

	try:
		df=''
		today = date. today()
		Filename = '/home/william/Desktop/wso2am-4.0.0/repository/logs/http_access_.' + today.strftime('%Y-%m-%d') + '.log'
		with open(filename) as f:
			for line in f:
				if (line. find('/fileupload/toolsAny HTTP/1.1') > -1) or (line.find('/authenticationendpoint') > -1):

					content = line.split()
					print(line)
					df = content[o]

		return df

	except:
		return 'error'
