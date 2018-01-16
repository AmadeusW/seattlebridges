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
        names = list()
        for name, time in self.recentBridgeOpening.items():
            if (time > currentTime - timedelta(minutes=15)):
                names.append(name)
        return names

state = State()
load(r'C:\src\seattlebridges\collector\tweets.csv')
