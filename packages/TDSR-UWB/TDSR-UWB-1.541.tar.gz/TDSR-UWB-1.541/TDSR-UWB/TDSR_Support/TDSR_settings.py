from pathlib import Path
from json import dumps, loads

__version__ = "1.541"

# loads and saves GUI settings. Also sets default values if settings file does not include all keys.
class appSettings():
    def __init__(self):
        self.settings = {}

    def settingsSetup(self):
        f = Path("UserSettings.txt")
        if f.is_file():
            f = open("UserSettings.txt", "r")
            self.settings = loads(f.read())
            f.close()
            # if given value is not already in saved settings, then give it a default value
            if 'showDrops' not in self.settings:
                self.settings['showDrops'] = 0
            if 'connectResp' not in self.settings:
                self.settings['connectResp'] = 0
            if 'chartDepth' not in self.settings:
                self.settings['chartDepth'] = 5000
            if 'memoryDepth' not in self.settings:
                self.settings['memoryDepth'] = 250000
            if 'rangeRequests' not in self.settings:
                self.settings['rangeRequests'] = 250
            if 'rangeRate' not in self.settings:
                self.settings['rangeRate'] = 5
            if 'reqRadio' not in self.settings:
                self.settings['reqRadio'] = "192.168.1.100"
            if 'respRadio' not in self.settings:
                self.settings['respRadio'] = "192.168.1.101"
            if 'respID' not in self.settings:
                self.settings['respID'] = "101"
            if 'logDirectory' not in self.settings:
                self.settings['logDirectory'] = "./data_directory/"
            if 'logFile' not in self.settings:
                self.settings['logFile'] = "logfile.log"
            if 'logJson' not in self.settings:
                self.settings['logJson'] = 1
            if 'logWhileIdle' not in self.settings:
                self.settings['logWhileIdle'] = 0
            if 'enableLogging' not in self.settings:
                self.settings['enableLogging'] = 0
            if 'logRangeInfoOnly' not in self.settings:
                self.settings['logRangeInfoOnly'] = 1
            if 'logDateBased' not in self.settings:
                self.settings['logDateBased'] = 0
            if 'logSegmented' not in self.settings:
                self.settings['logSegmented'] = 0
            if 'segmentTime' not in self.settings:
                self.settings['segmentTime'] = 60
            if 'guiUpdateRate' not in self.settings:
                self.settings['guiUpdateRate'] = 10
            if 'downloadDirectory' not in self.settings:
                self.settings['downloadDirectory'] = "./Downloads/"
            if 'savePosition' not in self.settings:
                self.settings['savePosition'] = "0,0"
        else:
            print("Creating Default Settings File")
            self.settings['showDrops'] = 0
            self.settings['connectResp'] = 0
            self.settings['chartDepth'] = 5000
            self.settings['memoryDepth'] = 250000
            self.settings['rangeRequests'] = 250
            self.settings['rangeRate'] = 5
            self.settings['reqRadio'] = "192.168.1.51"
            self.settings['respRadio'] = "192.168.1.52"
            self.settings['respID'] = "52"
            self.settings['logDirectory'] = "./data_directory/"
            self.settings['logFile'] = "logfile.log"
            self.settings['logJson'] = 1
            self.settings['logWhileIdle'] = 0
            self.settings['enableLogging'] = 0
            self.settings['logRangeInfoOnly'] = 1
            self.settings['logDateBased'] = 0
            self.settings['logSegmented'] = 0
            self.settings['segmentTime'] = 60
            self.settings['guiUpdateRate'] = 10
            self.settings['downloadDirectory'] = "./Downloads/"
            self.settings['savePosition'] = "0,0"
            file = open("UserSettings.txt", "w")
            file.write(dumps(self.settings))
            file.close()
# save settings is triggered when app closes down.
    def settingsSave(self):
        f = open("UserSettings.txt", "w")
        f.write(dumps(self.settings))
        f.close()
