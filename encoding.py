import os
import time

for i in range(10):
    print("Encoding! PID - %d" % os.getpid())
    time.sleep(2)
