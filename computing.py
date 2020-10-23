import os
import time

for i in range(10):
    print("Computing! PID - %d" % os.getpid())
    time.sleep(0.5)
