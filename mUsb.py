import os
from twilio.rest import Client

def sendNotifToAdmin():
    # put your own credentials here
    ACCOUNT_SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    AUTH_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
        to='+XXXXXXXXXXXX',  # Your phone Number
        from_='+XXXXXXXXXXX',  # Your Twilio Phone Number
        body='An external Drive has been plugged in',
    )

whiteListDisks = ["SCSI\DISK&VEN_HGST&PROD_HTS545050A7E380\\4&3140E8F0&0&000000"]
extraConnectedDisks = []
old_stat = []
notifSent = []
while True:
    presentDisks = []
    with open("status.txt", "w") as GenDiskfile:
        GenDiskfile.write("")
    os.system('@echo off&devcon.exe status GenDisk >> status.txt')
    with open("status.txt", "r") as GenDiskfile:
        GenDiskLines = GenDiskfile.readlines()
        if GenDiskLines:
            totalDisks = (len(GenDiskLines) - 1) / 3 #Get IDs. because after first line, every 3rd line contains Disk 
            mConst = 3
            mMinus = -3

            # Get all present connected driv IDs
            while True:
                presentDisks.append(str(GenDiskLines[mMinus + mConst]).rstrip())
                mMinus += 3
                totalDisks -= 1
                if totalDisks == 0:
                    break

            ###############################################################
            # Main algo to detect if a drive has been connected or removed
            len_p = len(presentDisks)
            len_o = len(old_stat)

            # if a drive has been connected
            if len_p > len_o:
                if len([p for p in presentDisks if p not in whiteListDisks]) > 0: # if drive isn;t whitelisted
                    print("Detected new drive that isn't whiteListed")
                    old_stat = presentDisks
                    sendNotifToAdmin()

            # if a drive has been disconnecetd
            elif len_p < len_o:
                print("Drive has been removed")
                old_stat = presentDisks
            ##################################################################

    GenDiskfile.close()