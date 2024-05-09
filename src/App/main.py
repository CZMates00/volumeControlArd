from serialcom import serialPortList
from serialcom import CSerial as CConn
from winvol import CVolume
import time
import sys

# global variables - it is easier to use global variables than to pass all of these variables into functions
done = False # controlling the main loop
# app lists
apps0 = []
apps1 = []
apps2 = []
# encoder assignment variables
e0 = None
e1 = None
e2 = None
# dictionary for storing the relation between encoders and app lists
assignmentDict = {"e0": None, "e1": None, "e2": None}


if __name__ == '__main__':
    # find connection
    choice = serialPortList()
    # open connection
    try:
        conn = CConn(choice)
    except: sys.exit() # exit the app if the serial connection was not succesfull
    time.sleep(1)

    # initialize volume class
    vol = CVolume()

    time.sleep(1)
    # close connection
    conn.close()