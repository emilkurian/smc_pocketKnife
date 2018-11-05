import subprocess
from operator import itemgetter

drives_list = list()
drives_dict = dict()

for drive_string in open("m04_lab_profiles"):
    drive_info_list = drive_string.strip().split(',')
    print(drive_info_list)

    drive_info = dict()
    drive_info['Drive'] = drive_info_list[0]
    drive_info['Logic'] = drive_info_list[1]
    drive_info['Exp'] = drive_info_list[2]
    drives_list.append(drive_info)
	
    if drive_info['Drive'] not in drives_dict:
        drives_dict[drive_info['Drive']] = list()

    drives_dict[drive_info['Drive']].append(drive_info)

	

for drive_info in drives_dict["Drive"]:

        print("{0:24}   {1:10}   {2:8,.2f}".format(drive_info['Drive'],
                                                   drive_info['Logic'],
                                                   drive_info['Exp']))
												   
												   
def ledBlink(slotID, expanderID):
	subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--set=ident",f"{expanderID}"])
	
	
def ledStop(slotID, expanderID):
	subprocess.run(["sudo","sg_ses",f"--descriptor={slotID}","--clear=ident",f"{expanderID}"])