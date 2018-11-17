import subprocess
from operator import itemgetter

drives_list = list()
drives_dict = dict()
count = 1
for drive_string in open("/home/joshua/pocketKnife/drives.txt"):
    drive_info_list = drive_string.strip().split(',')
    
   
    drive_info = dict()
    drive_info['SAS'] = drive_info_list[0][4:]
    drive_info['Logic'] = drive_info_list[1]
    drive_info['Exp'] = drive_info_list[2]
    drives_list.append(drive_info)
    



print(drives_list[0])
print(drive_info[SAS]for drive_info in drives_list[0])

def ledBlink(slotID, expanderID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--set=ident",f"{expanderID}"])
	
	
def ledStop(slotID, expanderID):
    subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--clear=ident",f"{expanderID}"])

def slotAssign(expanderID):
    subprocess.run(["sudo","slotAlloc.sh",f"expanderID"])
    for slot in f.open("slot.txt"):
        
        

def getAppendSlot(listDrives, expanderID):
    slotList = list()
    for index in range(len(listDrives)):
        for SAS in listDrives[index]: 
            subprocess.run(["sudo","sg_ses",f"--sas-addr={listDrives[index][SAS]}",f"{expanderID}","|", "grep", "Slot", ">", "slot.txt"])
            slotList[index] = subprocess.run(["awk", "'{print $1}'", "slot.txt"])
   

    print(slotList)
    for index in range(len(listDrives)):
	 
