import os
import sys
import time
import readline

sys.path.append(".")

from NodeManager import *

def main():

    mgr = NodeManager("mgr.config")
    time.sleep(0.1)

    while True:

        operation = input("What do you want me to do: ")

        mgr.indirect(operation)



if __name__ == '__main__':
    main()
