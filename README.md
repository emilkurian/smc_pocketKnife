# SMC_PocketKnife

AJs PocketKnife

Designed to turn on Drive LEDs on based on Failure reporting for SSG systems.

Python 3.6.7
lsscsi 0.28
sg_ses 2.43
npyscreen 4.10.5

Purpose:
1) Create a User-Readable text Based GUI to report on Drive Location, and allow for the 
   User to Activate/Deactivate slot LED's
2) Set up StartUp script to document HDD on Expanders for Topload Systems
    - create command line argument for HDD documentation, then add script to init.d 
3) Create a Trigger to Initiate LED notification for User (Python)
    - user can take drive logical name (/dev/sda , etc), and turn on or off LEDs
    - based on how information is stored, dead drives can still be tied to slots

To run:
"python3 pocketKnife.py"
- will activate the GUI for the program. Instructions page of the Program will have navigation controls.
"python3 pocketKnife.py -S" or "python3 pocketKnife.py --store"
-used to store drive information on startup, will store drive information in a JSON file.

Feature Improvements:
1)Triggering Mechanism
    - Polling DMESG or var/log/* and cronjob to find drive failures
2) Solutions Specific
    - Do mapping for Ceph/Lustre, so OSD names can be used.

