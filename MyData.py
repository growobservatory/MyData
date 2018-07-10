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
api.login(username, password)

now = time.strftime("%d-%b-%Y %H:%M:%S")
twodays= datetime.now()- timedelta(days=30)
stwodays=twodays.strftime("%d-%b-%Y %H:%M:%S")

dumpAllFlowerPower(api, stwodays,now, )

if sys.version_info[0] <3 :
   blank=raw_input("Press Return to finish: ")
else:
   blank=str(input("Press Return to finish: "))

