from ApiCloud import ApiCloud
from datetime import *
from time import sleep
import csv
import json
import socket
import uuid
from os.path import expanduser

dateFormat = "%d-%b-%Y %H:%M:%S"

def dumpAllFlowerPower(api, account,since="born", until="today"):
    status  = api.getSensorStatus()

    sensorDataSync = api.getSensorDataSync()
#    print json.dumps(sensorDataSync,indent=4,sort_keys=True)     
    for location in sensorDataSync["locations"]:
        err = dumpFlowerPower(api, location, since, until,account)
        if (err == -1):
            print ("Your 'Since' date is after your 'Until' date !?")
            break ;


def dumpFlowerPower(api, location, since, until,account):
    meta=dict()
    if (until == "today"):
        until = datetime.today()
    else:
        until = datetime.strptime(until, dateFormat)
    if (since == "born"):
        since = until - timedelta(days=7)
    else:
        since = datetime.strptime(since, dateFormat)
    now = until.strftime("%d-%b-%Y")
    print (location['latitude'])
    print (location['longitude'])
    meta.update({"latitude":location['latitude']})
    meta.update({"longitude":location['longitude']})
    meta.update({"Type":"FlowerPower"})
    meta.update({"Is_indoor":location['is_indoor']})
    meta.update({"In Pot":location['in_pot']})
    meta.update({"Avatar":location['avatar_url']})
    if (since > until):
        return -1

    elif (location['sensor']):
        SerialNumber=location['sensor']['sensor_serial']
        NickName=location['sensor']['nickname']
        SensorUUID=SerialNumber
        SensorIdentifier=location['sensor']['sensor_identifier']
        Plant_Nickname=location['plant_nickname']
        print ("Sensor ID "+SensorUUID)
        print ("Dump " + location['sensor']['sensor_identifier']+ location['sensor']['firmware_version'] + '.csv')
        print (" location_identifier "+location['location_identifier'])

        print (" From: " + str(since)[:19])
        print (" To:   " + str(until)[:19])
        home = expanduser("~")
        location_identifier=location['location_identifier']
        SummaryfileCsv = csv.writer(open(home+"/Desktop/"+account + ".csv", "a"))
        DownloadSummaryfileCsv = csv.writer(open(home+"/Downloads/"+account + ".csv", "a"))
        fileCsv = csv.writer(open(home+"/Desktop/"+location['sensor']['sensor_identifier'] +"-"+now+ ".csv", "w"))
        DownloadfileCsv = csv.writer(open(home+"/Downloads/"+location['sensor']['sensor_identifier'] +"-"+now+ ".csv", "w"))
        fileCsv.writerow(["Plant Nickname","SensorIdentifier","NickName","serial_number","capture_datetime_utc", "fertilizer_level", "light", "soil_moisture_percent", "air_temperature_celsius"])
        fileCsv.writerow([Plant_Nickname,SensorIdentifier,NickName,SerialNumber])        
        DownloadfileCsv.writerow(["Plant Nickname","SensorIdentifier","NickName","serial_number","capture_datetime_utc", "fertiliz\
er_level", "light", "soil_moisture_percent", "air_temperature_celsius"])
        DownloadfileCsv.writerow([Plant_Nickname,SensorIdentifier,NickName,SerialNumber])
        last_datetime="None"

        while (since < until):
            samplesLocation = api.getSamplesLocation(location['location_identifier'], since, since + timedelta(days=7))

            if (len(samplesLocation["errors"])):
                print (location['sensor']['sensor_identifier'], samplesLocation["errors"][0]["error_message"])
                continue
            for sample in samplesLocation['samples']:
                SensorData=dict()

                SensorData.update({"device":SensorUUID})

                capture_datetime_utc = sample["capture_datetime_utc"].replace("T", " ").replace("Z", "")
                SensorData.update({"insertion_time":capture_datetime_utc})
                fertilizer_level = sample["fertilizer_level"]
                soil_moisture_percent = sample["soil_moisture_percent"]
                air_temperature_celsius = sample["air_temperature_celsius"]
                light = sample["light"]
                fileCsv.writerow([Plant_Nickname,SensorIdentifier,NickName,SerialNumber,capture_datetime_utc, fertilizer_level, light, soil_moisture_percent, air_temperature_celsius])
                DownloadfileCsv.writerow([Plant_Nickname,SensorIdentifier,NickName,SerialNumber,capture_datetime_utc, fertilizer_level, light, soil_moisture_percent, air_temperature_celsius])
                last_datetime=capture_datetime_utc
            since += timedelta(days=7)
        print()
        DownloadSummaryfileCsv.writerow([Plant_Nickname,SensorIdentifier,NickName,SerialNumber,location_identifier,location['latitude'],location['longitude'],last_datetime] )
        return 0
