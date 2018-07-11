from datetime import *
from time import sleep
import csv
import json
import sys

dateFormat = "%d-%b-%Y %H:%M:%S"

def dumpAllFlowerPower(api_service, since="born", until="today"):
  """
  Loops over the available locations (aka sensors) and 
  collect data for output.
  """
  status  = api_service.getSensorStatus()

  sensorDataSync = api_service.getSensorDataSync()

  if not sensorDataSync:
    sys.exit("Error authenticating with the parrot API")

  for location in sensorDataSync["locations"]:
    err = dumpFlowerPower(api, location, since, until)
    
    if (err == -1):
      print ("Your 'Since' date is after your 'Until' date !?")
      break 

def dumpFlowerPower(api, location, since, until):
  meta = {}

  if (until == "today"):
    until = datetime.today()
  else:
    until = datetime.strptime(until, dateFormat)
  
  if (since == "born"):
    since = until - timedelta(days=7)
  else:
    since = datetime.strptime(since, dateFormat)

  if (since > until):
    return -1
      
  meta["latitude"] = location['latitude']
  meta["longitude"] = location['longitude']
  meta["Type"] = "FlowerPower"
  meta["Is_indoor"] = location['is_indoor']
  meta["In Pot"] = location['in_pot']
  meta["Avatar"] = location['avatar_url']

   
  if location['sensor']:
    fileCsv = csv.writer(open(location['sensor']['sensor_identifier'] + ".csv", "w"))
    fileCsv.writerow(["capture_datetime_utc", "fertilizer_level", "light", "soil_moisture_percent", "air_temperature_celsius"])
    
    while (since < until):
      samplesLocation = api.getSamplesLocation(location['location_identifier'], since, since + timedelta(days=7))

      if (len(samplesLocation["errors"])):
        continue
            
      for sample in samplesLocation['samples']:
        sensor_data = {}
        arr = []
        
        sensor_data["device"] = location['sensor']['sensor_serial']
        
        capture_datetime_utc = sample["capture_datetime_utc"].replace("T", " ").replace("Z", "")
        sensor_data.update({"insertion_time":capture_datetime_utc})
        fertilizer_level = sample["fertilizer_level"]
        soil_moisture_percent = sample["soil_moisture_percent"]
        air_temperature_celsius = sample["air_temperature_celsius"]
        light = sample["light"]

        fileCsv.writerow([capture_datetime_utc, fertilizer_level, light, soil_moisture_percent, air_temperature_celsius])
        
        arr.append({"name":"fertilizer_level", "fValue":fertilizer_level})
        arr.append({"name":"soil_moisture_percent", "fValue":soil_moisture_percent})
        arr.append({"name":"air_temperature_celsius", "fValue":air_temperature_celsius})
        arr.append({"name":"light", "fValue":light})
        
        a=json.dumps({"SensorData":sensor_data, "meta":meta, "sensors":arr})

      since += timedelta(days=7)
        
    return 0
