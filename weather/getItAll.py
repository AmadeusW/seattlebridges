from getWeather import go, goForwards
import time

for i in range(0, 50): # the upper bound is number of days since last available piece of data and today
    print("iteration {0}".format(i))
    goForwards()
    time.sleep(6)