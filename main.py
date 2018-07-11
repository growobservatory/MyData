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

# get user credentials
if sys.version_info[0] <3 :
   username=raw_input("Username: ")
else:
   username=str(input("Username:"))

password=getpass.getpass()

# authenticate with parrot
api_service = mydata.api_cloud.ApiCloud(client_id, client_secret)
api_service.login(username, password)

# set start and end date to use for querying data
now = time.strftime("%d-%b-%Y %H:%M:%S")
twodays= datetime.now()- timedelta(days=30)
stwodays=twodays.strftime("%d-%b-%Y %H:%M:%S")

# output fetched data to csv file  
mydata.csv_dump.dumpAllFlowerPower(api_service, stwodays, now)

# finish
if sys.version_info[0] < 3 :
   blank=raw_input("Press Return to finish: ")
else:
   blank=str(input("Press Return to finish: "))