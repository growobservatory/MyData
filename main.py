import mydata.api_cloud
import mydata.csv_dump
from datetime import *
import time
import sys
import getpass

# secret.py is a file with the client id and secret for the API
# Should be of the form:
# client_id = 'user@example.com'
# client_secret = 'longsecretkeyfromparrot'
from secret import *

if sys.version_info[0] <3 :
   username=raw_input("Username: ")
else:
   username=str(input("Username:"))

password=getpass.getpass()

api = mydata.api_cloud.ApiCloud(client_id, client_secret)
api.login(username, password)

now = time.strftime("%d-%b-%Y %H:%M:%S")
twodays= datetime.now()- timedelta(days=30)
stwodays=twodays.strftime("%d-%b-%Y %H:%M:%S")

mydata.csv_dump.dumpAllFlowerPower(api, stwodays, now)

if sys.version_info[0] < 3 :
   blank=raw_input("Press Return to finish: ")
else:
   blank=str(input("Press Return to finish: "))