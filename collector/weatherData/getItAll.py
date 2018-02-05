from getWeather import go, goForwards
import time

for i in range(0, 21):
    print("iteration {0}".format(i))
    goForwards()
    time.sleep(6)