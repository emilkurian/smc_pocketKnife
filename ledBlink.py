import subprocess

drives_dict = dict()

def getEncl():
    encsList = list()
    subprocess.run(["sudo","./encList.sh"])
    for encString in open("exp.txt"):
        encsList.append(encString)
	
    return encsList
	

def getNumSlots(encList):
    slotList = list()
    for enc in encList:
        subprocess.run(["sudo","./slotsList.sh",f"{enc}"])
        for slotString in open("slots.txt"):
            tup = [enc,slotString]
            slotList.append(tup)
		
    return slotList
	
	
def getSASaddr(slotList):
    for tup in slotList:
        subprocess.run(["sudo","./sasAddr.sh",f"{tup[0]}",f"{tup[1]}"])
        for sasAddr in open("sasAddr.txt"):
            subprocess.run(["sudo","./logicName.sh",f"{sasAddr}"])
            for name in open("logicName.txt"):
                tup.append(sasAddr)
                tup.append(name)
		
    return slotList


def ledBlink(slotID, expanderID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--set=ident",f"{expanderID}"])
	
	
def ledStop(slotID, expanderID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--clear=ident",f"{expanderID}"])
	 
def printWorld():
    print("Working")
    return [1,2,3]


encList = getEncl()
numList = getNumSlots(encList)
driveInfo = getSASaddr(numList)

print(driveInfo)

