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

    time.sleep(1)
    # close connection
    conn.close()