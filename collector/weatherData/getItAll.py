from getWeather import go
import time

for i in range(0, 200):
    print("iteration {0}".format(i))
    go()
    time.sleep(6)