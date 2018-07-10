from ApiCloud import ApiCloud
from CSVDump import *
from datetime import *
import time
import sys
# First we set our credentials
from Secret import *

username = 'andy@r2-dvd.org'
password = '3ur0R8ck!'

api = ApiCloud(client_id, client_secret)
api.login(username, password)

now = time.strftime("%d-%b-%Y %H:%M:%S")
twodays= datetime.now()- timedelta(days=30)
stwodays=twodays.strftime("%d-%b-%Y %H:%M:%S")

dumpAllFlowerPower(api, stwodays,now, )
