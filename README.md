# SMC_PocketKnife

AJ&#39;s PocketKnife

Designed to turn on Drive LEDs on Failure for SSG systems.

1) Set up StartUp script to document HDD on Expanders for Topload Systems
    - create command line argument for HDD documentation, then add script to init.d 
2) Create a Trigger to Initiate LED notification for User (Python)
    - user can take drive logical name (/dev/sda , etc), and turn on or off LEDs
    - based on how information is stored,dead drives can still be tied to slots

Clean up:

1) Make Drive Info Dict list option
    - Allows User to see All Drives in Readable Format
2)Triggering Mechanism
    - Polling DMESG or var/log/*
    - possibly something more efficient.

To Do:

1) GUI
    - makes app User Friendly
    - AJ's Recommendation: NCurses (can be used with SSH?)
2) Multiple systems
    - Based on Expanders, figure out and Map Systems + JBODs Seperately
3) Solutions Specific
    - Do mapping for Ceph/Lustre, so OSD names can be used.
