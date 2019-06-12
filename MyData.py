from ApiCloud import ApiCloud
from CSVDump import *
from datetime import *
import time
import sys
import getpass
#Secret.py is a file with the client id and secret for the API
#Should be of the form:
#client_id = 'user@example.com'
#client_secret = 'longsecretkeyfromparrot'
from Secret import *

if sys.version_info[0] <3 :
   username=raw_input("Username: ")
else:
   username=str(input("Username:"))
password=getpass.getpass()


api = ApiCloud(client_id, client_secret)

if (api.login(username, password) == False):
   print "Logon failed"
   sys.exit()

if sys.version_info[0] <3 :
   numdays=int(raw_input("Number of Days: "))
else:
   numdays=int(str(input("Number of Days:")))

now = time.strftime("%d-%b-%Y %H:%M:%S")
twodays= datetime.now()- timedelta(days=numdays)
stwodays=twodays.strftime("%d-%b-%Y %H:%M:%S")
home = expanduser("~")
SummaryfileCsv = csv.writer(open(home+"/Desktop/"+username + ".csv", "w"))
dumpAllFlowerPower(api, username,stwodays,now)

if sys.version_info[0] <3 :
   blank=raw_input("Press Return to finish: ")
else:
   blank=str(input("Press Return to finish: "))

