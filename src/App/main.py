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


# returns -1 if user doesnt want to set custom app-lists nor use the default ones = e0 will be global volume
# return 0 if user wants to use default lists
# return 1 to 3 meaning how many lists are set
def setLists(cvol):
    done = False
    global apps0
    global apps1
    global apps2
    alreadyUsed = []
    # use lists or not?
    while True:
        print("\n-----\n")
        choice = input("Would you like to set custom app-lists or use predefined ones? Y/N: ")
        if choice == 'N' or choice == 'n': return -1
        elif choice == "Y" or choice == "y": break
        else: continue # invalid user input handling
    # default or custom lists?
    while True:
        print("\n-----\n")
        choice = input("1: Use predefined lists\n2: Make custom lists\nChoice: ")
        if choice == '1': apps0 = vol.m_voip_enum; apps1 = vol.m_music_apps_enum; apps2 = vol.m_browsers_enum; return 0
        elif choice == '2': break
        else: continue # invalid user input handling
    cntLists = 0
    while not done:
        print("\n-----\n")
        if cntLists != 0:
            print("list1: " + str(apps0))
            if cntLists > 1: print("list2: " + str(apps1))
            if cntLists > 2: print("list3: " + str(apps2))
        
        i = 0
        apps = [] 

        vol.getSessionNamesOut(apps) # get running apps names
        applist = list(dict.fromkeys(apps)) # remove duplicates
        for app in applist:
            if app in alreadyUsed: applist.remove(app); continue # if the app was previously assigned, it cannot be assigned again and thus remove it from the list
            print(f"{i}: {app}")
            i += 1
        choices = input("App-Numbers you want to add (comma separated): ")
        for ch in choices.split(","):
            try:
                c = int(ch)
            except: continue # invalid user input handling
            if cntLists == 0: apps0.append(applist[c])
            if cntLists == 1: apps1.append(applist[c])
            if cntLists == 2: apps2.append(applist[c])
            alreadyUsed.append(applist[c])

        cntLists += 1
        if cntLists == 3: break # using 3 encoders, doesnt make sense to make more lists than 3

        while True:
            next = input("Would you like to add another list? Y/N: ")
            if next == 'n' or next == 'N': done = True; break
            elif next == 'y' or next == 'Y': break
            else: continue # invalid user input handling

    # print current state
    if cntLists != 0:
        print("list1: " + str(apps0))
    if cntLists > 1: print("list2: " + str(apps1))
    if cntLists > 2: print("list3: " + str(apps2))

    return cntLists

# assign encoders to user-defined app lists
def assignEncoders():
    global assignmentDict
    global apps0
    global apps1
    global apps2
    while True:
        print("\n-----\n")
        print("current: ")
        print(f"\t encoder 0: {assignmentDict['e0']}")
        print(f"\t encoder 1: {assignmentDict['e1']}")
        print(f"\t encoder 2: {assignmentDict['e2']}")
        print(f"\t list 0: {str(apps0)}")
        print(f"\t list 1: {str(apps1)}")
        print(f"\t list 2: {str(apps2)}")
        
        choice = input("New assignment? Y/N: ")
        if choice == 'n' or choice == 'N': break
        elif choice == 'y' or choice == 'Y':
            ch = input("Assign which encoder to which list? For example: 0-1: ")
            e,l = ch.split("-")
            if l == '0': li = apps0
            elif l == '1': li = apps1
            elif l == '2': li = apps2
            else: continue # invalid user input handling
            if e == '0': assignmentDict["e0"] = li
            elif e == '1': assignmentDict["e1"] = li
            elif e == '2': assignmentDict["e2"] = li
            else: continue # invalid user input handling
            
    print("current: ")
    print(f"\t encoder 0: {assignmentDict['e0']}")
    print(f"\t encoder 1: {assignmentDict['e1']}")
    print(f"\t encoder 2: {assignmentDict['e2']}")
    print(f"\t list 0: {str(apps0)}")
    print(f"\t list 1: {str(apps1)}")
    print(f"\t list 2: {str(apps2)}")

# send current volume and enabled encoders to Arduino
def sendInit(conn, vol):
    global assignmentDict
    time.sleep(1)
    buf = "" # using buffer for easy interpretation on Arduino
    if (assignmentDict['e0'] == "master"): # e0 is the only valid encoder for master volume control
        vol0 = vol.getMasterVolumeNative()
        if (vol0 < 10): buf += "00"; buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        elif (vol0 >= 10 and vol0 < 100): buf += "0"; buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        else: buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        buf += ":"
    elif (assignmentDict['e0'] != None):
        vol0array = []
        # find all running apps in the app-list volumes and store them in an array
        for v in assignmentDict['e0']:
            try:
                vol0 = vol.getSessionVolume(v)
                if (type(vol0) is int): vol0array.append(vol0) # dont append if the app is not running
            except: continue # dont crash the program if the app is not running
        vol0 = max(vol0array) # find the maximum volume of all the apps in one list
        for s in assignmentDict['e0']: # assign the maximum volume to all the apps in the list
            try:
                vol.setSessionVolume(s, vol0)
            except: continue # dont crash the program if the app is not running
        if (vol0 < 10): buf += "00"; buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        elif (vol0 >= 10 and vol0 < 100): buf += "0"; buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        else: buf += str(vol0) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        buf += ":"
    else: buf += str(999); buf += ":" # if the encoder shall not be enabled, use 999 as the value; using : as a delimiter

    if (assignmentDict['e1'] != None):
        vol1array = []
        # find all running apps in the app-list volumes and store them in an array
        for v in assignmentDict['e1']:
            try:
                vol1 = vol.getSessionVolume(v)
                if (type(vol1) is int): vol1array.append(vol1) # dont append if the app is not running
            except: continue # dont crash the program if the app is not running
        vol1 = max(vol1array) # find the maximum volume of all the apps in one list
        for s in assignmentDict['e1']: # assign the maximum volume to all the apps in the list
            try:
                vol.setSessionVolume(s, vol1)
            except: continue # dont crash the program if the app is not running
        if (vol1 < 10): buf += "00"; buf += str(vol1) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        elif (vol1 >= 10 and vol1 < 100): buf += "0"; buf += str(vol1) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        else: buf += str(vol1) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        buf += ":"
    else: buf += str(999); buf += ":" # if the encoder shall not be enabled, use 999 as the value; using : as a delimiter

    if (assignmentDict['e2'] != None):
        vol2array = []
        # find all running apps in the app-list volumes and store them in an array
        for v in assignmentDict['e2']:
            try:
                vol2 = vol.getSessionVolume(v)
                if (type(vol2) is int): vol2array.append(vol2) # dont append if the app is not running
            except: continue # dont crash the program if the app is not running
        vol2 = max(vol2array) # find the maximum volume of all the apps in one list
        for s in assignmentDict['e2']: # assign the maximum volume to all the apps in the list
            try:
                vol.setSessionVolume(s, vol2)
            except: continue # dont crash the program if the app is not running
        if (vol2 < 10): buf += "00"; buf += str(vol2) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        elif (vol2 >= 10 and vol2 < 100): buf += "0"; buf += str(vol2) # zero-padding to hit the targeted format XXX:YYY:ZZZ
        else: buf += str(vol2) # zero-padding to hit the targeted format XXX:YYY:ZZZ
    else: buf += str(999) # if the encoder shall not be enabled, use 999 as the value
    
    conn.writeData(buf) # sending the configuration at once
    time.sleep(2)
    conn.writeData("DONE") # telling Arduino to start the main program

# mute functionality
# different handling depending on whether the master or list is chosen
def eMute(vol, e):
    l = assignmentDict[e]
    if l == "master": vol.toggleMasterState(); return
    for item in l:
        try: # dont crash the program if the app in list is not running
            pass
        except: continue

# volume incrementation
# different handling depending on whether the master or list is chosen
def eVolInc(vol, e):
    l = assignmentDict[e]
    if l == "master": vol.setMasterVolumeIncNative(1); return
    for item in l:
        try: # dont crash the program if the app in list is not running
            vol.setSessionVolumeInc(item, 1)
        except: continue

# volume decrementation
# different handling depending on whether the master or list is chosen
def eVolDec(vol, e):
    l = assignmentDict[e]
    if l == "master": vol.setMasterVolumeDecNative(1); return
    for item in l:
        try: # dont crash the program if the app in list is not running
            vol.setSessionVolumeDec(item, 1)
        except: continue

def main(conn, vol, lists):
    global done
    cnt = 0
    while not done:
        # future synchronization implementation
        # cnt += 1
        # if cnt > 1000: sendInit(conn, vol); cnt = 0 # synchronization

        data = conn.readData()
        try:
            eid, ech, ebtn = data.split(":") # eid = encoder id; ech = change vol up/down; ebtn = mute (button press)
        except: continue
        if (eid == '0'):
            if int(ebtn) == 1: eMute(vol, "e0")
            if ech == '+': eVolInc(vol, "e0")
            if ech == '-': eVolDec(vol, "e0")

        if (eid == '1' and lists > 1):
            if int(ebtn) == 1: eMute(vol, "e1")
            if ech == '+': eVolInc(vol, "e1")
            if ech == '-': eVolDec(vol, "e1")

        if (eid == '2' and lists > 2):
            if int(ebtn) == 1: eMute(vol, "e2")
            if ech == '+': eVolInc(vol, "e2")
            if ech == '-': eVolDec(vol, "e2")


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
    # set custom lists and assign encoders to the specified lists
    lists = setLists(vol)
    if lists == -1: assignmentDict["e0"] = "master" # automatic master assignment
    elif lists == 0:assignmentDict["e0"] = apps0; assignmentDict["e1"] = apps1; assignmentDict["e2"] = apps2 # default list assignment
    else: assignEncoders() # manual assignment

    conn.writeData("CONNECTED") # tell Arduino that the program is ready
    time.sleep(2)
    sendInit(conn, vol) # tell Arduino current volume levels and which encoders should be enabled

    main(conn, vol, lists)

    time.sleep(1)
    # close connection
    conn.close()