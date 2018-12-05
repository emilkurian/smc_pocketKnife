import subprocess
import json

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


def ledBlink(expanderID, slotID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--set=ident",f"{expanderID}"])
    print(f"Activated {slotID} on Expander {expanderID}")


def ledBlinkQuery():
    startOrStop=input("Do you want to turn LEDs On or Off? (On/Off) ").strip()
    if startOrStop=='On':
        #print("Turn LEDs On")
        print("Enter space-seperated full device names (i.e., /dev/sda /dev/sdb).")
        print("For Unnamed devices, use the keyword NoName.")
        blinkInput=input("For Empty drive bays, use the keyword Empty. ").strip().split()
        #print(blinkInput)
        for i in iter(blinkInput):
            infoList=drive_dict.get(i)
           # print(infoList)
            if infoList==None:  #input device not a key in dictionary
                print("Error: ",i, "device name not found.")
            elif i=='Empty' or i=='NoName': #Edge Cases
                #print("Empty or No Name cases: ", i, infoList)
                for item in infoList:
                    ledBlink(item[0],item[1])
            else: #all other standard logical names
                #print("Standard Logical Name Case")
                ledBlink(infoList[0],infoList[1])
    elif startOrStop=='Off':
        #print("Turn LEDs Off")
        print("Enter space-seperated full device names (i.e., /dev/sda /dev/sdb).")
        print("For Unnamed devices, use the keyword NoName.")
        blinkInput=input("For Empty drive bays, use the keyword Empty. ").strip().split()
        #print(blinkInput)
        for i in iter(blinkInput):
            infoList=drive_dict.get(i)
           # print(infoList)
            if infoList==None:  #input device not a key in dictionary
                print("Error: ",i, "device name not found.")
            elif i=='Empty' or i=='NoName': #Edge Cases
                #print("Empty or No Name cases: ", i, infoList)
                for item in infoList:
                    ledStop(item[0],item[1])
            else: #all other standard logical names
                #print("Standard Logical Name Case")
                ledStop(infoList[0],infoList[1])    
    elif startOrStop=="Update"
         updateDict()
    else:
        print("This function only accepts On or Off as a parameter")
	
def ledStop(expanderID, slotID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--clear=ident",f"{expanderID}"])
    print(f"Deactivated {slotID} on Expander {expanderID}")

def updateDict()
    createSASDict()
    createFullDict()


test = "Test program for Arguments"

parser = argparse.ArgumentParser(description = test)
group = parser.add_mutually_exclusive_group()
group.add_argument("-S", "--store", help="store drive info", action="store_true")
group.add_argument("-D", "--dump", help="dump drive info", action="store_true")

args = parser.parse_args()

if args.store:
    updateDict()
    driveDump(drive_dict)
    exit()
elif args.dump:
    dictDump = driveRead()
else:
    print("loading util")
    

updateDict()
ledBlinkQuery()
