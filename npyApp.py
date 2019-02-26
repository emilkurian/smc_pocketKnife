#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import subprocess
import json

drive_dict = dict()
sas_dict = dict()


def getEncl():
    encsList = list()
    subprocess.run(["sudo", "./encList.sh"])
    for encString in open("exp.txt"):
        encsList.append(encString.strip('\n'))

    return encsList


def getNumSlots(encList):
    slotList = list()
    for enc in encList:
        subprocess.run(["sudo", "./slotsList.sh", f"{enc}"])
        for slotString in open("slots.txt"):
            tup = [enc, slotString.strip('\n')]
            slotList.append(tup)

    return slotList


def createSASDict():  # key: sas address, value: logical name
    subprocess.run(["sudo", "./sasDict.sh"])
    file = iter(open("/home/joshua/pocketKnife/sasDict.txt"))
    for line in file:
        # print(line)
        tokens = line.split()
        # print(tokens)
        value = tokens.pop().strip()
        key = tokens.pop().strip()
        # print(key,value)
        sas_dict[key] = value
    # print("SAS Dictionary")
    # print(sas_dict)


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
    # print(drive_dict) TODO: Make printout of dictionary more reader-friendly


def getSASaddr(slotList):
    for tup in slotList:
        subprocess.run(["sudo", "./sasAddr.sh", f"{tup[0]}", f"{tup[1]}"])
        for sasAddr in open("sasAddr.txt"):
            # print("getSASfunction: ",sasAddr)
            tup.append(sasAddr.strip('\n'))
            # print(tup)
            # subprocess.run(["sudo","./logicName.sh",f"{sasAddr}"])
            # for name in open("logicName.txt"):
            #    subprocess.run(["sudo","cat","logicName.txt"])
            #    #print(name)
            #    tup.append(name)
            #    #print(tup)
    return slotList
    # return sasAddr #return as string instead of as SASAddress appended to end of List


def driveDump(testDict):
    with open('test.json', 'w') as file:
        file.write(json.dumps(testDict))


def driveRead():
    with open('test.json') as handle:
        return json.loads(handle.read())


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Drive Comparison", color="IMPORTANT")
        self.addForm("BLINK", secondForm, name="Drive LED Configuration", color="IMPORTANT")
        self.addForm("INSTRUCTIONS", thirdForm, name="Instructions", color="IMPORTANT")

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


class MainForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

        with open('drive.json') as handle:
            testJSON = json.loads(handle.read())
        test = list(testJSON.keys())
        setTest = set(testJSON.keys())
        setTest.add("/dev/sdz")

        t2 = self.add(npyscreen.BoxTitle, name="Start-Up:", max_height=len(test) + 3,
                      scroll_exit=True)
        t3 = self.add(npyscreen.BoxTitle, name="Current:", max_height=len(test) + 3,
                      scroll_exit=True)
        t4 = self.add(npyscreen.BoxTitle, name="Difference:", max_height=6,
                      scroll_exit=True)

        t2.values = test
        t3.values = t2.values
        t4.values = setTest.difference(set(test))

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application, "é"),
            ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Blink/Unblink LED", self.change_forms1),
            ("Instructions", self.change_forms2)
            ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def on_ok(self):
        npyscreen.notify_confirm("OK Button Pressed!")

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def change_forms1(self, *args, **keywords):
        change_to = "BLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms2(self, *args, **keywords):
        change_to = "INSTRUCTIONS"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class secondForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

        with open('drive.json') as handle:
            testJSON = json.loads(handle.read())
        test = list(testJSON.keys())

        drives = self.add(npyscreen.TitleMultiSelect, max_height=len(test)+2,
                          name="Drive LEDs to configure (press x to choose)", values=test, scroll_exit=True)

        blink = self.add(npyscreen.TitleSelectOne, max_height=4, value=[1, ], name="Turn the Drive LEDs on or off?",
                         values=["On", "Off"], scroll_exit=True)

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application)
        ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Compare", self.change_forms1),
            ("Instructions", self.change_forms2),
            ])

        key_of_choice = 'Return'
        what_to_display = 'Press {} for popup'.format(key_of_choice)

        self.add_handlers({key_of_choice: self.spawn_notify_popup})
        self.add(npyscreen.FixedText, value=what_to_display)

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def on_ok(self):
        exit()

    def change_forms1(self, *args, **keywords):
        change_to = "MAIN"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms2(self, *args, **keywords):
        change_to = "INSTRUCTIONS"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class thirdForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Exit Application", self.exit_application)
        ])

        self.m2 = self.add_menu(name="Tools", shortcut="b",)
        self.m2.addItemsFromList([
            ("Blink/Unblink ", self.change_forms1),
            ("Compare", self.change_forms2)
            ])

        self.edit()

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def on_ok(self):
        # Exit the application if the OK button is pressed.
        npyscreen.notify_wait("Goodbye!")
        self.parentApp.switchForm(None)

    def change_forms1(self, *args, **keywords):
        change_to = "BLINK"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

    def change_forms2(self, *args, **keywords):
        change_to = "MAIN"
        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


def ledBlink(expanderID, slotID):
    subprocess.run(["sudo", "sg_ses", f"--descriptor={slotID}", "--set=ident", f"{expanderID}"])
    print(f"Activated {slotID} on Expander {expanderID}")


def ledStop(expanderID, slotID):
    subprocess.run(["sudo", "sg_ses", f"--descriptor={slotID}", "--clear=ident", f"{expanderID}"])
    print(f"Deactivated {slotID} on Expander {expanderID}")


def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
