from urllib.request import urlopen
import os
import json

apiKeyLocation = r'C:\Users\ama\OneDrive\config\wunderground.json'

def getApiKey():
    with open(apiKeyLocation, 'r') as apiFile:
        data = json.load(apiFile)
        return data['apiKey']

def getWeatherData(year, month, day):
    apiKey = getApiKey()
    url = 'http://api.wunderground.com/api/{0}/history_{1}{2}{3}/q/WA/seattle.json'.format(apiKey, year, month, day)
    raw = urlopen(url)
    jsons = raw.read()
    data = json.loads(jsons)
    print(data)
    raw.close()

def getSampleData():
    result = {}
    with open('analysis\\SampleWeatherData.json', 'r') as dataFile:
        data = json.load(dataFile)
        summary = data['history']['dailysummary'][0]
        result['maxtemperature'] = int(summary['maxtempm'])
        result['meantemperature'] = int(summary['meantempm'])
        result['mintemperature'] = int(summary['mintempm'])
        result['fog'] = summary['fog']
        result['snow'] = summary['snow']
        result['rain'] = summary['rain']
        result['visibility'] = int(summary['maxvism'])
        return result

# getWeatherData(2017, 12, 24)
getSampleData()