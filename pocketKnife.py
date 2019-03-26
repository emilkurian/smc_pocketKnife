#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import subprocess
import json
import argparse
import os

drive_dict = dict()
sas_dict = dict()
startUp_dict = dict()


def getEncl():
    encsList = list()
    output = subprocess.Popen(["lsscsi -g -t | grep encl | awk '{print $5}'"], shell=True, stdout=subprocess.PIPE).stdout
    for i in output.read().splitlines():
        encString = i.decode('utf-8')
        encsList.append(encString.strip('\n'))
    return encsList


def getNumSlots(encList):
    slotList = list()
    for enc in encList:
        output = subprocess.Popen([f"sudo sg_ses --page=ED {enc} | grep Slot| awk '{{print $4}}'"], shell=True, stdout=subprocess.PIPE).stdout
        for i in output.read().splitlines():
            tup = [enc, i.decode('utf-8')]
            if tup not in slotList:
                slotList.append(tup)
    return slotList


def createSASDict():  # key: sas address, value: logical name
    output = subprocess.Popen(["lsscsi -t | grep sas | grep disk | awk '{{print $3," "$4}}' | sed 's/^....//'"], shell=True, stdout=subprocess.PIPE).stdout
    for line in output.read().splitlines():
        tup = line.decode('utf-8')
        tokens = tup.split()
        value = tokens.pop().strip()
        key = tokens.pop().strip()
        sas_dict[key] = value


def createFullDict():  # key: logical name, value: infoList [encIDString, SlotString, sas address, other info if needed]
    encList = getEncl()
    numList = getNumSlots(encList)
    # print(numList)
    infoList = getSASaddr(numList)
    for i in infoList:
        logicName = sas_dict.get(i[2])
        newinfo = i
        sasAddr = i[2]
        # print("newinfo: ",i,"sasAddr: ",i[2])
        if sasAddr == '0x0':  # Case: SAS Address missing = empty slot
            # print("empty slot found:",i)
            logicName = 'Empty'
            if logicName in drive_dict:  # empty slot already exists, add in slot info
                # print("Empty slot already exists in dict")
                drive_dict[logicName].append(i)
            else:  # first time adding empty slot
                # print("First Time adding empty slot")
                newinfo = list()
                newinfo.append(i)  # needs to be a list within a list
                drive_dict[logicName] = newinfo
        elif logicName == '-':  # Case: no logical name?
            print("No Logical Name case. Implement Code?")
            logicName = 'NoName'
            if logicName in drive_dict:  # NoName entry already exists
                drive_dict[logicName].append(i)
            else:  # first time adding no name entry
                newinfo = list()
                newinfo.append(i)
                drive_dict[logicName] = newinfo
        else:
            drive_dict[logicName] = newinfo
    # print("Drive Dictionary")
    # print(drive_dict) TODO Make printout of dictionary more reader-friendly


def getSASaddr(slotList):
    for tup in slotList:
        output = subprocess.Popen([f"sudo sg_ses --descriptor={tup[1]} {tup[0]} | grep 'SAS address' | sed '1d' | awk '{{print $3}}'"], shell=True, stdout=subprocess.PIPE).stdout
        address = output.read().decode('utf-8')
        if address == "":
            tup.append('0x0')
        else:
            tup.append(address.strip('\n'))
    return slotList


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Instructions", color="IMPORTANT")
        self.addForm("BLINK", secondForm, name="Drive LED Configuration", color="IMPORTANT")
        self.addForm("COMPARISON", thirdForm, name="Drive Comparison", color="IMPORTANT")
        self.addForm("STARTBLINK", fourthForm,"Start Up LED Configuration", color="IMPORTANT")

    def onCleanExit(self):
        for key in drive_dict:
            infoList = drive_dict.get(key)
            ledStop(infoList[0], infoList[1])
        subprocess.run(["sudo", "rm", "*.txt"])
        npyscreen.notify_wait("Goodbye!")

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


class MainForm(npyscreen.ActionFormWithMenus):
    def create(self):

        self.add(npyscreen.FixedText, value="This Program  is designed to locate and blink LEDs for storage drives")
        self.add(npyscreen.FixedText, value="Drive Comparison:")
        self.add(npyscreen.FixedText, value="Will list drives found on start up versus drives currently found")
        self.add(npyscreen.FixedText, value="LED Blink:")
        self.add(npyscreen.FixedText, value="Will blink or unblink drives")

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application, "�"),
            ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Blink/Unblink ", self.change_forms1),
            ("Compare", self.change_forms2)
            ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def on_ok(self):
        npyscreen.notify_confirm("Use ^X to go explore!")

    def change_forms1(self, *args, **keywords):
        change_to = "BLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms2(self, *args, **keywords):
        change_to = "COMPARISON"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class secondForm(npyscreen.ActionFormWithMenus):
    def create(self):

        drive = list()

        for key in drive_dict:
            drive.append(str(key))

        self.drives = self.add(npyscreen.TitleMultiSelect, max_height=10,
                          name="Drive LEDs to configure (press x to choose)", values=drive, scroll_exit=True)

        self.blink = self.add(npyscreen.TitleSelectOne, max_height=4, name="Turn the Drive LEDs on or off?",
                         values=["On", "Off"], scroll_exit=True)

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application),
            ("Use Start Up Drive List", self.change_forms3)
        ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Compare", self.change_forms1),
            ("Instructions", self.change_forms2),
            ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def on_ok(self):
        passDrives = self.drives.get_selected_objects()
        passBlink = self.blink.get_selected_objects()
        if str(passBlink) == "['On']":
            for i in passDrives:
                infoList = drive_dict.get(i)
                # print(infoList)
                if infoList is None:  # input device not a key in dictionary
                    print("Error: ", i, "device name not found.")
                elif i == 'Empty' or i == 'NoName':  # Edge Cases
                    # print("Empty or No Name cases: ", i, infoList)
                    for item in infoList:
                        ledBlink(item[0], item[1])
                else:  # all other standard logical names
                    # print("Standard Logical Name Case")
                    ledBlink(infoList[0], infoList[1])

        elif str(passBlink) == "['Off']":  # print("Turn LEDs Off")
            # print(blinkInput)
            for i in passDrives:
                infoList = drive_dict.get(i)
            # print(infoList)
                if infoList is None:  # input device not a key in dictionary
                    print("Error: ", i, "device name not found.")
                elif i == 'Empty' or i == 'NoName':  # Edge Cases
                    # print("Empty or No Name cases: ", i, infoList)
                    for item in infoList:
                        ledStop(item[0], item[1])
                else:  # all other standard logical names
                    # print("Standard Logical Name Case")
                    ledStop(infoList[0], infoList[1])
        else:
            npyscreen.notify_wait("Only On or Off as a Parameter!")

        npyscreen.notify_confirm("You turned " + str(passDrives) + str(passBlink))

    def change_forms2(self, *args, **keywords):
        change_to = "MAIN"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms1(self, *args, **keywords):
        change_to = "COMPARISON"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms3(self, *args, **keywords):
        change_to = "STARTBLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class thirdForm(npyscreen.ActionFormWithMenus):
    def create(self):

        drives = list()
        startUp = list()

        for key in drive_dict:
            drives.append(key)

        for key in startUp_dict:
            startUp.append(key)

        t2 = self.add(npyscreen.BoxTitle, name="Start-Up:", max_height=12,
                      scroll_exit=True)
        t3 = self.add(npyscreen.BoxTitle, name="Current:", max_height=12,
                      scroll_exit=True)
        t4 = self.add(npyscreen.BoxTitle, name="Difference:", max_height=6,
                      scroll_exit=True)

        t2.values = startUp
        t3.values = drives
        t4.values = list(set(startUp).difference(set(drives)))

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application, "é"),
            ("Instructions", self.change_forms2)
            ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Blink/Unblink LED", self.change_forms1)
            ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def on_ok(self):
        self.parentApp.switchForm(None)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def change_forms1(self, *args, **keywords):
        change_to = "BLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms2(self, *args, **keywords):
        change_to = "MAIN"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class fourthForm(npyscreen.ActionFormWithMenus):
    def create(self):

        drive = list()

        for key in startUp_dict:
            drive.append(str(key))

        self.drives = self.add(npyscreen.TitleMultiSelect, max_height=10,
                          name="Drive LEDs to configure (press x to choose)", values=drive, scroll_exit=True)

        self.blink = self.add(npyscreen.TitleSelectOne, max_height=4, name="Turn the Drive LEDs on or off?",
                         values=["On", "Off"], scroll_exit=True)

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application),
            ("Instructions", self.change_forms2)
        ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Compare", self.change_forms1),
            ("Use Current Drive List", self.change_forms3),
            ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def on_ok(self):
        passDrives = self.drives.get_selected_objects()
        passBlink = self.blink.get_selected_objects()
        if str(passBlink) == "['On']":
            for i in passDrives:
                infoList = startUp_dict.get(i)
                # print(infoList)
                if infoList is None:  # input device not a key in dictionary
                    print("Error: ", i, "device name not found.")
                elif i == 'Empty' or i == 'NoName':  # Edge Cases
                    # print("Empty or No Name cases: ", i, infoList)
                    for item in infoList:
                        ledBlink(item[0], item[1])
                else:  # all other standard logical names
                    # print("Standard Logical Name Case")
                    ledBlink(infoList[0], infoList[1])
        elif str(passBlink) == "['Off']":  # print("Turn LEDs Off")
            # print(blinkInput)
            for i in passDrives:
                infoList = startUp_dict.get(i)
            # print(infoList)
                if infoList is None:  # input device not a key in dictionary
                    print("Error: ", i, "device name not found.")
                elif i == 'Empty' or i == 'NoName':  # Edge Cases
                    # print("Empty or No Name cases: ", i, infoList)
                    for item in infoList:
                        ledStop(item[0], item[1])
                else:  # all other standard logical names
                    # print("Standard Logical Name Case")
                    ledStop(infoList[0], infoList[1])
        else:
            npyscreen.notify_wait("Only On or Off as a Parameter!")

        npyscreen.notify_confirm("You turned " + str(passDrives) + str(passBlink))

    def change_forms2(self, *args, **keywords):
        change_to = "MAIN"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms1(self, *args, **keywords):
        change_to = "INSTRUCTIONS"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms3(self, *args, **keywords):
        change_to = "BLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


def ledBlink(expanderID, slotID):
    subprocess.run(["sudo", "sg_ses", f"--descriptor={slotID}", "--set=ident", f"{expanderID}"])


def ledStop(expanderID, slotID):
    subprocess.run(["sudo", "sg_ses", f"--descriptor={slotID}", "--clear=ident", f"{expanderID}"])


def main():
    TA = MyTestApp()
    TA.run()


def driveDump(testDict):
    with open('startUpDrive.json', 'w') as file:
        file.write(json.dumps(testDict))


def driveRead():
    with open('startUpDrive.json') as handle:
        return json.loads(handle.read())


if __name__ == '__main__':

    test = "Test program for Arguments"

    parser = argparse.ArgumentParser(description=test)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-S", "--store", help="store drive info", action="store_true")
    args = parser.parse_args()

    if args.store:
        createSASDict()
        createFullDict()
        driveDump(drive_dict)
        exit()
    else:
        startUp_dict = driveRead()

    createSASDict()
    createFullDict()
    main()
