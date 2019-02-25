import npyscreen
import json


class ExampleTUI(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", testApp, name="Drive Listing")
        self.addForm("Hal's", HalsTUI, name="Drive Actions")

class testApp(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Hal's")

    def create(self):
        with open('drive.json') as handle:
            testJSON = json.loads(handle.read())
        test = list(testJSON.keys())
        self.drives = self.add(npyscreen.TitleMultiSelect, max_height=len(test),
                               name="Drive LEDs to light up", values=test, scroll_exit=True)

    def on_ok(self):
        toHal = self.parentApp.getForm("Hal's")
        for i in len(self.drives):
            toHal.drives.value.append(self.drives.values[self.drives.value[i]])
        self.parentApp.switchForm("Hal's")


class HalsTUI(npyscreen.Form):
    def activate(self):
        self.edit()

    def create(self):
        self.drives = self.add(npyscreen.TitleFixedText, name="Drives Chosen: ")


if __name__ == "__main__":
    npyscreen.wrapper(ExampleTUI().run())
