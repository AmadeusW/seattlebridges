import csv
import os
from datetime import datetime, timedelta
from Weather import getSampleData

indexBridge = 0
bridgeData = {
    "The Ballard Bridge": 0,
    "The Fremont Bridge": 1,
    "The University Bridge": 2,
    "The Montlake Bridge": 3,
    "The Lower Spokane St Bridge": 4,
    "The 1st Ave S Bridge": 5,
    "The South Park Bridge": 6
}

indexWeather = indexBridge + len(bridgeData)
weatherData = {
    "TemperatureCold": 0,
    "Temperature10": 1,
    "Temperature15": 2,
    "Temperature20": 3,
    "Temperature25": 4,
    "Temperature30": 5,
    "RainOrSnow": 6,
    "VisibilityLow": 7,
    "VisibilityMedium": 8,
    "VisibilityHigh": 9,
}

indexCalendar = indexWeather + len(weatherData)
calendarData = {
    "dayOff": 0,
    "dayOffOrNextTo": 1
}

indexRecentBridgeOpening = indexCalendar + len(calendarData)
indexTime = indexRecentBridgeOpening + len(bridgeData)
totalLength = indexTime + 24 * 4 # we're dividing time into fifteen minute segments

def encodeWeatherData(data):
    encoding = [0] * len(weatherData)
    if (data['maxtemperature'] < 10):
        encoding[weatherData["TemperatureCold"]] = 1
    elif (data['maxtemperature'] < 15):
        encoding[weatherData["Temperature10"]] = 1
    elif (data['maxtemperature'] < 20):
        encoding[weatherData["Temperature15"]] = 1
    elif (data['maxtemperature'] < 25):
        encoding[weatherData["Temperature20"]] = 1
    elif (data['maxtemperature'] < 30):
        encoding[weatherData["Temperature25"]] = 1
    else:
        encoding[weatherData["Temperature30"]] = 1
    if (data['snow'] == 1 or data['rain'] == 1):
        encoding[weatherData["RainOrSnow"]] = 1
    if (data['visibility'] < 2):
        encoding[weatherData["VisibilityLow"]] = 1
    elif (data['visibility'] < 5):
        encoding[weatherData["VisibilityMed"]] = 1
    else:
        encoding[weatherData["VisibilityHigh"]] = 1
    return encoding

def encodeCalendarData(time):
    encoding = [0] * len(calendarData)
    if (time.weekday() >= 5): # saturday (5) or sunday (6)
        encoding[calendarData["dayOff"]] = 1
    if (time.weekday() >= 4 or time.weekday() == 0): # thursday to monday
        encoding[calendarData["dayOffOrNextTo"]] = 1
    return encoding

def encodeBridgeName(name):
    encoding = [0] * len(bridgeData)
    encoding[bridgeData[name]] = 1
    return encoding

def encodeTime(time):
    encoding = [0] * 24 * 4
    quarter = time.minute // 15 + time.hour * 4
    encoding[quarter] = 1
    return encoding

class State(object):
    """Stores state pertinent to the currently processed node"""

    recentBridgeOpening = dict()

    def updateAndGetRecentBridgeEncoding(self, name, time):
        recentBridgeEncoding = self.getRecentBridgeEncoding(time)
        self.recentBridgeOpening[name] = time
        return recentBridgeEncoding

    def getRecentBridgeEncoding(self, currentTime):
        recentBridgeEncoding = [0] * len(bridgeData)
        for name, time in self.recentBridgeOpening.items():
            if (time > currentTime - timedelta(minutes=15)):
                recentBridgeEncoding[bridgeData[name]] = 1
        return recentBridgeEncoding

def process(row):
    print(row)
    if row['closed'] == 'false': return

    time = datetime.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%S.000Z')
    name = row['bridge']

    nameEncoding = encodeBridgeName(name)
    timeEncoding = encodeTime(time)
    calendarEncoding = encodeCalendarData(time)
    weatherEncoding = encodeWeatherData(getSampleData())
    recentBridgeEncoding = state.updateAndGetRecentBridgeEncoding(name, time)

    data = []
    data.extend(weatherEncoding)
    data.extend(calendarEncoding)
    data.extend(recentBridgeEncoding)
    data.extend(timeEncoding)

    print(nameEncoding)
    print(data)

def load(filename):
    with open(filename, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        rows = list(reader)
        for i, row in enumerate(rows):
            process(row)
            if (i > 10):
                return


state = State()
load(r'C:\src\seattlebridges\collector\tweets.csv')
