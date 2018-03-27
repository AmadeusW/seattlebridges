from urllib.request import URLopener
import os
import json
from datetime import datetime, timedelta

apiKeyLocation = r'C:\Users\ama\OneDrive\config\wunderground.json'
dataLocation = "data/"
dataExtension = "json"

def getApiKey():
    with open(apiKeyLocation, 'r') as apiFile:
        data = json.load(apiFile)
        return data['apiKey']

def getWeatherData(year, month, day):
    apiKey = getApiKey()
    url = 'http://api.wunderground.com/api/{0}/history_20{1}{2}{3}/q/WA/seattle.json'.format(apiKey, year, month, day)
    testfile = URLopener()
    testfile.retrieve(url, dataLocation + "{0}{1}{2}.{3}".format(year, month, day, dataExtension))

def getEarliestData(path):
    earliest = ""
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if (filename.endswith("."+dataExtension)):
                earliest = filename
                break # stop on the first date we see. Assume that the OS returned files in sorted fashion
    if earliest == "":
        raise Exception("Could not find any {0} files in {1}".format(dataExtension, path))

    year = earliest[0:2]
    month = earliest[2:4]
    day = earliest[4:6]
    return [year, month, day]

def getLatestData(path):
    latest = ""
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if (filename.endswith("."+dataExtension)):
                latest = filename
                # don't break. Try to process all files. Assume that the OS returned files in sorted fashion
    if latest == "":
        raise Exception("Could not find any {0} files in {1}".format(dataExtension, path))

    year = latest[0:2]
    month = latest[2:4]
    day = latest[4:6]
    return [year, month, day]

def getPreviousDate(year, month, day):
    thisDate = datetime.strptime("{0}{1}{2}-12:00:00".format(year, month, day),
    "%y%m%d-%H:%M:%S")
    nextDate = thisDate - timedelta(days=1)
    return [nextDate.strftime("%y"), nextDate.strftime("%m"), nextDate.strftime("%d")]

def getNextDate(year, month, day):
    thisDate = datetime.strptime("{0}{1}{2}-12:00:00".format(year, month, day),
    "%y%m%d-%H:%M:%S")
    nextDate = thisDate + timedelta(days=1)
    return [nextDate.strftime("%y"), nextDate.strftime("%m"), nextDate.strftime("%d")]

def go():
    earliestDate = getEarliestData(dataLocation)
    nextDate = getPreviousDate(earliestDate[0], earliestDate[1], earliestDate[2])
    getWeatherData(nextDate[0], nextDate[1], nextDate[2])

def goForwards():
    latestDate = getLatestData(dataLocation)
    nextDate = getNextDate(latestDate[0], latestDate[1], latestDate[2])
    getWeatherData(nextDate[0], nextDate[1], nextDate[2])

#go()