from ApiCloud import ApiCloud
from datetime import *
from time import sleep
import csv
import json
import socket
import uuid

dateFormat = "%d-%b-%Y %H:%M:%S"

def dumpAllFlowerPower(api, since="born", until="today"):
    status  = api.getSensorStatus()

    sensorDataSync = api.getSensorDataSync()
    for location in sensorDataSync["locations"]:
        err = dumpFlowerPower(api, location, since, until)
        if (err == -1):
            print ("Your 'Since' date is after your 'Until' date !?")
            break ;


def dumpFlowerPower(api, location, since, until):
    meta=dict()
    if (until == "today"):
        until = datetime.today()
    else:
        until = datetime.strptime(until, dateFormat)
    if (since == "born"):
        since = until - timedelta(days=7)
    else:
        since = datetime.strptime(since, dateFormat)

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

        print ("Sensor ID "+SensorUUID)
        print ("Dump " + location['sensor']['sensor_identifier']+ location['sensor']['firmware_version'] + '.csv')
        print (" location_identifier "+location['location_identifier'])

        print (" From: " + str(since)[:19])
        print (" To:   " + str(until)[:19])
        fileCsv = csv.writer(open(location['sensor']['sensor_identifier'] + ".csv", "w"))
        fileCsv.writerow(["NickName","serial_number","capture_datetime_utc", "fertilizer_level", "light", "soil_moisture_percent", "air_temperature_celsius"])
#        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        clientsocket.connect(("0.0.0.0", 19877))
        while (since < until):
            samplesLocation = api.getSamplesLocation(location['location_identifier'], since, since + timedelta(days=7))

            if (len(samplesLocation["errors"])):
                print (location['sensor']['sensor_identifier'], samplesLocation["errors"][0]["error_message"])
                continue

            for sample in samplesLocation['samples']:
                SensorData=dict()
                arr = []

                SensorData.update({"device":SensorUUID})

                capture_datetime_utc = sample["capture_datetime_utc"].replace("T", " ").replace("Z", "")
                SensorData.update({"insertion_time":capture_datetime_utc})
                fertilizer_level = sample["fertilizer_level"]
                soil_moisture_percent = sample["soil_moisture_percent"]
                air_temperature_celsius = sample["air_temperature_celsius"]
                light = sample["light"]
                fileCsv.writerow([NickName,SerialNumber,capture_datetime_utc, fertilizer_level, light, soil_moisture_percent, air_temperature_celsius])
                arr.append({"name":"fertilizer_level","fValue":fertilizer_level})
                arr.append({"name":"soil_moisture_percent","fValue":soil_moisture_percent})
                arr.append({"name":"air_temperature_celsius","fValue":air_temperature_celsius})
                arr.append({"name":"light","fValue":light})

                a=json.dumps({"SensorData":SensorData,"meta":meta,"sensors":arr})
            since += timedelta(days=7)
        print()

        return 0
