import csv
import os
from datetime import datetime, timedelta

def load(filename):
    with open(filename, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        rows = list(reader)
        for i, row in enumerate(rows):
            state.update(row)
            if (i > 10):
                return

indices = {
    "The Ballard Bridge": 0,
    "The Fremont Bridge": 1,
    "The University Bridge": 2,
    "The Montlake Bridge": 3,
    "The Lower Spokane St Bridge": 4,
    "The 1st Ave S Bridge": 5,
    "The South Park Bridge": 6
}

class State(object):
    """Stores state pertinent to the currently processed node"""

    recentBridgeOpening = dict()

    def update(self, row):
        print(row)
        time = datetime.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%S.000Z')

        quarter = time.minute // 15 + time.hour * 4
        recentBridgeEncoding = self.getRecentBridgeEncoding(time)
        self.recentBridgeOpening[row['bridge']] = time

        print(quarter, recentBridgeEncoding)

    def getRecentBridgeEncoding(self, currentTime):
        names = [0] * len(indices)
        for name, time in self.recentBridgeOpening.items():
            if (time > currentTime - timedelta(minutes=15)):
                names[indices[name]] = 1
        return names

state = State()
load(r'C:\src\seattlebridges\collector\tweets.csv')
