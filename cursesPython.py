import subprocess
import json
from curses import wrapper
import curses

drive_dict = dict()
sas_dict = dict()


def getEncl():
    encsList = list()
    subprocess.run(["sudo","./encList.sh"])
    for encString in open("exp.txt"):
        encsList.append(encString.strip('\n'))

    return encsList


def getNumSlots(encList):
    slotList = list()
    for enc in encList:
        subprocess.run(["sudo","./slotsList.sh",f"{enc}"])
        for slotString in open("slots.txt"):
            tup = [enc,slotString.strip('\n')]
            slotList.append(tup)

    return slotList


def createSASDict(): #key: sas address, value: logical name
    subprocess.run(["sudo","./sasDict.sh"])
    file=iter(open("/home/joshua/pocketKnife/sasDict.txt"))
    for line in file:
        #print(line)
        tokens = line.split()
        #print(tokens)
        value=tokens.pop().strip()
        key=tokens.pop().strip()
        #print(key,value)
        sas_dict[key]=value
    #print("SAS Dictionary")
    #print(sas_dict)

def createFullDict(): #key: logical name, value: infoList [encIDString, SlotString, sas address, other info if needed]
    encList = getEncl()
    numList = getNumSlots(encList)
    #print(numList)
    infoList = getSASaddr(numList)
    for i in infoList:
        logicName=sas_dict.get(i[2])
        newinfo=i
        sasAddr=i[2]
        #print("newinfo: ",i,"sasAddr: ",i[2])
        if sasAddr == '0x0': #Case: SAS Address missing = empty slot
           #print("empty slot found:",i)
           logicName='Empty'
           if logicName in drive_dict: #empty slot already exists, add in slot info
               #print("Empty slot already exists in dict")
               drive_dict[logicName].append(i)
           else: #first time adding empty slot
               #print("First Time adding empty slot")
               newinfo=list()
               newinfo.append(i) #needs to be a list within a list
               drive_dict[logicName]=newinfo
        elif logicName == '-': #Case: no logical name?
            print("No Logical Name case. Implement Code?")
            logicName='NoName'
            if logicName in drive_dict: #NoName entry already exists
                drive_dict[logicName].append(i)
            else: #first time adding no name entry
                newinfo=list()
                newinfo.append(i)
                drive_dict[logicName]=newinfo
        else:
            drive_dict[logicName]=newinfo
    #print("Drive Dictionary")
    #print(drive_dict) #TODO: Make printout of dictionary more reader-friendly


def getSASaddr(slotList):
    for tup in slotList:
        subprocess.run(["sudo","./sasAddr.sh",f"{tup[0]}",f"{tup[1]}"])
        for sasAddr in open("sasAddr.txt"):
            #print("getSASfunction: ",sasAddr)
            tup.append(sasAddr.strip('\n'))
            #print(tup)
            #subprocess.run(["sudo","./logicName.sh",f"{sasAddr}"])
            #for name in open("logicName.txt"):
            #    subprocess.run(["sudo","cat","logicName.txt"])
            #    #print(name)
            #    tup.append(name)
            #    #print(tup)
    return slotList
            #return sasAddr #return as string instead of as SASAddress appended to end of List

def driveDump(testDict):
    with open('test.json', 'w') as file:
        file.write(json.dumps(testDict))


def driveRead():
    with open('test.json') as handle:
        return json.loads(handle.read())


def compareDict(drive_dict(), dictImport()):
    dictSet = set(drive_dict.keys())
    importSet = set(dictImport.keys())
    diff = importSet.difference(dictSet)
    for drives in diff:
        #print("Drive "+drives+" is missing"


def menu(stdscr):
    dims = stdscr.getmaxyx()
    stdscr.nodelay(0)
    stdscr.clear()
    selection = -1
    option = 0
    while selection < 0:
        menuOptions = [0]*4
        menuOptions[option] = curses.A_REVERSE
        stdscr.addstr(int(dims[0]/2)-2, int(dims[1]/2-4), 'Blink LED', menuOptions[0])
        stdscr.addstr(int(dims[0]/2)-1, int(dims[1]/2-3), 'Compare', menuOptions[1])
        stdscr.addstr(int(dims[0]/2), int(dims[1]/2)-6, 'Instructions', menuOptions[2])
        stdscr.addstr(int(dims[0]/2)+1, int(dims[1]/2)-2, 'Exit', menuOptions[3])
        action = stdscr.getch()
        if action == curses.KEY_UP:
            option = (option - 1) % 4
        elif action == curses.KEY_DOWN:
            option = (option + 1) % 4
        elif action == ord('\n'):
            selection = option
        stdscr.refresh()
        if selection == 0:
            stcscr.clear()
            stdscr.addstr(0, 0, "Do you want to turn LEDs On or Off? (On/Off)")
            stdscr.addstr(1, 0, "(hit Ctrl-G to send)")
            firstWin = curses.newwin(5,30, 2,1)
            rectangle(stdscr, 3,0, 1+5+1, 1+40+1)
            stdscr.refresh()
            box = Textbox(firstWin)
            box.edit()
            messageOn = box.gather()
            stdscr.addstr(10, 0, "Enter space-seperated full device names (i.e., /dev/sda /dev/sdb).")
            stdscr.addstr(11, 0, "(hit Ctrl-G to send)")
            stdscr.addstr(12, 0, "For Empty drive bays, use the keyword Empty.")
            secondWin = curses.newwin(5,30, 2,1)
            rectangle(stdscr, 14,0, 1+5+1, 1+40+1)
            stdscr.refresh()
            box = Textbox(secondWin)
            box.edit()
            messageDevice = box.gather()
            ledBlinkQuery(messageOn, messageDevice)
            stdscr.clear()
            stdscr.addstr(1, 0, "Press Enter to Return to Menu, E to exit")
            if action == ord('\n'):
                selection = option
            if action == ord('e'):
                exit()
        if selection == 2:
            stdscr.clear()
            stdscr.addstr(1,int(dims[1]/2)-6,'Instructions')
            message = """Designed to turn on Drive LEDs on Failure for SSG systems.\n
                         Blink LED will turn on or off LEDs on connected backplanes.\n
                         Compare will bring up a table of all drive curretly found
                         versus all drives that were found on startup. \n
                         Instructions will bring up this menu. \n
                         Exit will exit the program. \n
                         """
            stdscr.addstr(5,int(dims[1]/2)- 30,message)
            stdscr.getch()
            stdscr.clear()
            selection = -1

def ledBlinkQuery(blinkInput, startOrStop):
    stdscr.clear()
    j = 0
    if startOrStop != "On" or startOrStop !="Off":
        stdscr.addstr(j, 0, "Error, Parameter only accepts On/Off")
    for i in iter(blinkInput):
        infoList=drive_dict.get(i)
         # print(infoList)
        if infoList==None:  #input device not a key in dictionary
            stdscr.addstr(j, 0, "Error: ",i, "device name not found.")
            stdscr.refresh()
            j+=1
        elif i=='Empty' or i=='NoName': #Edge Cases
                #print("Empty or No Name cases: ", i, infoList)
            for item in infoList:
                if startOrStop == "On":
                    ledBlink(item[0],item[1],j)
                    stdscr.refresh()
                    j+=1
                else:
                    ledStop(item[0],item[1],j)
                    stdscr.refresh()
                    j+=1
        else: #all other standard logical names
                #print("Standard Logical Name Case")
            if startOrStop == "On":
                ledBlink(item[0],item[1],j)
                stdscr.refresh()
                j+=1
            else:
                ledStop(item[0],item[1],j)
                stdscr.refresh()
                j+=1
    stdscr.addstr(j, 0, "Task Complete")


def ledBlink(expanderID, slotID, j):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--set=ident",f"{expanderID}"])
    stdscr.addstr(j,0, f"Activated {slotID} on Expander {expanderID}")

def ledStop(expanderID, slotID,j):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--clear=ident",f"{expanderID}"])
    stdscr.addstr(j,0,f"Deactivated {slotID} on Expander {expanderID}")

wrapper(menu)
