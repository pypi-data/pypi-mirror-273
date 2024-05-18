from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QCheckBox,
        QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QTabWidget, QMainWindow, QTextBrowser, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, QByteArray
from PyQt6.QtGui import QFont, QPixmap, QScreen
from pyqtgraph import PlotWidget, mkPen
from pathlib import Path
from time import time, sleep

from json import loads, dumps
from os import path
from glob import glob
from sys import platform

from TDSR_Support import TDSR_logging
from TDSR_Support import TDSR_settings
from TDSR_Support import TDSR_radioControl
from TDSR_Support import TDSR_radioConnection

# Primary window GUI class. All sub windows are launched from here as well.
__version__ = "1.541"
# Primary application window and GUI
class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        title = "PennyWhistle Ranging GUI V" + __version__
        self.setWindowTitle(title)
        self.myScreen = app.primaryScreen()                      # self is mainwindow Widget and myScreen is the display it lives on
        self.monitor = self.myScreen.availableVirtualGeometry()  # space across entire virtual display
        app.aboutToQuit.connect(self.closeItDown)
        self.connectedResponder = 0
        self.connectedRequester = 0
        self.connectedMultiCast = 0
        self.radioConfigReq = None
        self.radioConfigResp = None
        self.defineSheets()
        self.platform = platform
        self.radioRanging = TDSR_radioControl.rangeCmds(self)
            # link in saved settings data
        self.settings = TDSR_settings.appSettings()
        self.settings.settingsSetup()
        self.appSettings = self.settings.settings
        self.initWindows()
        self.screenSetup()
        self.chipTempTimer = QTimer()
        self.setStyleSheet(self.mainWindowSheet)
        self.initGUI()
        self.show()
        self.appSetup()

    def screenSetup(self):
        allScreens = self.myScreen.virtualSiblings() # list of each available monitor as a QScreen
        # print(allScreens)
        if int(self.monitor.height()) < 1100:
            self.reduceSize = (1000 - int(self.monitor.height()) + 80)
        else:
            self.reduceSize = 0
        self.mainWindowHeight = 1000 - self.reduceSize
        self.mainWindowWidth = 1000
        savedPosition = self.appSettings['savePosition'].split(",")
        x = int(savedPosition[0])
        y = int(savedPosition[1])
        print(f"Detected Monitor Resolution: {self.monitor.width(), self.monitor.height()}")
        print(f"Saved Location: {x,y}")
        # Try to move to saved position
        if x < 0 or y < 0:
            x = 0
            y = 0
        if ((x + self.mainWindowWidth) > self.monitor.width()) or ((y + self.mainWindowHeight) > self.monitor.height()):
            x = 0
            y = 0
        self.move(self.monitor.left()+x, self.monitor.top()+y)
        self.setFixedSize(self.mainWindowWidth,self.mainWindowHeight)
        # figure out where we are and test if new size and position are valid
        for i in range(len(allScreens)):
            if self.screen() == allScreens[i]:
                currentScreen = allScreens[i]
        # screen1 = allScreens[0]
        # screen2 = allScreens[1]
        # print(screen1.size())
        # print(screen2.size())
        # if int(currentScreen.size().height()) < 1100:
        #     self.reduceSize = (1000 - int(currentScreen.size().height()) + 80)
        # else:
        #     self.reduceSize = 0
        # self.mainWindowHeight = 1000 - self.reduceSize
        # self.mainWindowWidth = 1000
        # if x < 0 or y < 0:
        #     x = 0
        #     y = 0
        # if ((x + self.mainWindowWidth) > currentScreen.size().width()) or ((y + self.mainWindowHeight) > currentScreen.size().height()):
        #     x = 0
        #     y = 0
        # self.move(currentScreen.availableGeometry().left()+x, currentScreen.availableGeometry().top()+y)
        self.positionWindows()


    def appSetup(self):
        self.multiCastIP = "239.255.92.43"
        self.radioIP_Port = 8888
        self.radioMultiCast_Port = 8890
        self.radioMode = 'idle'
        self.ipRadios = []
        self.usbRadios = []
        self.radioReq = None
        self.radioResp = None
        self.configID = 0
        self.radioConfigReq = None
        self.radioConfigResp = None
        self.radioStateReq = None
        self.radioStateResp = None
        self.radioReqNodeID = None
        self.radioRespNodeID = None
        self.rangeDispType = "precision"
        self.interface   = 'ip'
        self.messageTypes = self.radioMessageTypes("JsonDoc")
        self.mode = 4
        self.rangeMax = 0
        self.rangeMin = 1000000
        self.powerMax = -200
        self.powerMin = 0
        self.stdNoiseMax = -10
        self.stdNoiseMin = 20000
        self.maxNoiseMax = -10
        self.maxNoiseMin = 20000
        self.destSlotDataMax = 100
        self.consoleBuf = ""
        self.logFile = TDSR_logging.logData(self)
        self.radioScanComplete = False
        # tmp1 = TDSR_radioConnection.Radio(self, self.messageTypes, 'None', "", "")
        # tmp = tmp1.getMulticast()
        # print()
        # print(tmp)
        # print()
        # print(tmp.keys())
        self.usbRadios = self.getUSBPorts()
        # self.radioConnectMultiCast()
        self.ipRadios = self.getMultiCastRadioIPs()
        self.radioScanComplete = False
        self.compileRadioList()
        self.radioScanComplete = True
        self.radioConnectReq()
        self.radioConnectResp()
        self.statsTimer = QTimer()
        self.statsTimer.setInterval(4000)
        self.statsTimer.timeout.connect(self.updateStats)
        self.chipTempTimer = QTimer()
        self.chipTempTimer.setInterval(4000)
        self.chipTempTimer.timeout.connect(self.updateChipTemp)
        self.radioCheckTimer = QTimer()
        self.radioCheckTimer.setInterval(2000)
        self.radioCheckTimer.timeout.connect(self.radioCheck)
        self.radioCheckTimer.start()
        self.guiUpdateTimer = QTimer()
        updateTime = int(1000*(1/(int(self.appSettings['guiUpdateRate']))))
        self.guiUpdateTimer.setInterval(updateTime)
        self.guiUpdateTimer.timeout.connect(self.updateGUI)
        self.rangingActive = False
        self.rangeInProgress = False
        if self.connectedRequester == 1:
            self.chipTempTimer.start()
        text = "-- App Initialized\n"
        self.updateConsole(text)
        # for thread in threading.enumerate():
        #     print(thread.name)

# Connects to requester radio. Needed for ranging to run.
    def radioConnectReq(self):
        if self.connectedRequester != 1:
            radioName = self.appSettings['reqRadio']
            self.radioReq = None
            for radio in self.radioList:
                if radioName == radio['name'] and radioName != 'Disconnect':
                    self.radioReq = TDSR_radioConnection.Radio(self, self.messageTypes, radio['type'], radio['addr'], radio['port'])
            if self.radioReq == None:
                self.radioReq = TDSR_radioConnection.Radio(self, self.messageTypes, 'None', 'None', 'None')
            if self.radioReq.status == False:
                if self.appSettings['reqRadio'] == "Disconnect":
                    print("Not connected to a primary radio")
                else:
                    print(f"Could not connect to primary radio: {self.appSettings['reqRadio']}")
                self.connectedRequester = 0
                self.windowDataTransfer.radioData.reqMsgTimer.stop()
                self.chipTempTimer.stop()
                self.dispChipTemp.setText("-")
            else:
                self.windowDataTransfer.radioData.reqMsgTimer.start()
                self.radioConfigReq, addr = self.radioReq.API.radio_GetConfig_Request(self.appSettings['reqRadio'], self.configID)
                self.radioStateReq, addr = self.radioReq.API.radio_GetState_Request(self.appSettings['reqRadio'])
                self.radioReqNodeIDMsg, addr = self.radioReq.API.radio_GetNodeID_Request(self.appSettings['reqRadio'])
                self.radioReqNodeID = self.radioReqNodeIDMsg['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']
                self.chipTempTimer.start()
                self.connectedRequester = 1
            self.updateConnectReq(self.radioReq.status)

# Connects to responding radio. Needed to get stats and set configuration but not needed to range.
    def radioConnectResp(self):
        if self.check_connectResp.isChecked():
            self.appSettings['connectResp'] = 1
        else:
            self.appSettings['connectResp'] = 0
        if self.appSettings['connectResp'] == 1:
            if self.connectedResponder != 1:
                self.radioResp = None
                radioName = self.appSettings['respRadio']
                for radio in self.radioList:
                    if radioName == radio['name'] and radioName != 'Disconnect':
                        self.radioResp = TDSR_radioConnection.Radio(self, self.messageTypes, radio['type'], radio['addr'], radio['port'])
                if self.radioResp == None:
                    self.radioResp = TDSR_radioConnection.Radio(self, self.messageTypes, 'None', 'None', 'None')
                if self.radioResp.status == False:
                    if self.appSettings['reqRadio'] == "Disconnect":
                        print("Not connected to a secondary radio")
                    else:
                        print(f"Could not connect to secondary radio: {self.appSettings['respRadio']}")
                    self.connectedResponder = 0
                    self.windowDataTransfer.radioData.respMsgTimer.stop()
                else:
                    self.connectedResponder = 1
                    self.windowDataTransfer.radioData.respMsgTimer.start()
                    self.radioConfigResp, addr = self.radioResp.API.radio_GetConfig_Request(self.appSettings['respRadio'], self.configID)
                    self.radioStateResp, addr = self.radioResp.API.radio_GetState_Request(self.appSettings['respRadio'])
                    self.radioRespNodeID, addr = self.radioResp.API.radio_GetNodeID_Request(self.appSettings['respRadio'])
                    self.radioRespNodeID = self.radioRespNodeID['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']
                    self.updateRespID(self.radioRespNodeID)
                    # self.respMsgTimer.start()
                self.updateConnectResp(self.radioResp.status)
        else:
            if self.connectedResponder == 1:
                self.windowDataTransfer.radioData.respMsgTimer.stop()
                self.connectedResponder = 0
                self.radioResp.disconnect()
            self.updateConnectResp(False)

    def radioConnectMultiCast(self):
        if self.connectedMultiCast != 1:
            self.radioMultiCast = TDSR_radioConnection.Radio(self, self.messageTypes, 'ip', self.multiCastIP, self.radioMultiCast_Port)
            if self.radioMultiCast.status == False:
                self.connectedMultiCast = 0
            else:
                self.connectedMultiCast = 1

    def USBTest(self):
        print("Trying:", self.usbRadios[0]['addr'])
        usbRadio = TDSR_radioConnection.Radio(self, self.messageTypes, 'usb', 'connect', self.usbRadios[0]['addr'])
        stats,packet,addr = usbRadio.API.radio_GetIP_Request("USB")
        # packet = '{"RADIO_GET_IP_REQUEST":{"msgId": 101}}'
        # usbRadio.radioIf.sendPacket(packet)
        # print("trying again")
        # sleep(3)
        # packet = usbRadio.radioIf.readPacketInternal()
        # print("USBTest:", packet)
        # packet = usbRadio.radioIf.readPacketInternal()
        print("USBTest:", packet)
        usbRadio.radioIf.disconnect()

    def radioMessageTypes(self,top_dir):
        messageTypes = {}
        basePath = path.dirname(path.abspath(__file__))
        top_dir = basePath + "/" + top_dir + "/"
        if (path.isdir(top_dir)):
            filesTxt = glob(path.join(top_dir,"*.txt"))
            for filePair in filesTxt:
                with open(filePair, "r") as f:
                    testLines = f.readlines()
                    for ln in  testLines:
                        if ln:
                            jsontest = loads(ln)
                            messageTypes[list(jsontest.keys())[0]] = jsontest #jsontest[list(jsontest.keys())[0]]
        return messageTypes

# Get various running statistics from requester radio
    def getReqStats(self):
        if self.connectedRequester != 1:
            self.radioConnectReq()
        if self.connectedRequester == 1:
            stats, packet, addr = self.radioReq.API.radio_GetStats_Request(self.appSettings['reqRadio'])
            self.updateReqStats(packet)

# Get various running statistics from responder radio if connected
    def getRespStats(self):
        if self.connectedResponder != 1:
            self.radioConnectResp()
        if self.connectedResponder == 1:
            stats,packet,addr = self.radioResp.API.radio_GetStats_Request(self.appSettings['respRadio'])
            self.updateRespStats(packet)

# gets config information from requester radio
    def getReqConfig(self):
        self.radioConfigReq,addr = self.radioReq.API.radio_GetConfig_Request(self.appSettings['reqRadio'], self.configID)
        self.radioReqNodeID,addr = self.radioReq.API.radio_GetNodeID_Request(self.appSettings['reqRadio'])
        self.radioReqNodeID = self.radioReqNodeID['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']

# gets config information from responder radio
    def getRespConfig(self):
        self.radioConfigResp,addr = self.radioResp.API.radio_GetConfig_Request(self.appSettings['respRadio'], self.configID)
        self.radioRespNodeID, addr = self.radioResp.API.radio_GetNodeID_Request(self.appSettings['respRadio'])
        self.radioRespNodeID = self.radioRespNodeID['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']

# gets general radio information from requester radio
    def getReqRadioInfo(self):
        self.radioConnectReq()
        if self.connectedRequester == 1:
            stats,packet,addr = self.radioReq.API.radio_GetInfo_Request(self.appSettings['reqRadio'])
            self.showReqRadioInfo(packet)

    def getMultiCastRadioIPs(self):
        multiCast = TDSR_radioConnection.Radio(self, "", 'None', "", "")
        multiCastIPs = multiCast.getMulticast()
        ipRadios = []
        for radio in multiCastIPs.keys():
            radioObj = {}
            addr = radio
            radioObj['nodeId'] = multiCastIPs[radio]['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']
            radioObj['type'] = "ip"
            radioObj['name'] = addr
            radioObj['addr'] = addr
            radioObj['port'] = self.radioIP_Port
            ipRadios.append(radioObj)
        return ipRadios

    def getUSBPorts(self):
        usbRadiosCheck = TDSR_radioConnection.Radio(self, self.messageTypes, 'usb', '', 'find')
        radios = usbRadiosCheck.findUsbRadios()
        usbRadios = []
        for radio in radios:
            radioObj = {}
            radioName = str(radio)
            if "tty" in radioName:
                radioName = radioName.split(" ")
                radioAddr = radioName[0]
                radioName = radioName[0].split("/")
                radioName = radioName[2]
                radioName = "USB-Port " + radioName[len(radioName)-1:]
            if "COM" in radioName:
                radioName = radioName.split(" ")
                radioAddr = radioName[0]
                radioName = radioName[0]
                radioName = radioName + " USB"
            if "modem" in radioName:
                radioName = radioName.split(" ")
                radioAddr = radioName[0]
                radioName = radioName[0].split("modem")
                radioName = "USB " + radioName[1]
            radioObj['type'] = "usb"
            radioObj['name'] = radioName
            radioObj['addr'] = radioAddr
            radioObj['port'] = "connect"
            radioObj['nodeId'] = ""
            usbRadios.append(radioObj)
        return usbRadios

    def radioCheck(self):
        ipRadios = self.getMultiCastRadioIPs()
        usbRadios = self.getUSBPorts()
        radioChange = 0
        if len(ipRadios) == len(self.ipRadios) and len(usbRadios) == len(self.usbRadios):
            for radio in ipRadios:
                if radio not in self.ipRadios:
                    radioChange = 1
            for radio in usbRadios:
                if radio not in self.usbRadios:
                    radioChange = 1
        else:
            radioChange = 1
        if radioChange == 1:
            self.ipRadios = ipRadios
            self.usbRadios = usbRadios
            self.compileRadioList()
            print("Change to radio list detected")

    def compileRadioList(self):
        self.radioList = []
        radioObj = {}
        radioObj['type'] = "Disconnect"
        radioObj['name'] = "Disconnect"
        radioObj['addr'] = "Disconnect"
        self.radioList.append(radioObj)
        for radio in self.ipRadios:
            self.radioList.append(radio)
        for radio in self.usbRadios:
            self.radioList.append(radio)
        self.radioScanComplete = False
        self.dropMenuReqRadio.clear()
        self.dropMenuRespRadio.clear()
        radios = []
        for radio in self.radioList:
            radios.append(radio['name'])
        self.dropMenuReqRadio.addItems(radios)
        self.dropMenuRespRadio.addItems(radios)
        self.radioScanComplete = True
        radioIndex = self.dropMenuReqRadio.findText(self.appSettings['reqRadio'])
        if radioIndex != -1:
            self.radioScanComplete = False
            self.dropMenuReqRadio.setCurrentIndex(radioIndex)
            self.radioScanComplete = True
        else:
            if self.connectedRequester == 1:
                self.radioReq.disconnect()
                self.connectedRequester = 0
            self.dropMenuReqRadio.setCurrentIndex(0)
            self.appSettings['reqRadio'] = self.dropMenuReqRadio.currentText()
            self.updateConnectReq(False)
        radioIndex = self.dropMenuRespRadio.findText(self.appSettings['respRadio'])
        if radioIndex != -1:
            self.radioScanComplete = False
            self.dropMenuRespRadio.setCurrentIndex(radioIndex)
            self.radioScanComplete = True
        else:
            if self.connectedResponder == 1:
                self.radioResp.disconnect()
                self.connectedResponder = 0
            self.dropMenuRespRadio.setCurrentIndex(0)
            self.appSettings['respRadio'] = self.dropMenuRespRadio.currentText()
            self.updateConnectResp(False)

# gets general radio information from requester radio
    def getReqRadioChipTemp(self):
        self.radioConnectReq()
        if self.connectedRequester == 1:
            status,packet,addr = self.radioReq.API.radio_GetInfo_Request(self.appSettings['reqRadio'])
            if status:
                tmp = packet['RADIO_GET_INFO_CONFIRM']['chipTemp']
                # if tmp > 100:
                #     print(packet)
                # else:
                #     print(packet)
                tmp = "%0.1f" % tmp
                tmp = tmp + "(C)"
                return tmp
            return "-"

    def updateGUI(self):
        # print(self.radioReq.messageQueues['RANGE_INFO'].qsize())
        self.plotData()
        self.guiPacketUpdates(self.radioRanging.packetDisplay)

# gets general radio information from responder radio if connected
    def getRespRadioInfo(self):
        self.radioConnectResp()
        if self.connectedResponder == 1:
            stats,packet,addr = self.radioResp.API.radio_GetInfo_Request(self.appSettings['respRadio'])
            self.showRespRadioInfo(packet)
# Updates small range display and large one if open. Color codes each based on signal strength.
# Updates stat and data windows if them are open.
    def guiPacketUpdates(self, packet):
        if packet != None:
            if self.radioMode == 'networking':
                slot = int(packet['RANGE_INFO']['slotIdx'])
                idColor = self.pen[slot].color().getRgb()
                idColor = idColor[0:3]
                idColor = "QLineEdit {background-color: rgb" + str(idColor) + ";}"
            if packet['RANGE_INFO']['rangeStatus'] != 4 and packet['RANGE_INFO']['precisionRangeM'] != 0.0:
                self.dispRespID.setText(str(packet['RANGE_INFO']['responderId']))
            # else:
                # print("guiPacketUpdates Range Error")
            if str(packet['RANGE_INFO']['rxPower']) != "-Infinity" and str(packet['RANGE_INFO']['rxPower']) != "-inf":
                rxPower = round(float(packet['RANGE_INFO']['rxPower']))
            else:
                rxPower = -120
                print("\n-Infinity Found")
                print("rxPower: ", str(packet['RANGE_INFO']['rxPower']))
                print("MaxGrowCIR: ", str(packet['RANGE_INFO']['maxGrowthCIR']))
                print("rxPreamCount: ", str(packet['RANGE_INFO']['rxPreamCount']))
                print("precRange: ", str(packet['RANGE_INFO']['precisionRangeM']))
                print("rangeStatus: ", str(packet['RANGE_INFO']['rangeStatus']))
            shadeFactor = 10
            if self.radioConfigReq[list(self.radioConfigReq.keys())[0]]['dataRate'] == "DWT_BR_110K":
                shadeFactor = 10
            if self.radioConfigReq[list(self.radioConfigReq.keys())[0]]['dataRate'] == "DWT_BR_850K":
                shadeFactor = 15
            if self.radioConfigReq[list(self.radioConfigReq.keys())[0]]['dataRate'] == "DWT_BR_6M8":
                shadeFactor = 20
            # print(shadeFactor)
            shade = 255 + ((82 + rxPower) * shadeFactor)
            if shade < 0:
                shade = 0
            if shade > 255:
                shade = 255
            tmp = "QLineEdit {background-color: rgb(255," + str(shade) + "," + str(shade) + ");}"
            # print(rxPower, shade)
            if packet['RANGE_INFO']['rangeStatus'] == 0 and packet['RANGE_INFO']['precisionRangeM'] != 0.0:    # have GUI show if range is good or bad with color indication
                self.dispRange.setStyleSheet(tmp)
                if self.radioMode == 'networking':
                    self.dispRespID.setStyleSheet(idColor)
                else:
                    self.dispRespID.setStyleSheet("QLineEdit {background-color: lightgreen;}")
            else:
                # print("guiPacketUpdates Range Error Error2")
                self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,0,0);}")
                if self.radioMode != 'networking':
                    self.dispRespID.setStyleSheet("QLineEdit {background-color: coral;}")
            displayRange = ""
            if self.rangeDispType == "precision":
                displayRange = f"{packet['RANGE_INFO']['precisionRangeM']:.3f}"
            else:
                displayRange = f"{packet['RANGE_INFO']['filteredRangeM']:.3f}"
            if self.windowRangeLarge.isVisible():   # If large range window open, then update it.
                self.windowRangeLarge.processData(displayRange,shade)
            if self.windowRangeData.isVisible():
                self.windowRangeData.processData(packet)
            self.dispRange.setText(displayRange)
            if self.radioMode == 'ranging':
                for k in range(len(self.dispStatWindow)):
                    self.dispStatWindow[k].setText(str(packet['RANGE_INFO'][self.statKeys[k]]))
        else:
            self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,0,0);}")
            self.dispRespID.setStyleSheet("QLineEdit {background-color: coral;}")
            if self.windowRangeLarge.isVisible():   # If large range window open, then update it.
                self.windowRangeLarge.processData(str(0),255)

# Updates charge with whichever data is selected to display
    def plotData(self):
        self.appSettings['chartDepth'] = int(self.dispChartStore.text())
        # case for no data in any of the arrays
        self.plotYT2 = []
        if (len(self.radioRanging.chartPointsX) == 0) and (len(self.windowNetwork.netXArray) == 0):
            self.chartData1.setData([], [])
            self.chartData2.setData([], [])
            self.chartDataT.setData([], [])
            self.chartDataB.setData([], [])
        else:
            # Case for Ranging data
            if len(self.radioRanging.chartPointsX) > 0:
                if self.check_plotDrops.isChecked():
                    self.plotX = self.radioRanging.chartPointsXAll
                    # Set appropriate data for Y so don't modify original datasets.
                    if self.dropMenuChart.currentText() == "Ranges":
                        self.plotYT = self.radioRanging.rangeArrayAll
                    if self.dropMenuChart.currentText() == "Filtered":
                        self.plotYT = self.radioRanging.rangeFilteredArrayAll
                    if self.dropMenuChart.currentText() == "Both":
                        self.plotYT = self.radioRanging.rangeArrayAll
                        self.plotYT2 = self.radioRanging.rangeFilteredArrayAll
                    if self.dropMenuChart.currentText() == "RxPower":
                        self.plotYT = self.radioRanging.rxPowerArrayAll
                    if self.dropMenuChart.currentText() == "MaxNoise":
                        self.plotYT = self.radioRanging.maxNoiseArrayAll
                    if self.dropMenuChart.currentText() == "StdNoise":
                        self.plotYT = self.radioRanging.stdNoiseArrayAll
                    if self.dropMenuChart.currentText() == "Multi":
                        self.plotYT = self.radioRanging.rangeArrayAll
                        self.plotYB = self.radioRanging.rxPowerArrayAll
                    if self.dropMenuChart.currentText() == "MultiFilt":
                        self.plotYT = self.radioRanging.rangeFilteredArrayAll
                        self.plotYB = self.radioRanging.rxPowerArrayAll
                    if len(self.plotYT) > int(self.appSettings['chartDepth']):
                        self.plotX = self.plotX[(len(self.plotX) - int(self.appSettings['chartDepth'])):]
                        self.plotYT = self.plotYT[(len(self.plotYT) - int(self.appSettings['chartDepth'])):]
                        if (len(self.plotYT2) > 0):
                            self.plotYT2 = self.plotYT2[(len(self.plotYT2) - int(self.appSettings['chartDepth'])):]
                        self.plotYB = self.plotYB[(len(self.plotYB) - int(self.appSettings['chartDepth'])):]
                    if "Multi" in self.dropMenuChart.currentText():
                        self.chartDataT.setData(self.plotX, self.plotYT)
                        self.chartDataB.setData(self.plotX, self.plotYB)
                    else:
                        self.chartData1.setData(self.plotX, self.plotYT)
                        self.chartData2.setData(self.plotX, self.plotYT2)
                else:
                    self.plotX = self.radioRanging.chartPointsX
                    # Set appropriate data for Y so don't modify original datasets.
                    if self.dropMenuChart.currentText() == "Ranges":
                        self.plotYT = self.radioRanging.rangeArray
                    if self.dropMenuChart.currentText() == "Filtered":
                        self.plotYT = self.radioRanging.rangeFilteredArray
                    if self.dropMenuChart.currentText() == "Both":
                        self.plotYT = self.radioRanging.rangeArray
                        self.plotYT2 = self.radioRanging.rangeFilteredArray
                    if self.dropMenuChart.currentText() == "RxPower":
                        self.plotYT = self.radioRanging.rxPowerArray
                    if self.dropMenuChart.currentText() == "MaxNoise":
                        self.plotYT = self.radioRanging.maxNoiseArray
                    if self.dropMenuChart.currentText() == "StdNoise":
                        self.plotYT = self.radioRanging.stdNoiseArray
                    if self.dropMenuChart.currentText() == "Multi":
                        self.plotYT = self.radioRanging.rangeArray
                        self.plotYB = self.radioRanging.rxPowerArray
                    if self.dropMenuChart.currentText() == "MultiFilt":
                        self.plotYT = self.radioRanging.rangeFilteredArray
                        self.plotYB = self.radioRanging.rxPowerArray
                    if len(self.plotYT) > int(self.appSettings['chartDepth']):
                        self.plotX = self.plotX[(len(self.plotX) - int(self.appSettings['chartDepth'])):]
                        self.plotYT = self.plotYT[(len(self.plotYT) - int(self.appSettings['chartDepth'])):]
                        if (len(self.plotYT2) > 0):
                            self.plotYT2 = self.plotYT2[(len(self.plotYT2) - int(self.appSettings['chartDepth'])):]
                        self.plotYB = self.plotYB[(len(self.plotYB) - int(self.appSettings['chartDepth'])):]
                    if "Multi" in self.dropMenuChart.currentText():
                        self.chartDataT.setData(self.plotX, self.plotYT)
                        self.chartDataB.setData(self.plotX, self.plotYB)
                    else:
                        self.chartData1.setData(self.plotX, self.plotYT)
                        self.chartData2.setData(self.plotX, self.plotYT2)

            # Case for Network data
            else:
                shortTest = True  # if true in end, it means all arrays were same length
                shortest = len(self.windowNetwork.netXArray)
                for k in range(len(self.windowNetwork.slotMap)):
                    for j in range(len(self.windowNetwork.localSlots)):
                        if k == self.windowNetwork.localSlots[j][0]:
                            if len(self.windowNetwork.netRangeArray[k]) < shortest:
                                shortest = len(self.windowNetwork.netRangeArray[k])
                                shortTest = False
                tmp1 = self.windowNetwork.netXArray
                tmp1 = tmp1[:shortest]
                tmp2b = []
                if len(tmp1) > int(self.appSettings['chartDepth']):
                    tmp1 = tmp1[(len(tmp1) - int(self.appSettings['chartDepth'])):]
                for k in range(len(self.windowNetwork.slotMap)):
                    for j in range(len(self.windowNetwork.localSlots)):
                        if k == self.windowNetwork.localSlots[j][0]:
                            if "Multi" not in self.dropMenuChart.currentText():
                                if self.dropMenuChart.currentText() == "Ranges":
                                    tmp2 = self.windowNetwork.netRangeArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "Filtered":
                                    tmp2 = self.windowNetwork.netRangeFilteredArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "Both":
                                    tmp2 = self.windowNetwork.netRangeArray[k][:shortest]
                                    tmp2b = self.windowNetwork.netRangeFilteredArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "RxPower":
                                    tmp2 = self.windowNetwork.netPowerArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "MaxNoise":
                                    tmp2 = self.windowNetwork.netMaxNoiseArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "StdNoise":
                                    tmp2 = self.windowNetwork.netStdNoiseArray[k][:shortest]
                                if len(tmp2) > int(self.appSettings['chartDepth']):
                                    tmp2 = tmp2[(len(tmp2) - int(self.appSettings['chartDepth'])):]
                                self.windowNetwork.netPlot1[k].setData(tmp1,tmp2)
                                self.windowNetwork.netPlot2[k].setData(tmp1,tmp2b)
                            else:
                                tmp2 = []
                                if self.dropMenuChart.currentText() == "Multi":
                                    tmp2 = self.windowNetwork.netRangeArray[k][:shortest]
                                if self.dropMenuChart.currentText() == "MultiFilt":
                                    tmp2 = self.windowNetwork.netRangeFilteredArray[k][:shortest]
                                tmp3 = self.windowNetwork.netPowerArray[k][:shortest]
                                if len(tmp2) > int(self.appSettings['chartDepth']):
                                    tmp2 = tmp2[(len(tmp2) - int(self.appSettings['chartDepth'])):]
                                if len(tmp3) > int(self.appSettings['chartDepth']):
                                    tmp3 = tmp3[(len(tmp3) - int(self.appSettings['chartDepth'])):]
                                self.windowNetwork.netPlotT[k].setData(tmp1,tmp2)
                                self.windowNetwork.netPlotB[k].setData(tmp1,tmp3)

# Checks to see if chart needs to be scaled
    def checkChartRange(self, packet):
        if packet == None:
            if len(self.windowNetwork.netRangeArray) == 1:
                self.rangeMax = 0
                self.rangeMin = 1000000
                self.powerMax = -200
                self.powerMin = 0
                self.stdNoiseMax = -10
                self.stdNoiseMin = 20000
                self.maxNoiseMax = -10
                self.maxNoiseMin = 20000
            if self.dropMenuChart.currentText() == "Ranges" or self.dropMenuChart.currentText() == "Filtered" or "Multi" in self.dropMenuChart.currentText():
                self.chartScale([self.rangeMax, self.rangeMin],[self.powerMax, self.powerMin])
            if self.dropMenuChart.currentText() == "RxPower":
                self.chartScale([self.powerMax, self.powerMin],[self.powerMax, self.powerMin])
            if self.dropMenuChart.currentText() == "MaxNoise":
                self.chartScale([self.maxNoiseMax, self.maxNoiseMin],[self.powerMax, self.powerMin])
            if self.dropMenuChart.currentText() == "StdNoise":
                self.chartScale([self.stdNoiseMax, self.stdNoiseMin],[self.powerMax, self.powerMin])
        else:
            tmp = float(packet['RANGE_INFO']['precisionRangeM'])
            if tmp > self.rangeMax or tmp < self.rangeMin:
                if tmp > self.rangeMax:
                    self.rangeMax = tmp
                if tmp < self.rangeMin:
                    self.rangeMin = tmp
                if self.dropMenuChart.currentText() == "Ranges" or self.dropMenuChart.currentText() == "Filtered" or "Multi" in self.dropMenuChart.currentText():
                    self.chartScale([self.rangeMax, self.rangeMin],[self.powerMax, self.powerMin])
            rxPower = str(packet['RANGE_INFO']['rxPower'])
            if rxPower != "-Infinity" and rxPower != "-inf":
                rxPower = round(float(packet['RANGE_INFO']['rxPower']))
            else:
                rxPower = -120
            if rxPower > self.powerMax or rxPower < self.powerMin:
                if rxPower > self.powerMax:
                    self.powerMax = rxPower
                if rxPower < self.powerMin:
                    self.powerMin = rxPower
                if self.dropMenuChart.currentText() == "RxPower":
                    self.chartScale([self.powerMax, self.powerMin],[self.powerMax, self.powerMin])
            tmp = int(packet['RANGE_INFO']['maxNoise'])
            if tmp > self.maxNoiseMax or tmp < self.maxNoiseMin:
                if tmp > self.maxNoiseMax:
                    self.maxNoiseMax = tmp
                if tmp < self.maxNoiseMin:
                    self.maxNoiseMin = tmp
                if self.dropMenuChart.currentText() == "MaxNoise":
                    self.chartScale([self.maxNoiseMax, self.maxNoiseMin],[self.powerMax, self.powerMin])
            tmp = int(packet['RANGE_INFO']['stdNoise'])
            if tmp > self.stdNoiseMax or tmp < self.stdNoiseMin:
                if tmp > self.stdNoiseMax:
                    self.stdNoiseMax = tmp
                if tmp < self.stdNoiseMin:
                    self.stdNoiseMin = tmp
                if self.dropMenuChart.currentText() == "StdNoise":
                    self.chartScale([self.stdNoiseMax, self.stdNoiseMin],[self.powerMax, self.powerMin])

# Scales chart based on available data.
    def chartScale(self, yDataT, yDataB):
        if len(yDataT) == 0:
            self.yScalePos = -10000
            self.yScaleNeg = 10000
        else:
            tmp = yDataT[0]
            if tmp > 0:
                self.yScalePos = yDataT[0] * 1.2
            else:
                self.yScalePos = yDataT[0] * 0.8
            tmp = yDataT[1]
            if tmp > 0:
                self.yScaleNeg = yDataT[1] * 0.8
            else:
                self.yScaleNeg = yDataT[1] * 1.2
            if self.dropMenuChart.currentText() == "RxPower":
                if self.yScalePos > -75:
                    self.yScalePos = -75
                if self.yScaleNeg < -130:
                    self.yScaleNeg = -130
        self.dataWindow.setYRange(self.yScaleNeg, self.yScalePos,padding = 0)
        if len(yDataT) == 0:
            self.yScalePosT = -10000
            self.yScaleNegT = 10000
        else:
            tmp = yDataT[0]
            if tmp > 0:
                self.yScalePosT = yDataT[0] * 1.2
            else:
                self.yScalePosT = yDataT[0] * 0.8
            tmp = yDataT[1]
            if tmp > 0:
                self.yScaleNegT = yDataT[1] * 0.8
            else:
                self.yScaleNegT = yDataT[1] * 1.2
        self.dataWindowT.setYRange(self.yScaleNegT, self.yScalePosT,padding = 0)
        if len(yDataB) == 0:
            self.yScalePosB = -10000
            self.yScaleNegB = 10000
        else:
            tmp = yDataB[0]
            if tmp > 0:
                self.yScalePosB = yDataB[0] * 1.2
            else:
                self.yScalePosB = yDataB[0] * 0.8
            tmp = yDataB[1]
            if tmp > 0:
                self.yScaleNegB = yDataB[1] * 0.8
            else:
                self.yScaleNegB = yDataB[1] * 1.2
        if "Multi" in self.dropMenuChart.currentText():
            if self.yScalePosB > -75:
                self.yScalePosB = -75
            if self.yScaleNegB < -130:
                self.yScaleNegB = -130
        self.dataWindowB.setYRange(self.yScaleNegB, self.yScalePosB,padding = 0)

# Sets up main window GUI.
    def initGUI(self):
        self.guiFont = guiFonts()
        self.definePens()
        self.TDSR = TDSR()
        self.tdsr_label = QLabel(self)
        # self.tdsr_logo = QPixmap('TDSR_Support/TDSR_logo_133x64.png')
        self.tdsr_logo = self.TDSR.logo()
        self.tdsr_label.setPixmap(self.tdsr_logo)
        self.tdsr_label.move(10,60)
        self.tdsr_label.resize(133,64)

        self.labelStatWindow = []
        self.dispStatWindow = []
        self.statWindows = ["Packets", "Rng Success %"]
        self.statKeys = ['packets', 'successRate']
        yStart = 0
        xStart = 730
        xBias = 0
        yBias = 0
        xBump = 140
        yBump = 75
        xWidth = 120    # Width of label/display
        yWidth = 40     # height of label/display
        x = 0
        y = 0
        for k in range(len(self.statWindows)):
            if x > 0:
                y = y + 1
                x = 0
            tmpL = QLabel(self)
            tmpL.resize(xWidth,yWidth)
            tmpL.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias)
            tmpL.setFont(self.guiFont.guiFont14)
            tmpL.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpL.setText(self.statWindows[k])
            tmpD = QLineEdit(self)
            tmpD.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
            tmpD.resize(xWidth,yWidth)
            tmpD.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpD.setStyleSheet("QLineEdit {background-color: lightyellow;}")
            tmpD.setFont(self.guiFont.guiFont18)
            tmpD.setText("-")
            self.labelStatWindow.append(tmpL)
            self.dispStatWindow.append(tmpD)
            x = x + 1

        self.guiFont = guiFonts()
        self.but_tuning = QPushButton(self)
        self.but_tuning.resize(10, 10)
        self.but_tuning.setFont(self.guiFont.guiFont18)
        self.but_tuning.setStyleSheet("QPushButton {background-color: black; color: black;}")
        self.but_tuning.move(76, 103)
        self.but_tuning.clicked.connect(self.windowChipTuning.displayWindow)

        yStart = 0
        xStart = 170
        xBias = -25
        yBias = 45
        xBump = 180
        yBump = 80
        xWidth = 120
        yWidth = 40
        x = 5
        y = 0
        self.but_run = QPushButton('Start\nRanging', self)
        self.but_run.setToolTip('Start/Stop Ranging')
        self.but_run.resize(100, 100)
        self.but_run.setFont(self.guiFont.guiFont18)
        self.but_run.setStyleSheet(self.buttonSheetBlue)
        self.but_run.move(x*xBump+xBias, y*yBump+yBias)
        self.but_run.clicked.connect(self.radioRanging.toggleRun)

        xStart = 715
        yStart = 145
        xBias = 0
        yBias = 0
        xBump = 140
        yBump = 80
        xWidth = 120
        yWidth = 80
        x = 0
        y = 0
        self.labelRangeRunTotal = QLabel(self)
        self.labelRangeRunTotal.resize(xWidth,yWidth)
        self.labelRangeRunTotal.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelRangeRunTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRangeRunTotal.setFont(self.guiFont.guiFont18)
        self.labelRangeRunTotal.setText("Range\nRequests")
        yStart = 195
        xWidth = 130
        xStart = 715
        self.labelRangeRate = QLabel(self)
        self.labelRangeRate.resize(xWidth,yWidth)
        self.labelRangeRate.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelRangeRate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRangeRate.setFont(self.guiFont.guiFont18)
        self.labelRangeRate.setText("Delay(ms)")
        yStart = 245
        xWidth = 130
        xStart = 715
        self.labelGuiUpdateRate = QLabel(self)
        self.labelGuiUpdateRate.resize(xWidth,yWidth)
        self.labelGuiUpdateRate.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelGuiUpdateRate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelGuiUpdateRate.setFont(self.guiFont.guiFont18)
        self.labelGuiUpdateRate.setText("DispRate(hz)")

        xStart = 850
        yStart = 165
        xWidth = 140
        yWidth = 40
        self.dispRangeRunTotal = QLineEdit(self)
        self.dispRangeRunTotal.setToolTip('Number of ranges to request')
        self.dispRangeRunTotal.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispRangeRunTotal.setFont(self.guiFont.guiFont18)
        self.dispRangeRunTotal.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispRangeRunTotal.resize(xWidth,yWidth)
        self.dispRangeRunTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRangeRunTotal.setText(str(self.appSettings['rangeRequests']))
        self.dispRangeRunTotal.editingFinished.connect(self.updateRunTotal)

        yStart = 215
        self.dispRangeRate = QLineEdit(self)
        self.dispRangeRate.setToolTip('Number of milliseconds between range requests. Min = 0. No Max')
        # self.dispRangeRate.setToolTip('GUI Update Rate. High GUI rates can cause missed ranges. Recommend 10hz, Max = 100hz')
        self.dispRangeRate.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispRangeRate.setFont(self.guiFont.guiFont18)
        self.dispRangeRate.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispRangeRate.resize(xWidth,yWidth)
        self.dispRangeRate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRangeRate.setText(str(self.appSettings['rangeRate']))
        self.dispRangeRate.editingFinished.connect(self.updateRangeRate)

        yStart = 265
        self.dispGuiUpdateRate = QLineEdit(self)
        self.dispGuiUpdateRate.setToolTip('GUI Update Rate. High GUI rates can cause missed ranges. Recommend 10hz, Max = 100hz')
        self.dispGuiUpdateRate.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispGuiUpdateRate.setFont(self.guiFont.guiFont18)
        self.dispGuiUpdateRate.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispGuiUpdateRate.resize(xWidth,yWidth)
        self.dispGuiUpdateRate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispGuiUpdateRate.setText(str(self.appSettings['guiUpdateRate']))
        self.dispGuiUpdateRate.editingFinished.connect(self.updateGuiUpdateRate)

        xStart = 10
        yStart = 170
        xBias = 0
        yBias = 0
        xBump = 140
        yBump = 80
        xWidth = 700
        yWidth = 180
        self.consoleOutput = QTextBrowser(self)
        self.consoleOutput.setGeometry(xStart,yStart,xWidth, yWidth)
        self.consoleOutput.setText("")
        self.consoleOutput.setStyleSheet("QTextBrowser {background-color: rgb(240,240,240);}")
        self.consoleOutputScrollBar = self.consoleOutput.verticalScrollBar()

        xStart = 150
        yStart = 0
        xBias = 0
        yBias = 0
        xBump = 210
        yBump = 75
        xWidth = 200
        yWidth = 40
        x = 0
        y = 0
        self.labelreqRadio = QLabel(self)
        self.labelreqRadio.resize(xWidth,yWidth)
        self.labelreqRadio.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelreqRadio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelreqRadio.setFont(self.guiFont.guiFont20)
        self.labelreqRadio.setText("Primary Radio")
        self.dropMenuReqRadio = QComboBox(self)
        self.dropMenuReqRadio.resize(xWidth,yWidth)
        self.dropMenuReqRadio.setToolTip("Select range requesting radio")
        self.dropMenuReqRadio.setFont(self.guiFont.guiFont20)
        self.dropMenuReqRadio.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dropMenuReqRadio.addItems([])
        self.dropMenuReqRadio.setEditable(False)
        self.dropMenuReqRadio.setStyleSheet(self.dropSheetBlue)
        self.dropMenuReqRadio.currentTextChanged.connect(self.updateReqRadio)

        x = 0
        y = 1
        self.labelrespRadio = QLabel(self)
        self.labelrespRadio.resize(xWidth,yWidth)
        self.labelrespRadio.move(x*xBump + xStart + xBias + 10, yStart + y*yBump + yBias)
        self.labelrespRadio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelrespRadio.setFont(self.guiFont.guiFont20)
        self.labelrespRadio.setText("Secondary Radio")

        self.dropMenuRespRadio = QComboBox(self)
        self.dropMenuRespRadio.resize(xWidth,yWidth)
        self.dropMenuRespRadio.setToolTip("Select range responding radio")
        self.dropMenuRespRadio.setFont(self.guiFont.guiFont20)
        self.dropMenuRespRadio.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dropMenuRespRadio.addItems([])
        self.dropMenuRespRadio.setEditable(False)
        self.dropMenuRespRadio.setStyleSheet(self.dropSheetBlue)
        self.dropMenuRespRadio.currentTextChanged.connect(self.updateRespRadio)

        self.check_connectResp = QCheckBox('', self)
        self.check_connectResp.setToolTip('Connect GUI to Responding Radio')
        self.check_connectResp.setFont(self.guiFont.guiFont14)
        self.check_connectResp.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.check_connectResp.resize(200,40)
        if self.appSettings['connectResp'] == 0:
            self.check_connectResp.setChecked(False)
        else:
            self.check_connectResp.setChecked(True)
        self.check_connectResp.stateChanged.connect(self.radioConnectResp)

        x = 1
        y = 0
        self.labelReqID = QLabel(self)
        self.labelReqID.resize(xWidth,yWidth)
        self.labelReqID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelReqID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelReqID.setFont(self.guiFont.guiFont20)
        self.labelReqID.setText("Primary Node ID")
        self.dispReqID = QLineEdit(self)
        self.dispReqID.setToolTip("Reported Node ID of requesting radio. Can be updated in Settings Window")
        self.dispReqID.setFont(self.guiFont.guiFont20)
        self.dispReqID.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispReqID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispReqID.resize(xWidth,yWidth)
        self.dispReqID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispReqID.setText("-")

        x = 1
        y = 1
        self.labelRespID = QLabel(self)
        self.labelRespID.resize(xWidth,yWidth)
        self.labelRespID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelRespID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRespID.setFont(self.guiFont.guiFont20)
        self.labelRespID.setText("Dest Node ID")
        self.dispRespID = QLineEdit(self)
        self.dispRespID.setToolTip("Enter node ID of radio being ranged to")
        self.dispRespID.setFont(self.guiFont.guiFont20)
        self.dispRespID.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispRespID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispRespID.resize(xWidth,yWidth)
        self.dispRespID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRespID.setText(self.appSettings['respID'])
        self.dispRespID.editingFinished.connect(self.setRespID)

        xBump = 210
        xWidth = 120
        yBias = 35
        x = 2
        y = 0
        self.but_RadioConfigReq = QPushButton('Req Settings', self)
        self.but_RadioConfigReq.setToolTip('Show Requester Radio Configuration Screen')
        self.but_RadioConfigReq.resize(xWidth, yWidth)
        self.but_RadioConfigReq.setStyleSheet(self.buttonSheetBlue)
        self.but_RadioConfigReq.setFont(self.guiFont.guiFont14)
        self.but_RadioConfigReq.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_RadioConfigReq.clicked.connect(self.windowConfigReq.displayWindow)

        x = 2
        y = 1
        self.but_RadioConfigResp = QPushButton('Resp Settings', self)
        self.but_RadioConfigResp.setToolTip('Show Responder Radio (if connected) Configuration Screen')
        self.but_RadioConfigResp.resize(xWidth, yWidth)
        self.but_RadioConfigResp.setStyleSheet(self.buttonSheetBlue)
        self.but_RadioConfigResp.setFont(self.guiFont.guiFont14)
        self.but_RadioConfigResp.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_RadioConfigResp.clicked.connect(self.windowConfigResp.displayWindow)

        xStart = 10
        yStart = 350
        xBias = 0
        yBias = 0
        xBump = 180
        yBump = 80
        xWidth = 160
        yWidth = 50
        x = 0
        y = 0
        self.labelChipTemp = QLabel(self)
        self.labelChipTemp.resize(xWidth,yWidth)
        self.labelChipTemp.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelChipTemp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelChipTemp.setFont(self.guiFont.guiFont20)
        self.labelChipTemp.setText("RF IC Temp")
        self.dispChipTemp = QLineEdit(self)
        self.dispChipTemp.setFont(self.guiFont.guiFont20)
        self.dispChipTemp.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 45)
        self.dispChipTemp.resize(xWidth,yWidth)
        self.dispChipTemp.setToolTip("Internal Temperature of RF IC")
        self.dispChipTemp.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispChipTemp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        x = 1
        y = 0
        dropMenuOptions = ["Ranges", "Filtered", "Both", "RxPower", "MaxNoise", "StdNoise", "Multi", "MultiFilt"]
        self.labelDropMenuChart = QLabel(self)
        self.labelDropMenuChart.resize(xWidth,yWidth)
        self.labelDropMenuChart.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelDropMenuChart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelDropMenuChart.setFont(self.guiFont.guiFont20)
        self.labelDropMenuChart.setText("Chart Options")
        # xWidth = 160
        self.dropMenuChart = QComboBox(self)
        self.dropMenuChart.resize(xWidth,yWidth)
        self.dropMenuChart.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 45)
        self.dropMenuChart.setFont(self.guiFont.guiFont20)
        self.dropMenuChart.addItems(dropMenuOptions)
        self.dropMenuChart.setEditable(False)
        self.dropMenuChart.setStyleSheet(self.dropSheetBlue)
        self.dropMenuChart.setToolTip("Pick what should be charted")
        self.dropMenuChart.currentTextChanged.connect(self.updateDropMenuChart)
        x = 2
        y = 0
        self.labelChartStore = QLabel(self)
        self.labelChartStore.resize(xWidth,yWidth)
        self.labelChartStore.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelChartStore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelChartStore.setFont(self.guiFont.guiFont20)
        self.labelChartStore.setText("Chart Depth")
        self.dispChartStore = QLineEdit(self)
        self.dispChartStore.setFont(self.guiFont.guiFont20)
        self.dispChartStore.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 45)
        self.dispChartStore.resize(xWidth,yWidth)
        self.dispChartStore.setToolTip("Number of datapoints chart holds before scrolling.\nAffects memory usage and CPU overhead.")
        self.dispChartStore.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispChartStore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispChartStore.setText(str(self.appSettings['chartDepth']))
        self.dispChartStore.editingFinished.connect(self.updateChartStore)
        x = 3
        y = 0
        self.labelMemoryDepth = QLabel(self)
        self.labelMemoryDepth.resize(xWidth,yWidth)
        self.labelMemoryDepth.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelMemoryDepth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelMemoryDepth.setFont(self.guiFont.guiFont20)
        self.labelMemoryDepth.setText("Memory Depth")
        self.dispMemoryDepth = QLineEdit(self)
        self.dispMemoryDepth.setFont(self.guiFont.guiFont20)
        self.dispMemoryDepth.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 45)
        self.dispMemoryDepth.resize(xWidth,yWidth)
        self.dispMemoryDepth.setToolTip("Number of datapoints held in range data array ring buffers.\nAffects memory usage and CPU overhead.")
        self.dispMemoryDepth.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispMemoryDepth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispMemoryDepth.setText(str(self.appSettings['memoryDepth']))
        self.dispChartStore.editingFinished.connect(self.updateMemoryDepth)

        xStart = 755
        yStart = 305
        xBias = 0
        yBias = 0
        xBump = 0
        yBump = 0
        xWidth = 200
        yWidth = 50
        x = 0
        y = 0
        self.labelRange = QLabel(self)
        self.labelRange.resize(xWidth,yWidth)
        self.labelRange.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 5)
        self.labelRange.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRange.setFont(self.guiFont.guiFont30)
        self.labelRange.setText("Range(m)")
        xStart = 735
        yStart = 365
        xWidth = 240
        yWidth = 80
        self.dispRange = QLineEdit(self)
        self.dispRange.setFont(self.guiFont.guiFont50)
        self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,255,255);}")
        self.dispRange.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispRange.resize(xWidth,yWidth)
        self.dispRange.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRange.setText("-")
        self.guiRange = 1
        xStart = 10
        yStart = 210
        xBump = 240
        yBump = 80
        # Range Chart

        self.dataWindow = PlotWidget(self)
        # self.dataWindow.setYRange(self.yScaleNeg,self.yScalePos,padding = 0)
        # self.dataWindow.setBackground(255,0,0,255)
        self.dataWindow.setBackground([230,230,230])
        self.dataWindow.setGeometry(5,450,990,500 - self.reduceSize)
        self.dataWindow.showGrid(x=True, y=True)
        self.dataWindow.setHidden(False)
        self.plotX = []
        self.plotY = []
        self.chartData1 = self.dataWindow.plot(self.plotX, self.plotY, pen=self.pen[0])
        self.chartData2 = self.dataWindow.plot(self.plotX, self.plotY, pen=self.pen[2])

        self.dataWindowT = PlotWidget(self)
        # self.dataWindowT.setYRange(self.yScaleNeg,self.yScalePos,padding = 0)
        # self.dataWindow.setBackground('w')
        self.dataWindowT.setBackground([255,255,255])
        self.dataWindowT.setGeometry(5,450,990,250 - self.reduceSize)
        self.dataWindowT.showGrid(x=True, y=True)
        self.dataWindowT.setHidden(True)
        self.plotX = []
        self.plotY = []
        self.chartDataT = self.dataWindowT.plot(self.plotX, self.plotY, pen=self.pen[0])

        self.dataWindowB = PlotWidget(self)
        # self.dataWindowB.setYRange(self.yScaleNeg,self.yScalePos,padding = 0)
        # self.dataWindow.setBackground('w')
        self.dataWindowB.setBackground([255,255,255])
        self.dataWindowB.setGeometry(5,700,990,250 - self.reduceSize)
        self.dataWindowB.showGrid(x=True, y=True)
        self.dataWindowB.setHidden(True)
        self.plotX = []
        self.plotY = []
        self.chartDataB = self.dataWindowB.plot(self.plotX, self.plotY, pen=self.pen[0])



        xStart = 50
        yStart = 900 - self.reduceSize
        self.check_plotDrops = QCheckBox('Show Drops', self)
        self.check_plotDrops.setToolTip('Plot Dropped Packets')
        self.check_plotDrops.setFont(self.guiFont.guiFont14)
        self.check_plotDrops.move(xStart,yStart)
        self.check_plotDrops.resize(200,40)
        if self.appSettings['showDrops'] == 0:
            self.check_plotDrops.setChecked(False)
        else:
            self.check_plotDrops.setChecked(True)
        self.check_plotDrops.stateChanged.connect(self.updatePlotDrops)

        xStart = 10
        yStart = 955 - self.reduceSize
        xBias = 0
        yBias = 0
        xBump = 140
        yBump = 50
        xWidth = 130
        yWidth = 40
        x = 0
        y = 0
        self.but_networkWindow = QPushButton('Networking', self)
        self.but_networkWindow.setToolTip('Show Networking Window')
        self.but_networkWindow.resize(xWidth, yWidth)
        self.but_networkWindow.setStyleSheet(self.buttonSheetBlue)
        self.but_networkWindow.setFont(self.guiFont.guiFont14)
        self.but_networkWindow.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_networkWindow.clicked.connect(self.networkWindow)

        x = 1
        y = 0
        self.but_rangeWindow = QPushButton('Range Window', self)
        self.but_rangeWindow.setToolTip('Show Large Range Window')
        self.but_rangeWindow.resize(xWidth, yWidth)
        self.but_rangeWindow.setStyleSheet(self.buttonSheetBlue)
        self.but_rangeWindow.setFont(self.guiFont.guiFont14)
        self.but_rangeWindow.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_rangeWindow.clicked.connect(self.rangeWindowLarge)

        xWidth = 80
        x = 2
        y = 0
        self.but_LoggingWindow = QPushButton('Logging', self)
        self.but_LoggingWindow.setToolTip('Show Data Logging Parameters')
        self.but_LoggingWindow.resize(xWidth, yWidth)
        self.but_LoggingWindow.setStyleSheet(self.buttonSheetBlue)
        self.but_LoggingWindow.setFont(self.guiFont.guiFont14)
        self.but_LoggingWindow.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_LoggingWindow.clicked.connect(self.openLoggingWindow)
        xBump = 123
        xWidth = 60
        x = 3
        y = 0
        self.but_dataWindow = QPushButton('Data', self)
        self.but_dataWindow.setToolTip('Open Data Transfer Window')
        self.but_dataWindow.resize(xWidth, yWidth)
        self.but_dataWindow.setStyleSheet(self.buttonSheetBlue)
        self.but_dataWindow.setFont(self.guiFont.guiFont14)
        self.but_dataWindow.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_dataWindow.clicked.connect(self.openDataTransferWindow)

        xStart = 450
        yStart = 955 - self.reduceSize
        xBias = 0
        yBias = 0
        xBump = 110
        yBump = 50
        xWidth = 100
        yWidth = 40
        x = 0
        y = 0
        self.but_rangeData = QPushButton('Range Data', self)
        self.but_rangeData.setToolTip('Show Ranging Data')
        self.but_rangeData.resize(xWidth, yWidth)
        self.but_rangeData.setStyleSheet(self.buttonSheetBlue)
        self.but_rangeData.setFont(self.guiFont.guiFont14)
        self.but_rangeData.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_rangeData.clicked.connect(self.openRangeData)

        x = 1
        y = 0
        self.but_reqStats = QPushButton('Req Stats', self)
        self.but_reqStats.setToolTip('Show Requester Stats')
        self.but_reqStats.resize(xWidth, yWidth)
        self.but_reqStats.setStyleSheet(self.buttonSheetBlue)
        self.but_reqStats.setFont(self.guiFont.guiFont14)
        self.but_reqStats.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        # self.but_reqStats.clicked.connect(self.ranging.getReqStats)
        self.but_reqStats.clicked.connect(self.openReqStats)

        x = 2
        y = 0
        self.but_respStats = QPushButton('Resp Stats', self)
        self.but_respStats.setToolTip('Show Responder Stats')
        self.but_respStats.resize(xWidth, yWidth)
        self.but_respStats.setStyleSheet(self.buttonSheetBlue)
        self.but_respStats.setFont(self.guiFont.guiFont14)
        self.but_respStats.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        # self.but_reqStats.clicked.connect(self.ranging.getRespStats)
        self.but_respStats.clicked.connect(self.openRespStats)

        x = 3
        y = 0
        self.but_reqRadioInfo = QPushButton('Req Info', self)
        self.but_reqRadioInfo.setToolTip('Show Radio Information')
        self.but_reqRadioInfo.resize(xWidth, yWidth)
        self.but_reqRadioInfo.setStyleSheet(self.buttonSheetBlue)
        self.but_reqRadioInfo.setFont(self.guiFont.guiFont14)
        self.but_reqRadioInfo.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_reqRadioInfo.clicked.connect(self.getReqRadioInfo)

        x = 4
        y = 0
        self.but_respRadioInfo = QPushButton('Resp Info', self)
        self.but_respRadioInfo.setToolTip('Show Radio Information')
        self.but_respRadioInfo.resize(xWidth, yWidth)
        self.but_respRadioInfo.setStyleSheet(self.buttonSheetBlue)
        self.but_respRadioInfo.setFont(self.guiFont.guiFont14)
        self.but_respRadioInfo.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_respRadioInfo.clicked.connect(self.getRespRadioInfo)
# tests to see if reqeusted range number is valid and updates variables and GUI
    def updateRunTotal(self):
        try:
            self.appSettings['rangeRequests'] = int(self.dispRangeRunTotal.text())
        except:
            text = "  == Range Request Entry Invalid. (Minumum Value = 1. Using Default ==\n"
            self.updateConsole(text)
            self.dispRangeRunTotal.setText("100")
        if int(self.dispRangeRunTotal.text()) < 1:
            text = "  == Range Request Entry Invalid. (Minumum Value = 1. Using Default ==\n"
            self.updateConsole(text)
            self.dispRangeRunTotal.setText("100")
        self.appSettings['rangeRequests'] = int(self.dispRangeRunTotal.text())
# tests to see if range rate number is valid and updates variables and GUI
    def updateRangeRate(self):
        try:
            self.appSettings['rangeRate'] = int(self.dispRangeRate.text())
        except:
            text = "  == Range Delay Entry Invalid. Min: 0   Max: 10,000   Default: 5 ==\n"
            # text = "  == Range Rate Entry Invalid. (0.001Hz to 350Hz. Using Default 200Hz ==\n"
            self.updateConsole(text)
            self.dispRangeRate.setText("5")
        if int(self.dispRangeRate.text()) > 10000 or float(self.dispGuiUpdateRate.text()) < 0:
            text = "  == Range Delay Entry Invalid. Min: 0   Max: 10,000   Default: 5 ==\n"
            self.updateConsole(text)
            self.dispRangeRate.setText("5")
        self.appSettings['rangeRate'] = self.dispRangeRate.text()
        rangeRate = 1 + int(self.dispRangeRate.text())
        self.radioRanging.rangeTimer.stop()
        self.radioRanging.rangeTimer.setInterval(rangeRate)
        # rangeRate = int(1000*(1/(int(self.dispRangeRate.text()))))
        # self.radioRanging.rangeTimer.setInterval(rangeRate)
# tests to see if range delay number is valid and updates variables and GUI
    def updateGuiUpdateRate(self):
        try:
            self.appSettings['guiUpdateRate'] = int(self.dispGuiUpdateRate.text())
        except:
            text = "  == GUI Update Rate Entry Invalid. (1Hz to 100Hz. Using Default 10Hz ==\n"
            self.updateConsole(text)
            self.dispGuiUpdateRate.setText("10")
        if int(self.dispGuiUpdateRate.text()) > 100 or int(self.dispGuiUpdateRate.text()) < 1:
            text = "  == GUI Update Rate Entry Invalid. (1Hz to 100Hz. Using Default 10Hz ==\n"
            self.updateConsole(text)
            self.dispGuiUpdateRate.setText("10")
        self.appSettings['guiUpdateRate'] = self.dispGuiUpdateRate.text()
        updateTime = int(1000*(1/(int(self.dispGuiUpdateRate.text()))))
        self.guiUpdateTimer.setInterval(updateTime)
        self.guiUpdateTimer.stop()
        self.guiUpdateTimer.start()
# tests to see if new requester IP number is valid and updates variables and GUI
    def updateReqRadio(self):
        if self.radioScanComplete == True:
            radioSelection = self.dropMenuReqRadio.currentText()
            testPass = 1
            if radioSelection == self.dropMenuRespRadio.currentText():
                self.dropMenuRespRadio.setCurrentIndex(0)
            if self.connectedRequester == 1:
                self.radioReq.disconnect()
                self.windowDataTransfer.radioData.reqMsgTimer.stop()
            self.connectedRequester = 0
            self.radioReq = None
            self.appSettings['reqRadio'] = radioSelection
            if testPass == 1:
                self.radioConnectReq()
# tests to see if new responder IP number is valid and updates variables and GUI
    def updateRespRadio(self):
        if self.radioScanComplete:
            radioSelection = self.dropMenuRespRadio.currentText()
            testPass = 1
            if radioSelection == self.dropMenuReqRadio.currentText():
                self.dropMenuReqRadio.setCurrentIndex(0)
            if self.connectedResponder == 1:
                self.radioResp.disconnect()
            self.connectedResponder = 0
            self.radioResp = None
            self.appSettings['respRadio'] = radioSelection
            self.connectedResponder = 0
            if testPass == 1:
                self.radioConnectResp()
# tests to see if new responder ID number is valid and updates variables and GUI, comes from responder connection.
    def updateRespID(self, nodeId):
        self.dispRespID.setText(str(nodeId))
        self.appSettings['respID'] = (self.dispRespID.text())
        if self.dispReqID.text() != "-":
            if self.dispReqID.text() == self.dispRespID.text():
                text = "  == ERROR, reqester and responder must have different nodeIDs ==\n"
                self.updateConsole(text)
                self.dispRespID.setStyleSheet("QLineEdit {background-color: red;}")
            else:
                self.dispRespID.setStyleSheet("QLineEdit {background-color: lightgreen;}")
# tests to see if new responder ID number is valid and updates variables and GUI. Comes from GUI update
    def setRespID(self):
        self.appSettings['respID'] = (self.dispRespID.text())
        if self.dispReqID.text() != "-":
            if self.dispReqID.text() == self.dispRespID.text():
                text = "  == ERROR, reqester and responder must have different nodeIDs ==\n"
                self.updateConsole(text)
                self.dispRespID.setStyleSheet("QLineEdit {background-color: red;}")
            else:
                self.dispRespID.setStyleSheet("QLineEdit {background-color: lightgreen;}")
# Reponds to changes in the charting data selected
    def updateDropMenuChart(self):
        if self.dropMenuChart.currentText() == "Ranges" or self.dropMenuChart.currentText() == "Filtered" or self.dropMenuChart.currentText() == "Both":
            self.dataWindow.setHidden(False)
            self.dataWindowT.setHidden(True)
            self.dataWindowB.setHidden(True)
            self.checkChartRange(None)
            # self.chartScale([self.rangeMax, self.rangeMin],[self.powerMax, self.powerMin])
        if self.dropMenuChart.currentText() == "RxPower":
            self.dataWindow.setHidden(False)
            self.dataWindowT.setHidden(True)
            self.dataWindowB.setHidden(True)
            self.checkChartRange(None)
            # self.chartScale([self.powerMax, self.powerMin],[self.powerMax, self.powerMin])
        if self.dropMenuChart.currentText() == "MaxNoise":
            self.dataWindow.setHidden(False)
            self.dataWindowT.setHidden(True)
            self.dataWindowB.setHidden(True)
            self.checkChartRange(None)
            # self.chartScale([self.maxNoiseMax, self.maxNoiseMin],[self.powerMax, self.powerMin])
        if self.dropMenuChart.currentText() == "StdNoise":
            self.dataWindow.setHidden(False)
            self.dataWindowT.setHidden(True)
            self.dataWindowB.setHidden(True)
            self.checkChartRange(None)
            # self.chartScale([self.stdNoiseMax, self.stdNoiseMin],[self.powerMax, self.powerMin])
        if "Multi" in self.dropMenuChart.currentText():
            self.dataWindow.setHidden(True)
            self.dataWindowT.setHidden(False)
            self.dataWindowB.setHidden(False)
            self.checkChartRange(None)
            # self.chartScale([self.rangeMax, self.rangeMin],[self.powerMax, self.powerMin])
        self.dataWindow.enableAutoRange(axis = 'x', enable = True)
        self.dataWindowT.enableAutoRange(axis = 'x', enable = True)
        self.dataWindowB.enableAutoRange(axis = 'x', enable = True)
        filterList = {"Filtered", "Both", "MultiFilt"}
        if self.dropMenuChart.currentText() in filterList:
            self.rangeDispType = "filtered"
        else:
            self.rangeDispType = "precision"
        self.plotData()

# tests to see if new chart depth number is valid and updates variables and GUI. Otherwise uses default.
    def updateChartStore(self):
        try:
            self.appSettings['chartDepth'] = int(self.dispChartStore.text())
        except:
            text = "  == Chart Depth Entry Invalid. (Minumum Value = 50. Using Default ==\n"
            self.updateConsole(text)
            self.dispChartStore.setText("5000")
        if int(self.dispChartStore.text()) < 50:
            text = "  == Chart Depth Entry Invalid. (Minumum Value = 50. Using Default ==\n"
            self.updateConsole(text)
            self.dispChartStore.setText("5000")
        self.appSettings['chartDepth'] = self.dispChartStore.text()
        self.plotData()
# tests to see if new memory depth number is valid and updates variables and GUI. Otherwise uses default.
    def updateMemoryDepth(self):
        try:
            self.appSettings['memoryDepth'] = int(self.dispMemoryDepth.text())
        except:
            text = "  == Memory Depth Entry Invalid. (Minumum Value = 50. Using Default ==\n"
            self.updateConsole(text)
            self.dispMemoryDepth.setText("250000")
        if int(self.dispMemoryDepth.text()) < 50:
            text = "  == Memory Depth Entry Invalid. (Minumum Value = 50. Using Default ==\n"
            self.updateConsole(text)
            self.dispMemoryDepth.setText("250000")
        self.appSettings['memoryDepth'] = self.dispMemoryDepth.text()
# Updates settings when change is made to plotDrops checkbox.
    def updatePlotDrops(self):
        if self.check_plotDrops.isChecked():
            self.appSettings['showDrops'] = 1
            self.plotData()
        else:
            self.appSettings['showDrops'] = 0
            self.plotData()
# Opens network panel for setup up slot maps and showing network data
    def networkWindow(self):
        if self.windowNetwork == None:
            self.windowNetwork = windowNetwork(self)
        if self.windowNetwork.isVisible():
            self.windowNetwork.raise_()
        else:
            self.windowNetwork.displayWindow()

# Opens a larger independent ranging window that's easier to see from a distance.
    def rangeWindowLarge(self):
        if self.windowRangeLarge == None:
            self.windowRangeLarge = windowRangeLarge(self)
        if self.windowRangeLarge.isVisible():
            self.windowRangeLarge.raise_()
        else:
            self.windowRangeLarge.displayWindow()
        self.windowRangeLarge.processData(self.dispRange.text(),255)
# Opens data logging settings window.
    def openLoggingWindow(self):
        data = "-"
        if self.windowLogging == None:
            self.windowLogging = windowLogFile(self)
        if self.windowLogging.isVisible():
            self.windowLogging.raise_()
        else:
            self.windowLogging.displayWindow()
# Opens data logging settings window.
    def openDataTransferWindow(self):
        data = "-"
        if self.windowDataTransfer == None:
            self.windowDataTransfer = windowDataTransfer(self)
        if self.windowDataTransfer.isVisible():
            self.windowDataTransfer.raise_()
        else:
            self.windowDataTransfer.displayWindow()
# Opens window to display data from large range message.
    def openRangeData(self):
        if self.windowRangeData == None:
            self.windowRangeData = windowRangeData(self)
        if self.windowRangeData.isVisible():
            self.windowRangeData.raise_()
        else:
            self.windowRangeData.displayWindow()
# Opens window to display requester statistics.
    def openReqStats(self):
        if self.windowReqStats == None:
            self.windowReqStats = windowChipStats(self, "Requester Stats")
        if self.windowReqStats.isVisible():
            self.windowReqStats.raise_()
        else:
            self.windowReqStats.displayWindow()
            self.statsTimer.start()
# Updates the requester stats window
    def updateReqStats(self, packet):
        self.windowReqStats.processData(packet)
# Opens window to display responder statistics.
    def openRespStats(self):
        if self.connectedResponder == 1:
            if self.windowRespStats == None:
                self.windowRespStats = windowChipStats(self, "Responder Stats")
            if self.windowRespStats.isVisible():
                self.windowRespStats.raise_()
            else:
                self.windowRespStats.displayWindow()
                self.statsTimer.start()
# Updates the responder stats window
    def updateRespStats(self, packet):
        if self.connectedResponder == 1:
            self.windowRespStats.processData(packet)
# Opens / Updates window to show general requester radio information
    def showReqRadioInfo(self, packet):
        if self.windowReqRadioInfo == None:
            self.windowReqRadioInfo = windowRadioInfo(self, packet, "Requester Info")
        if self.windowReqRadioInfo.isVisible():
            self.windowReqRadioInfo.raise_()
        else:
            self.windowReqRadioInfo.displayWindow()
        self.windowReqRadioInfo.processData(packet)
# Opens / Updates window to show general responder radio information
    def showRespRadioInfo(self, packet):
        if self.connectedResponder == 1:
            if self.windowRespRadioInfo == None:
                self.windowRespRadioInfo = windowRadioInfo(self, packet, "Responder Info")
            if self.windowRespRadioInfo.isVisible():
                self.windowRespRadioInfo.raise_()
            else:
                self.windowRespRadioInfo.displayWindow()
            self.windowRespRadioInfo.processData(packet)
# Updates stats for whatever windows are detected to be open
    def updateStats(self):
        if self.windowReqStats.isVisible():
            self.getReqStats()
        if self.windowRespStats.isVisible():
            self.getRespStats()
        if (not self.windowRespStats.isVisible()) and (not self.windowReqStats.isVisible()):
            self.statsTimer.stop()
# Updates GUI connection status of requester
    def updateConnectReq(self, status):
        if status == False:
            self.dropMenuReqRadio.setStyleSheet("QComboBox {background-color: red;}")
            self.but_RadioConfigReq.setStyleSheet("QPushButton {background-color: red;}")
            text = "== Could not connect to primary radio address " + self.appSettings['reqRadio'] + " ==\n"
            self.updateConsole(text)
        else:
            self.dropMenuReqRadio.setStyleSheet("QComboBox {background-color: lightgreen;}")
            self.but_RadioConfigReq.setStyleSheet(self.buttonSheetBlue)
            self.dispReqID.setText(str(self.radioReqNodeID))
            text = "Connected to Primary Radio Address " + self.appSettings['reqRadio'] + "\n"
            self.updateConsole(text)
# Updates GUI connection status of responder
    def updateConnectResp(self, status):
        if status == False:
            # self.connectedResponder = 0
            self.dropMenuRespRadio.setStyleSheet("QComboBox {background-color: red;}")
            self.but_RadioConfigResp.setStyleSheet("QPushButton {background-color: red;}")
            self.but_respRadioInfo.setStyleSheet("QPushButton {background-color: red;}")
            self.but_respStats.setStyleSheet("QPushButton {background-color: red;}")
            if self.appSettings['connectResp'] == 1:
                text = "== Could not connect to secondary radio address " + self.appSettings['respRadio'] + " ==\n"
                self.updateConsole(text)
            else:
                # self.connectedResponder = 0
                text = "Connected responder not selected\n"
                self.updateConsole(text)
        else:
            # self.connectedResponder = 1
            self.dropMenuRespRadio.setStyleSheet("QComboBox {background-color: lightgreen;}")
            self.but_RadioConfigResp.setStyleSheet(self.buttonSheetBlue)
            self.but_respRadioInfo.setStyleSheet(self.buttonSheetBlue)
            self.but_respStats.setStyleSheet(self.buttonSheetBlue)
            text = "Connected to Secondary Radio Address " + self.appSettings['respRadio'] + "\n"
            self.updateConsole(text)
        self.windowDataTransfer.updateRespAvailable()
# Updates text in GUI console output.
    def updateConsole(self, text):
        self.consoleBuf = self.consoleBuf + text
        self.consoleOutput.setText(self.consoleBuf)
        self.consoleOutputScrollBar.setValue(self.consoleOutputScrollBar.maximum())
    def updateChipTemp(self):
        if self.connectedRequester == 1:
            tmp = self.getReqRadioChipTemp()
            self.dispChipTemp.setText(str(tmp))

# App close signal triggers closing of any open gui windows.
    def closeEvent(self, event):
        self.radioCheckTimer.stop()
        self.radioRanging.networkTimer.stop()
        self.appSettings['savePosition'] = str(self.x()) + "," + str(self.y())
        self.radioRanging.closeApp()
        print("\nRanging Halted, Ranging App Closed.\n")
        self.chipTempTimer.stop()
        if self.windowReqStats.isVisible():
            self.windowReqStats.close()
        self.windowReqStats = None
        if self.windowRespStats.isVisible():
            self.windowRespStats.close()
        self.windowRespStats = None
        if self.windowRangeData.isVisible():
            self.windowRangeData.close()
        self.windowRangeData = None
        if self.windowReqRadioInfo.isVisible():
            self.windowReqRadioInfo.close()
        self.windowReqRadioInfo = None
        if self.windowRespRadioInfo.isVisible():
            self.windowRespRadioInfo.close()
        self.windowRespRadioInfo = None
        if self.windowRangeLarge.isVisible():
            self.windowRangeLarge.close()
        self.windowRangeLarge = None
        if self.windowNetwork.isVisible():
            self.windowNetwork.close()
        self.windowNetwork = None
        if self.windowLogging.isVisible():
            self.windowLogging.close()
        self.windowLogging = None
        if self.windowDataTransfer.isVisible():
            self.windowDataTransfer.close()
        self.windowDataTransfer = None
        if self.windowConfigReq.isVisible():
            self.windowConfigReq.close()
        self.windowConfigReq = None
        if self.windowConfigResp.isVisible():
            self.windowConfigResp.close()
        self.windowConfigResp = None
        if self.windowChipTuning.isVisible():
            self.windowChipTuning.close()
        self.windowChipTuning = None
        self.settings.settingsSave()
        self.logFile.closeLogFile()
        if self.connectedRequester == 1:
            self.radioReq.disconnect()
        if self.connectedResponder == 1:
            self.radioResp.disconnect()
        if self.connectedMultiCast == 1:
            self.radioMultiCast.disconnect()

# Closes down any open windows when app close signal comes.
    def closeItDown(self):
        print("Have a good day!")

    def initWindows(self):
        self.guiFont = guiFonts()
        self.windowConfigReq = windowConfiguration(self, 1)   # Need these here for GUI info
        self.windowConfigResp = windowConfiguration(self, 0)
        self.windowReqStats =  windowChipStats(self, "Requester Stats")
        self.windowRespStats = windowChipStats(self, "Responder Stats")
        self.windowRangeData = windowRangeData(self)
        self.windowReqRadioInfo = windowRadioInfo(self, "Requester Info", 1)
        self.windowRespRadioInfo = windowRadioInfo(self, "Responder Info", 0)
        self.windowRangeLarge = windowRangeLarge(self)
        self.windowNetwork = windowNetwork(self)
        self.windowLogging = windowLogFile(self)
        self.windowDataTransfer = windowDataTransfer(self)
        self.windowChipTuning = windowChipTuning(self)

    def positionWindows(self):
        xOffset = self.x() + self.mainWindowWidth + 5
        yOffset = self.y()
        self.windowDataTransfer.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowConfigReq.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowConfigResp.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowReqStats.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowRespStats.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowRangeData.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowReqRadioInfo.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowRespRadioInfo.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowRangeLarge.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowNetwork.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowLogging.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowDataTransfer.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)
        self.windowChipTuning.move(self.monitor.left()+xOffset, self.monitor.top()+yOffset)

    def definePens(self):
        self.pen = []
        self.pen.append(mkPen(width = 4, color=(255,0,0)))
        self.pen.append(mkPen(width = 4, color=(0,255,0)))
        self.pen.append(mkPen(width = 4, color=(0,0,255)))
        self.pen.append(mkPen(width = 4, color=(127,127,0)))
        self.pen.append(mkPen(width = 4, color=(0,255,255)))
        self.pen.append(mkPen(width = 4, color=(255,0,255)))
        self.pen.append(mkPen(width = 4, color=(127,0,0)))
        self.pen.append(mkPen(width = 4, color=(0,127,0)))
        self.pen.append(mkPen(width = 4, color=(0,0,127)))
        self.pen.append(mkPen(width = 4, color=(63,63,0)))
        self.pen.append(mkPen(width = 4, color=(0,127,127)))
        self.pen.append(mkPen(width = 4, color=(127,0,127)))
        self.pen.append(mkPen(width = 4, color=(63,0,0)))
        self.pen.append(mkPen(width = 4, color=(0,63,0)))
        self.pen.append(mkPen(width = 4, color=(0,0,63)))
        self.pen.append(mkPen(width = 4, color=(31,31,0)))
        self.pen.append(mkPen(width = 4, color=(0,63,63)))
        self.pen.append(mkPen(width = 4, color=(63,0,63)))
        self.pen.append(mkPen(width = 4, color=(0,0,0)))

    def defineSheets(self):
        self.buttonSheetBlue = "QPushButton {background-color: rgb(0,60,100); color: GhostWhite;}"
        self.buttonSheetGray = "QPushButton {background-color: lightgrey; color: black;}"
        self.dropSheetBlue = "QComboBox {color: GhostWhite; background-color: rgb(0,60,100);} QAbstractItemView {color: GhostWhite; background-color: DarkBlue;}"
        self.dropSheetGray = "QComboBox {color: black; background-color: lightgrey;} QAbstractItemView {color: black; background-color: GhostWhite;}"
        self.lineSheet = "QLineEdit {background-color: rgb(240,240,240);}"
        self.lineSheetYellow = "QLineEdit {color: black; background-color: lightyellow;}"
        self.windowSheet = "QWidget {background-color: rgb(100,160,220);}"
        self.mainWindowSheet = "QMainWindow {background-color: rgb(100,160,220);}"
        self.checkBoxSheet = "QCheckBox {color: GhostWhite;} QCheckBox::indicator {width:20px; height:20px;}"

# Class window to display long running radio statistics
class windowChipStats(QWidget):
    def __init__(self, gui, name):
        super().__init__()
        # self.setGeometry(10, 10, 800, 480)
        self.setFixedSize(800,480)
        self.setWindowTitle(name)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.name = name
        self.guiFont = guiFonts()
        self.initChipStatsGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        if self.name == "Requester Stats":
            self.gui.windowReqStats.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
        else:
            self.gui.windowRespStats.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def processData(self, stats):
        tmp = self.name + ":"
        for k in range(len(self.chipStatFields)):
            self.dispChipStatWindow[k].setText(str(stats['RADIO_GET_STATS_CONFIRM'][self.chipStatKeys[k]]))

    def initChipStatsGUI(self):
        xStart = 225
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 350
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText(self.name)

        self.chipStatFields =  ['Pckts-TX', 'Pkts-RX', 'Rng_RequestsRX', 'Num 2nd ReqRx', 'Num 3rd ReqRx',
                            'Num RX Resp', 'Num TX Req', 'Num 2nd ReqTx', 'Num 3rd ReqTx',
                            'Rng_Successes', 'PHE', 'RSL', 'CRCG', 'CRCB', 'ARFE', 'OVER', 'SFDTO', 'PTO',
                            'RTO', 'TXF', 'HPW', 'TXW', 'TX-Errors', 'RX-IdleError']
        self.chipStatKeys = ['numPacketsTransmitted', 'numPacketsReceived', 'numRangeRequestsRx',  'numRangeReq2Rx', 'numRangeReq3Rx',
                            'numRangeResponsesRx', 'numRangeRequestsTx', 'numRangeReq2Tx', 'numRangeReq3Tx',
                            'numRangeRequestsComplete', 'PHE', 'RSL', 'CRCG', 'CRCB', 'ARFE', 'OVER', 'SFDTO', 'PTO',
                            'RTO', 'TXF', 'HPW', 'TXW', 'txErrors', 'receiverIdleError']
        self.chipStatTips = ['Packets Transmitted', ' Packets Received', 'Range Requests', 'Range2 RequestsRX', 'Range3 RequestsRX',
                                'Range ResponsesRX', 'Range ResponsesTX', 'Range2 RequestsTX', 'Range3 RequestsTX',
                                'Successful Ranges', 'Phy Header Errors', 'FEC Sync Loss', 'FrameCheck(CRC) Good', 'FrameCheck(CRC) Bad', 'Frame Filter Rejections',
                                'OverRun Error Count', 'Start of Frame Delimiter', 'PreAmble Detection Timeout', 'Receive Frame Wait Timeout', 'TX Frame Success',
                                'Half Period Warning Counter', 'TX TurnOn Time Warning', 'Transmit Timing Errors', 'Receive Idle Error']
        self.labelChipStatWindow = []
        self.dispChipStatWindow = []

        xStart = 10
        yStart = 70
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 140
        yWidth = 40
        x = 0
        y = 0
        for k in range(len(self.chipStatFields)):
            if x > 4:
                y = y + 1
                x = 0
            tmpL = QLabel(self)
            tmpL.resize(xWidth,yWidth)
            tmpL.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias)
            tmpL.setFont(self.guiFont.guiFont14)
            tmpL.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpL.setText(self.chipStatFields[k])
            tmpL.setToolTip(self.chipStatTips[k])
            tmpD = QLineEdit(self)
            tmpD.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
            tmpD.resize(xWidth,yWidth)
            tmpD.setToolTip(self.chipStatTips[k])
            tmpD.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpD.setStyleSheet("QLineEdit {background-color: lightyellow;}")
            tmpD.setFont(self.guiFont.guiFont18)
            tmpD.setText("-")
            self.labelChipStatWindow.append(tmpL)
            self.dispChipStatWindow.append(tmpD)
            x = x + 1

class windowChipTuning(QWidget):
    def __init__(self, gui):
        super().__init__()
        self.setFixedSize(640,330)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.name = "Chip Tuning"
        self.setWindowTitle(self.name)
        self.guiFont = guiFonts()
        self.initGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowChipTuning.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
        self.radioGetTuning()

    def initGUI(self):
        xStart = 145
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 350
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText(self.name)

        xStart = 90
        yStart = 100
        xBias = 0
        yBias = 0
        xBump = 120
        yBump = 80
        xWidth = 300
        yWidth = 40
        x = 0
        y = 0
        self.labelTXPower = QLabel(self)
        self.labelTXPower.resize(xWidth,yWidth)
        self.labelTXPower.move(170,65)
        self.labelTXPower.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXPower.setFont(self.guiFont.guiFont20)
        self.labelTXPower.setText("TXPower Control")
        xWidth = 100
        y = 0
        self.labelTXPower3 = QLabel(self)
        self.labelTXPower3.resize(xWidth,yWidth)
        self.labelTXPower3.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTXPower3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXPower3.setFont(self.guiFont.guiFont20)
        self.labelTXPower3.setText("Byte3")
        self.dispTXPower3 = QLineEdit(self)
        self.dispTXPower3.setFont(self.guiFont.guiFont20)
        self.dispTXPower3.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTXPower3.resize(xWidth,yWidth)
        self.dispTXPower3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTXPower3.setText("-")
        self.dispTXPower3.editingFinished.connect(self.radioUpdateTuning)
        x = 1
        self.labelTXPower2 = QLabel(self)
        self.labelTXPower2.resize(xWidth,yWidth)
        self.labelTXPower2.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTXPower2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXPower2.setFont(self.guiFont.guiFont20)
        self.labelTXPower2.setText("Byte2")
        self.dispTXPower2 = QLineEdit(self)
        self.dispTXPower2.setFont(self.guiFont.guiFont20)
        self.dispTXPower2.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTXPower2.resize(xWidth,yWidth)
        self.dispTXPower2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTXPower2.setText("-")
        self.dispTXPower2.editingFinished.connect(self.radioUpdateTuning)
        x = 2
        self.labelTXPower1 = QLabel(self)
        self.labelTXPower1.resize(xWidth,yWidth)
        self.labelTXPower1.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTXPower1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXPower1.setFont(self.guiFont.guiFont20)
        self.labelTXPower1.setText("Byte1")
        self.dispTXPower1 = QLineEdit(self)
        self.dispTXPower1.setFont(self.guiFont.guiFont20)
        self.dispTXPower1.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTXPower1.resize(xWidth,yWidth)
        self.dispTXPower1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTXPower1.setText("-")
        self.dispTXPower1.editingFinished.connect(self.radioUpdateTuning)
        x = 3
        self.labelTXPower0 = QLabel(self)
        self.labelTXPower0.resize(xWidth,yWidth)
        self.labelTXPower0.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTXPower0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXPower0.setFont(self.guiFont.guiFont20)
        self.labelTXPower0.setText("Byte0")
        self.dispTXPower0 = QLineEdit(self)
        self.dispTXPower0.setFont(self.guiFont.guiFont20)
        self.dispTXPower0.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTXPower0.resize(xWidth,yWidth)
        self.dispTXPower0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTXPower0.setText("-")
        self.dispTXPower0.editingFinished.connect(self.radioUpdateTuning)
        y = 1
        x = 0
        self.labelPGTarget = QLabel(self)
        self.labelPGTarget.resize(xWidth+10,yWidth)
        self.labelPGTarget.move(x*xBump + xStart + xBias - 5, yStart + y*yBump + yBias)
        self.labelPGTarget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelPGTarget.setFont(self.guiFont.guiFont20)
        self.labelPGTarget.setText("PG Target")
        self.dispPGTarget = QLineEdit(self)
        self.dispPGTarget.setFont(self.guiFont.guiFont20)
        self.dispPGTarget.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispPGTarget.resize(xWidth,yWidth)
        self.dispPGTarget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispPGTarget.setText("-")
        self.dispPGTarget.editingFinished.connect(self.radioUpdateTuning)
        y = 1
        x = 1
        self.labelPGDelay = QLabel(self)
        self.labelPGDelay.resize(xWidth,yWidth)
        self.labelPGDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelPGDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelPGDelay.setFont(self.guiFont.guiFont20)
        self.labelPGDelay.setText("PG Delay")
        self.dispPGDelay = QLineEdit(self)
        self.dispPGDelay.setFont(self.guiFont.guiFont20)
        self.dispPGDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispPGDelay.resize(xWidth,yWidth)
        self.dispPGDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispPGDelay.setText("-")
        self.dispPGDelay.editingFinished.connect(self.radioUpdateTuning)
        x = 2
        self.labelRXDelay = QLabel(self)
        self.labelRXDelay.resize(xWidth,yWidth)
        self.labelRXDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelRXDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRXDelay.setFont(self.guiFont.guiFont20)
        self.labelRXDelay.setText("RX Delay")
        self.dispRXDelay = QLineEdit(self)
        self.dispRXDelay.setFont(self.guiFont.guiFont20)
        self.dispRXDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispRXDelay.resize(xWidth,yWidth)
        self.dispRXDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRXDelay.setText("-")
        self.dispRXDelay.editingFinished.connect(self.radioUpdateTuning)
        x = 3
        self.labelTXDelay = QLabel(self)
        self.labelTXDelay.resize(xWidth,yWidth)
        self.labelTXDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTXDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTXDelay.setFont(self.guiFont.guiFont20)
        self.labelTXDelay.setText("TX Delay")
        self.dispTXDelay = QLineEdit(self)
        self.dispTXDelay.setFont(self.guiFont.guiFont20)
        self.dispTXDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTXDelay.resize(xWidth,yWidth)
        self.dispTXDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTXDelay.setText("-")
        self.dispTXDelay.editingFinished.connect(self.radioUpdateTuning)
        yBias = 10
        xBump = 180
        xWidth = 160
        xStart = 60
        x = 0
        y = 2
        self.but_getTuning = QPushButton('Get Config', self)
        self.but_getTuning.setToolTip('Get Radio Tuning Values')
        self.but_getTuning.resize(xWidth, yWidth)
        self.but_getTuning.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_getTuning.setFont(self.guiFont.guiFont14)
        self.but_getTuning.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_getTuning.clicked.connect(self.radioGetTuning)

        x = 1
        self.but_storeTuning = QPushButton('Store in Flash', self)
        self.but_storeTuning.setToolTip('Store Radio Tuning In Flash')
        self.but_storeTuning.resize(xWidth, yWidth)
        self.but_storeTuning.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_storeTuning.setFont(self.guiFont.guiFont14)
        self.but_storeTuning.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_storeTuning.clicked.connect(self.radioStoreTuning)

        x = 2
        self.but_storeLockPreset = QPushButton('Lock in Preset', self)
        self.but_storeLockPreset.setToolTip('Store as locked preset')
        self.but_storeLockPreset.resize(xWidth, yWidth)
        self.but_storeLockPreset.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_storeLockPreset.setFont(self.guiFont.guiFont14)
        self.but_storeLockPreset.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_storeLockPreset.clicked.connect(self.gui.windowConfigReq.radioLockSavePreset)

    def radioStoreTuning(self):
        byte3 = int(self.dispTXPower3.text(), 16)
        byte2 = int(self.dispTXPower2.text(), 16)
        byte1 = int(self.dispTXPower1.text(), 16)
        byte0 = int(self.dispTXPower0.text(), 16)
        pgTarget = int(self.dispPGTarget.text(), 16)
        pgDelay = int(self.dispPGDelay.text(), 16)
        rxDelay = int(self.dispRXDelay.text(), 16)
        txDelay = int(self.dispTXDelay.text(), 16)
        txPower = (byte3 << 24) + (byte2 << 16) + (byte1 << 8) + byte0
        newPacket = {"RADIO_SET_TUNING_REQUEST":{"msgId":0,"TxPwrContrl":txPower,"PGCount_Target":pgTarget,"TC_PGDelay":pgDelay,"RXAntDelay":rxDelay,"TXAntDelay":txDelay,"persistFlag":1}}
        if self.gui.connectedRequester == 1:
            self.gui.radioReq.API.radio_SetTuning_Request(self.gui.appSettings['reqRadio'], newPacket)
            self.but_storeTuning.setStyleSheet("QPushButton {background-color: FireBrick;}")
            self.but_storeTuning.setText("Writing...")
            self.flashTimer = QTimer()
            self.flashTimer.setInterval(500)
            self.flashTimer.timeout.connect(self.updateFlashButton)
            self.flashTimer.start()

    def updateFlashButton(self):
        self.but_storeTuning.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_storeTuning.setText("Store in Flash")
        self.flashTimer.stop()
        self.flashTimer = None

    def radioUpdateTuning(self):
        byte3 = int(self.dispTXPower3.text(), 16)
        byte2 = int(self.dispTXPower2.text(), 16)
        byte1 = int(self.dispTXPower1.text(), 16)
        byte0 = int(self.dispTXPower0.text(), 16)
        pgTarget = int(self.dispPGTarget.text(), 16)
        pgDelay = int(self.dispPGDelay.text(), 16)
        rxDelay = int(self.dispRXDelay.text(), 16)
        txDelay = int(self.dispTXDelay.text(), 16)
        txPower = (byte3 << 24) + (byte2 << 16) + (byte1 << 8) + byte0
        newPacket = {"RADIO_SET_TUNING_REQUEST":{"msgId":0,"TxPwrContrl":txPower,"PGCount_Target":pgTarget,"TC_PGDelay":pgDelay,"RXAntDelay":rxDelay,"TXAntDelay":txDelay,"persistFlag":0}}
        if self.gui.connectedRequester == 1:
            self.gui.radioReq.API.radio_SetTuning_Request(self.gui.appSettings['reqRadio'], newPacket)

    def radioGetTuning(self):
        if self.gui.connectedRequester == 1:
            status,packet,addr = self.gui.radioReq.API.radio_GetTuning_Request(self.gui.appSettings['reqRadio'])
            data = packet['RADIO_GET_TUNING_CONFIRM']
            try:
                pgTarget = data['PGCount_Target']
            except:
                pgTarget = 0
            pgDelay = data['TC_PGDelay']
            rxDelay = data['RXAntDelay']
            txDelay = data['TXAntDelay']
            power = data['TxPwrContrl']
            byte3 = power >> 24
            byte2 = power & 0xff0000
            byte2 = byte2 >> 16
            byte1 = power & 0xff00
            byte1 = byte1 >> 8
            byte0 = power & 0xff
            self.dispTXPower3.setText(hex(byte3))
            self.dispTXPower2.setText(hex(byte2))
            self.dispTXPower1.setText(hex(byte1))
            self.dispTXPower0.setText(hex(byte0))
            self.dispPGTarget.setText(hex(pgTarget))
            self.dispPGDelay.setText(hex(pgDelay))
            self.dispRXDelay.setText(hex(rxDelay))
            self.dispTXDelay.setText(hex(txDelay))

# Class for window to display data from current range message.
class windowRangeData(QWidget):
    def __init__(self, gui):
        super().__init__()
        # self.setGeometry(10, 10, 640, 330)
        self.setFixedSize(640,330)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.name = "Range Data"
        self.setWindowTitle(self.name)
        self.guiFont = guiFonts()
        self.initGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowRangeData.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def processData(self, rangeData):
        tmp = str(rangeData['RANGE_INFO']['rxPower'])
        if tmp == "-Infinity" or tmp == "-inf":
            tmp = "-110.0"
            print("\n-Infinity Found")
            print("rxPower: ", str(rangeData['RANGE_INFO']['rxPower']))
            print("MaxGrowCIR: ", str(rangeData['RANGE_INFO']['maxGrowthCIR']))
            print("rxPreamCount: ", str(rangeData['RANGE_INFO']['rxPreamCount']))
            print("precRange: ", str(rangeData['RANGE_INFO']['precisionRangeM']))
            print("rangeStatus: ", str(rangeData['RANGE_INFO']['rangeStatus']))
        tmp = tmp.split(".")
        tmp = tmp[0] + "." + tmp[1][:1]
        rangeData['RANGE_INFO']['rxPower'] = tmp
        tmp = str(rangeData['RANGE_INFO']['firstPathPower'])
        tmp = tmp.split(".")
        tmp = tmp[0] + "." + tmp[1][:2]
        rangeData['RANGE_INFO']['firstPathPower'] = tmp
        for k in range(len(self.rangeDataFields)):
            self.dispRangeDataWindow[k].setText(str(rangeData['RANGE_INFO'][self.rangeDataKeys[k]]))

    def initGUI(self):
        xStart = 145
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 350
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText(self.name)

        self.rangeDataFields =  ['rxPower', 'maxNoise', 'stdNoise', 'maxGrowthCIR',
                            'rxPreamCount', 'firstPath', '1st_PathPower', 'Resp_1st_PP',
                            'firstPathAmp1', 'firstPathAmp2', 'firstPathAmp3']
        self.rangeDataKeys = ['rxPower', 'maxNoise', 'stdNoise', 'maxGrowthCIR',
                            'rxPreamCount', 'firstPath', 'firstPathPower', 'responderFpp',
                            'firstPathAmp1', 'firstPathAmp2', 'firstPathAmp3']
        self.rangeDataTips = ['RX Power', 'Max Noise', 'Std Noise', 'Max Growth Chan Impulse Response',
                            'rxPreamCount', 'firstPath', 'Requester First Path Power', 'Responder First Path Power',
                            'First Path Amp1', 'First Path Amp2', 'First Path Amp3']
        self.labelRangeDataWindow = []
        self.dispRangeDataWindow = []

        xStart = 10
        yStart = 70
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 140
        yWidth = 40
        x = 0
        y = 0
        for k in range(len(self.rangeDataFields)):
            if x > 3:
                y = y + 1
                x = 0
            tmpL = QLabel(self)
            tmpL.resize(xWidth,yWidth)
            tmpL.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias)
            tmpL.setFont(self.guiFont.guiFont14)
            tmpL.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpL.setText(self.rangeDataFields[k])
            tmpL.setToolTip(self.rangeDataTips[k])
            tmpD = QLineEdit(self)
            tmpD.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
            tmpD.resize(xWidth,yWidth)
            tmpD.setToolTip(self.rangeDataTips[k])
            tmpD.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpD.setStyleSheet("QLineEdit {background-color: lightyellow;}")
            tmpD.setFont(self.guiFont.guiFont18)
            tmpD.setText("-")
            self.labelRangeDataWindow.append(tmpL)
            self.dispRangeDataWindow.append(tmpD)
            x = x + 1

# Class for window to display general radio information
class windowRadioInfo(QWidget):
    def __init__(self, gui, name, req):
        super().__init__()
        # self.setGeometry(10, 10, 780, 500)
        self.setFixedSize(780,500)
        self.setWindowTitle(name)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.name = name
        self.req = req
        self.guiFont = guiFonts()
        self.initGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        if self.req == 1:
            self.gui.windowReqRadioInfo.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
        else:
            self.gui.windowRespRadioInfo.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def processData(self, stats):
        tmp = self.name + ":"
        for k in range(len(self.radioInfoFields)):
            self.dispRadioInfoWindow[k].setText(str(stats['RADIO_GET_INFO_CONFIRM'][self.radioInfoKeys[k]]))

    def initGUI(self):
        xStart = 225
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 350
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText(self.name)

        self.radioInfoFields =  ['Serial #', 'BoardType', 'BarCode', 'Kernel Ver', 'App Ver', 'DW Info']
        self.radioInfoKeys = ['serialNo', 'boardType', 'barCodeString', 'kernelVersion', 'appVersion', 'chipInfo']
        self.labelRadioInfoWindow = []
        self.dispRadioInfoWindow = []

        xStart = 10
        yStart = 70
        xBias = 0
        yBias = 0
        xBump = 400
        yBump = 80
        xWidth = 360
        yWidth = 40
        x = 0
        y = 0
        for k in range(len(self.radioInfoFields)):
            if k < 2:
                if x > 1:
                    y = y + 1
                    x = 0
            else:
                xWidth = 760
                y = y + 1
                x = 0
            tmpL = QLabel(self)
            tmpL.resize(xWidth,yWidth)
            tmpL.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias)
            tmpL.setFont(self.guiFont.guiFont14)
            tmpL.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpL.setText(self.radioInfoFields[k])
            tmpD = QLineEdit(self)
            tmpD.move((x)*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
            tmpD.resize(xWidth,yWidth)
            tmpD.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tmpD.setStyleSheet("QLineEdit {background-color: lightyellow;}")
            tmpD.setFont(self.guiFont.guiFont18)
            tmpD.setText("-")
            self.labelRadioInfoWindow.append(tmpL)
            self.dispRadioInfoWindow.append(tmpD)
            x = x + 1

# Class for window to display, set, and get radio configuration
class windowConfiguration(QWidget):
    def __init__(self, gui, req):
        super().__init__()
        # self.setGeometry(10, 10, 620, 400)
        self.setFixedSize(620,840)
        self.setWindowTitle("Radio Configuration")
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.guiFont = guiFonts()
        self.configFormUpdate = 0
        self.req = req  # 0 = responder, 1 = requester
        if self.req == 1:
            self.radioConfig = self.gui.radioConfigReq
        else:
            self.radioConfig = self.gui.radioConfigResp

    def displayWindow(self):
        if (self.req) and (self.gui.connectedRequester == 1):
            if self.gui.windowConfigReq.isVisible():
                self.raise_()
            else:
                self.initGUI()
                self.show()
                xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
                yOffset = self.gui.y()
                self.gui.windowConfigReq.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
            self.radioGetPresets()
            self.radioUpdateActivePreset()
            self.radioUpdatePresets()
            self.radioGetIP()
        if (not self.req) and (self.gui.connectedResponder == 1):
            if self.gui.windowConfigResp.isVisible():
                self.raise_()
            else:
                self.initGUI()
                self.show()
                xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
                yOffset = self.gui.y()
                self.gui.windowConfigResp.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
            self.radioGetPresets()
            self.radioUpdateActivePreset()
            self.radioUpdatePresets()
            self.radioGetIP()

    def updateNodeID(self):
        if self.configFormUpdate == 1:  # config get = 1. 0 is either set or set and store
            if self.req:
                self.gui.radioReqNodeID, addr = self.gui.radioReq.API.radio_GetNodeID_Request(self.gui.appSettings['reqRadio'])
                self.gui.radioReqNodeID = self.gui.radioReqNodeID['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']
                self.dispNodeID.setText(str(self.gui.radioReqNodeID))
                self.gui.dispReqID.setText(str(self.gui.radioReqNodeID))
            else:
                self.gui.radioRespNodeID, addr = self.gui.radioResp.API.radio_GetNodeID_Request(self.gui.appSettings['respRadio'])
                self.gui.radioRespNodeID = self.gui.radioRespNodeID['RADIO_GET_NODE_CONFIG_CONFIRM']['nodeId']
                self.dispNodeID.setText(str(self.gui.radioRespNodeID))
                self.gui.dispRespID.setText(str(self.gui.radioRespNodeID))
        else:                           # set or set and store branch
            if self.req:
                self.gui.radioReqNodeID = int(self.dispNodeID.text())
                self.gui.dispReqID.setText(str(self.gui.radioReqNodeID))
            else:
                self.gui.radioRespNodeID = int(self.dispNodeID.text())
                self.gui.dispRespID.setText(str(self.gui.radioRespNodeID))
        self.configFormUpdate = 0

    def updateTxPower(self):
        if self.configFormUpdate == 1:
            self.dispTxPower.setText(str(self.radioConfig[list(self.radioConfig.keys())[0]]['power']))
        else:
            self.radioConfig[list(self.radioConfig.keys())[0]]['power'] = int(self.dispTxPower.text())
        self.configFormUpdate = 0

    def updateAntDelay(self):
        if self.configFormUpdate == 1:
            self.dispAntDelay.setText(str(self.radioConfig[list(self.radioConfig.keys())[0]]['antennaDelay']))
        else:
            self.radioConfig[list(self.radioConfig.keys())[0]]['antennaDelay'] = int(self.dispAntDelay.text())
        self.configFormUpdate = 0

    def updateMenuPRF(self):
        option = self.dropMenuPRF.currentText()
        dropMenuOptions = ["16MHz", "64Mhz"]
        settingsOptions = ["DWT_PRF_16M", "DWT_PRF_64M"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['prf'] = settingsOptions[k]
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if settingsOptions[k] in self.radioConfig[list(self.radioConfig.keys())[0]]['prf']:
                    self.dropMenuPRF.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['prf']}")
            self.configFormUpdate = 0

    def updateMenuPreamLen(self):
        option = self.dropMenuPreamLen.currentText()
        dropMenuOptions = ["64", "128", "256", "512", "1024", "1536", "2048", "4096"]
        settingsOptions = ["DWT_PLEN_64", "DWT_PLEN_128", "DWT_PLEN_256", "DWT_PLEN_512", "DWT_PLEN_1024", "DWT_PLEN_1536",
                            "DWT_PLEN_2048", "DWT_PLEN_4096"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['txPreambleLength'] = settingsOptions[k]
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if settingsOptions[k] == self.radioConfig[list(self.radioConfig.keys())[0]]['txPreambleLength']:
                    self.dropMenuPreamLen.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['txPreambleLength']}")
            self.configFormUpdate = 0

    def updateMenuBitRate(self):
        option = self.dropMenuBitRate.currentText()
        dropMenuOptions = ["110Kb", "850Kb", "6.8Mb"]
        settingsOptions = ["DWT_BR_110K", "DWT_BR_850K", "DWT_BR_6M8"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['dataRate'] = settingsOptions[k]
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if settingsOptions[k] == self.radioConfig[list(self.radioConfig.keys())[0]]['dataRate']:
                    self.dropMenuBitRate.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['dataRate']}")
            self.configFormUpdate = 0

    def updateMenuPAC(self):
        option = self.dropMenuPAC.currentText()
        dropMenuOptions = ["8", "16", "32", "64"]
        settingsOptions = ["DWT_PAC8", "DWT_PAC16", "DWT_PAC32", "DWT_PAC64"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['PAC'] = settingsOptions[k]
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if settingsOptions[k] == self.radioConfig[list(self.radioConfig.keys())[0]]['PAC']:
                    self.dropMenuPAC.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['PAC']}")
            self.configFormUpdate = 0

    def updateMenuChannel(self):
        option = self.dropMenuChannel.currentText()
        dropMenuOptions = ["4.0GHz(2)", "4.5GHz(3)", "6.5GHz(5)", "8GHz(9)"]
        settingsOptions = ["2", "3", "5", "9"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['channel'] = int(settingsOptions[k])
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if int(settingsOptions[k]) == self.radioConfig[list(self.radioConfig.keys())[0]]['channel']:
                    self.dropMenuChannel.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['channel']}")
            self.configFormUpdate = 0

    def updateMenuPreamCode(self):
        option = self.dropMenuPreamCode.currentText()
        dropMenuOptions = ["9", "10", "11", "12", "13"]
        settingsOptions = ["9", "10", "11", "12", "13"]
        if self.configFormUpdate == 0:
            for k in range(len(dropMenuOptions)):
                if dropMenuOptions[k] == option:
                    self.radioConfig[list(self.radioConfig.keys())[0]]['txRxPreambleCode'] = int(settingsOptions[k])
        else:
            found = 0
            for k in range(len(settingsOptions)):
                if int(settingsOptions[k]) == self.radioConfig[list(self.radioConfig.keys())[0]]['txRxPreambleCode']:
                    self.dropMenuPreamCode.setCurrentText(dropMenuOptions[k])
                    found = 1
            if found == 0:
                print(f"Illegal parameter in radio config: {self.radioConfig[list(self.radioConfig.keys())[0]]['txRxPreambleCode']}")
            self.configFormUpdate = 0
# Gets configuration from radio
    def radioGetConfig(self):
        if self.req:
            self.gui.getReqConfig()
            self.radioConfig = self.gui.radioConfigReq
        else:
            self.gui.getRespConfig()
            self.radioConfig = self.gui.radioConfigResp
        self.configFormUpdate = 1
        self.updateMenuPRF()
        self.configFormUpdate = 1
        self.updateMenuPreamLen()
        self.configFormUpdate = 1
        self.updateMenuBitRate()
        self.configFormUpdate = 1
        # self.updateMenuPAC()
        self.configFormUpdate = 1
        self.updateMenuChannel()
        self.configFormUpdate = 1
        self.updateMenuPreamCode()
        self.configFormUpdate = 1
        self.updateNodeID()
        self.configFormUpdate = 1
        self.updateTxPower()
        self.configFormUpdate = 1
        self.updateAntDelay()
        text = "Configuration Downloaded From Radio\n"
        self.gui.updateConsole(text)
        self.but_setRadioConfig.setStyleSheet(self.gui.buttonSheetBlue)

# Sets radio confiuration and makes it persist after reboot.
    def radioStoreConfig(self):
        self.configFormUpdate = 0
        self.updateMenuPRF()
        self.updateMenuPreamLen()
        self.updateMenuBitRate()
        # self.updateMenuPAC()
        self.updateMenuChannel()
        self.updateMenuPreamCode()
        self.updateNodeID()
        self.updateTxPower()
        self.updateAntDelay()
        self.but_storeRadioConfig.setStyleSheet("QPushButton {background-color: FireBrick;}")
        self.but_storeRadioConfig.setText("Writing...")
        self.flashTimer = QTimer()
        self.flashTimer.setInterval(500)
        self.flashTimer.timeout.connect(self.updateFlashButton)
        if self.req:
            self.gui.radioReq.API.radio_SetConfig_Request(self.gui.appSettings['reqRadio'], self.radioConfig, 1)
            self.gui.radioReq.API.radio_SetNodeID_Request(self.gui.appSettings['reqRadio'], self.gui.radioReqNodeID, 1)
        else:
            self.gui.radioResp.API.radio_SetConfig_Request(self.gui.appSettings['respRadio'], self.radioConfig, 1)
            self.gui.radioResp.API.radio_SetNodeID_Request(self.gui.appSettings['respRadio'], self.gui.radioRespNodeID, 1)
        self.flashTimer.start()
        text = "Configuration Updated In Flash\n"
        self.gui.updateConsole(text)
        self.radioGetConfig()

# Simply gives visual display delay to let flash save and indicate that it happened.
    def updateFlashButton(self):
        self.but_storeRadioConfig.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_storeRadioConfig.setText("Store in Flash")
        self.flashTimer.stop()
        self.flashTimer = None

# Updates current radio config without saving it to flash.
    def radioSetConfig(self):
        self.configFormUpdate = 0
        self.updateMenuPRF()
        self.updateMenuPreamLen()
        self.updateMenuBitRate()
        # self.updateMenuPAC()
        self.updateMenuChannel()
        self.updateMenuPreamCode()
        self.updateNodeID()
        self.updateTxPower()
        self.updateAntDelay()
        if self.req:
            self.gui.radioReq.API.radio_SetConfig_Request(self.gui.appSettings['reqRadio'], self.radioConfig, 0)
            self.gui.radioReq.API.radio_SetNodeID_Request(self.gui.appSettings['reqRadio'], self.gui.radioReqNodeID, 0)
        else:
            self.gui.radioResp.API.radio_SetConfig_Request(self.gui.appSettings['respRadio'], self.radioConfig, 0)
            self.gui.radioResp.API.radio_SetNodeID_Request(self.gui.appSettings['respRadio'], self.gui.radioRespNodeID, 0)
        text =  "Configuration Set\n"
        self.gui.updateConsole(text)
        self.radioGetConfig()
        self.but_setRadioConfig.setStyleSheet(self.gui.buttonSheetBlue)

## IP Config
    def radioGetIP(self):
        ip = ""
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            status, msg, addr = self.gui.radioReq.API.radio_GetIP_Request(ip)
        else:
            ip = self.gui.appSettings['respRadio']
            status, msg, addr = self.gui.radioResp.API.radio_GetIP_Request(ip)
        msg = msg['RADIO_GET_IP_CONFIRM']
        ip = msg['ipv4']
        netmask = msg ['netmask']
        gateway = msg['gateway']
        self.dispIP.setText(ip)
        self.dispNetMask.setText(netmask)
        self.dispGateWay.setText(gateway)

    def radioSetIP(self):
        newIP = self.dispIP.text()
        netmask = self.dispNetMask.text()
        gateway = self.dispGateWay.text()
        ip = ""
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            self.gui.radioReq.API.radio_SetIP_Request(ip, newIP, netmask, gateway)
        else:
            ip = self.gui.appSettings['respRadio']
            self.gui.radioResp.API.radio_SetIP_Request(ip, newIP, netmask, gateway)
        self.gui.updateConsole("\nRadio IP information updated\n")

    def radioReboot(self):
        newIP = self.dispIP.text()
        ip = ""
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            self.gui.radioReq.API.radio_Reboot_Request(ip)
            self.gui.appSettings['reqRadio'] = newIP
            self.connectedRequester = 0
            self.gui.dispreqRadio.setStyleSheet("QLineEdit {background-color: red;}")
            self.gui.radioReq.disconnect()
        else:
            ip = self.gui.appSettings['respRadio']
            self.gui.radioResp.API.radio_Reboot_Request(ip)
            self.gui.appSettings['respRadio'] = newIP
            self.gui.disprespRadio.setStyleSheet("QLineEdit {background-color: red;}")
            self.gui.radioResp.disconnect()
            self.connectedResponder = 0
        self.but_reboot.setStyleSheet("QPushButton {background-color: red;}")
        self.gui.updateConsole("\nRebooting Radio. Changing to new IP\n == Waiting for reboot ==\n")
        self.rebootTimer = QTimer()
        self.rebootTimer.setInterval(20000)
        self.rebootTimer.timeout.connect(self.radioReconnect)
        self.rebootTimer.start()
        self.gui.statsTimer.stop()
        self.gui.chipTempTimer.stop()

    def radioReconnect(self):
        self.rebootTimer.stop()
        if self.req:
            self.gui.dispreqRadio.setText(self.gui.appSettings['reqRadio'])
            self.gui.updateReqRadio()
        else:
            self.gui.disprespRadio.setText(self.gui.appSettings['respRadio'])
            self.gui.updateRespRadio()
        self.gui.updateConsole("\nAttempting reconnect after reboot\n")
        self.but_reboot.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.gui.statsTimer.start()
        self.gui.chipTempTimer.start()

## Presets

    # Gets a list of all presets on the radio and adds to dropdown menu.
    def radioGetPresets(self):
        ip = ""
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            msg, addr = self.gui.radioReq.API.radio_ListPresets_Request(ip)
        else:
            ip = self.gui.appSettings['respRadio']
            msg, addr = self.gui.radioResp.API.radio_ListPresets_Request(ip)
        msg = msg['RADIO_LIST_PRESETS_CONFIRM']
        presets = msg['presetNames']
        self.dropMenuPresets.clear()
        if len(presets) < 1:
            print("No presets stored on radio")
            self.dropMenuPresets.addItems(["Current Active Settings"])
        else:
            self.dropMenuPresets.addItems(["Current Active Settings"])
            self.dropMenuPresets.addItems(presets)

    def radioUpdateActivePreset(self):
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            nameMsgActive, addr = self.gui.radioReq.API.radio_Get_Active_Preset_Request(ip)
        else:
            ip = self.gui.appSettings['respRadio']
            nameMsgActive, addr = self.gui.radioReq.API.radio_Get_Active_Preset_Request(ip)
        # print(nameMsgActive)
        nameMsgActive = nameMsgActive['RADIO_GET_ACTIVE_PRESET_CONFIRM']
        nameActive = nameMsgActive['activePreset']
        self.dropMenuPresets.setCurrentText(nameActive)

    def radioUpdatePresets(self):
        # Get what is currently selected in drop down menu
        nameSelected = self.dropMenuPresets.currentText()
        ip = ""
        configMsgSelected = ""
        nameMsgActive = ""
        # Get the config of name currently selected in drop down
        # Get the name of the active preset if one exists.
        if self.req:
            ip = self.gui.appSettings['reqRadio']
            configMsgSelected, addr = self.gui.radioReq.API.radio_GetPreset_Request(ip, nameSelected)
            # nameMsgActive, addr = self.gui.radioReq.API.radio_Get_Active_Preset_Request(ip)
        else:
            ip = self.gui.appSettings['respRadio']
            configMsgSelected, addr = self.gui.radioResp.API.radio_GetPreset_Request(ip, nameSelected)
            # nameMsgActive, addr = self.gui.radioReq.API.radio_Get_Active_Preset_Request(ip)
        # nameMsgActive = nameMsgActive['RADIO_GET_ACTIVE_PRESET_CONFIRM']
        # nameActive = nameMsgActive['activePreset']
        # if a preset is active on radio and GUI does not match, make GUI match active preset. Else show current config
        if nameSelected == "Current Active Settings" or nameSelected == "":
            self.radioGetConfig()
            self.gui.windowChipTuning.radioGetTuning()
            self.dispNewPresetName.setText("Default")
            self.dropMenuPresets.setCurrentText("Current Active Settings")
        else:
            # This can come from opening a window or from changing the drop menu
            self.updatePresetGUI(configMsgSelected)
            self.dispNewPresetName.setText(nameSelected)

    # Gets the values stored in a preset on the radio and updates the gui to match without changing the config active on the radio
    def updatePresetGUI(self, msg):
        data = msg['RADIO_GET_PRESET_CONFIRM']
        # print(data)
        self.radioConfig[list(self.radioConfig.keys())[0]]['txRxPreambleCode'] = data['txRxPreambleCode']
        self.radioConfig[list(self.radioConfig.keys())[0]]['power'] = data['power']
        self.radioConfig[list(self.radioConfig.keys())[0]]['antennaDelay'] = data['antennaDelay']
        self.radioConfig[list(self.radioConfig.keys())[0]]['prf'] = data['prf']
        self.radioConfig[list(self.radioConfig.keys())[0]]['txPreambleLength'] = data['txPreambleLength']
        self.radioConfig[list(self.radioConfig.keys())[0]]['dataRate'] = data['dataRate']
        # self.radioConfig[list(self.radioConfig.keys())[0]]['PAC'] = data['PAC']
        self.radioConfig[list(self.radioConfig.keys())[0]]['channel'] = data['channel']
        self.radioConfig[list(self.radioConfig.keys())[0]]['txRxPreambleCode'] = data['txRxPreambleCode']
        # print(msg)
        # print(self.radioConfig)
        self.configFormUpdate = 1
        self.updateMenuPRF()
        self.configFormUpdate = 1
        self.updateMenuPreamLen()
        self.configFormUpdate = 1
        self.updateMenuBitRate()
        self.configFormUpdate = 1
        # self.updateMenuPAC()
        self.configFormUpdate = 1
        self.updateMenuChannel()
        self.configFormUpdate = 1
        self.updateMenuPreamCode()
        self.configFormUpdate = 1
        self.updateNodeID()
        self.configFormUpdate = 1
        self.updateTxPower()
        self.configFormUpdate = 1
        self.updateAntDelay()
        try:
            pgTarget = data['PGCount_Target']
        except:
            pgTarget = 0
        pgDelay = data['TC_PGDelay']
        rxDelay = data['RXAntDelay']
        txDelay = data['TXAntDelay']
        power = data['TxPwrContrl']
        byte3 = power >> 24
        byte2 = power & 0xff0000
        byte2 = byte2 >> 16
        byte1 = power & 0xff00
        byte1 = byte1 >> 8
        byte0 = power & 0xff
        self.gui.windowChipTuning.dispTXPower3.setText(hex(byte3))
        self.gui.windowChipTuning.dispTXPower2.setText(hex(byte2))
        self.gui.windowChipTuning.dispTXPower1.setText(hex(byte1))
        self.gui.windowChipTuning.dispTXPower0.setText(hex(byte0))
        self.gui.windowChipTuning.dispPGTarget.setText(hex(pgTarget))
        self.gui.windowChipTuning.dispPGDelay.setText(hex(pgDelay))
        self.gui.windowChipTuning.dispRXDelay.setText(hex(rxDelay))
        self.gui.windowChipTuning.dispTXDelay.setText(hex(txDelay))

    # Creates a new preset name and stores the active parameters on the radio, not necessarily what is on the GUI if they do not match.
    def radioSavePreset(self):
        name = self.dispNewPresetName.text()
        if name == "":
            print("Please enter a preset name")
            self.gui.updateConsole("\n== Please enter a preset name == \n")
        else:
            lock = "false"
            ip = ""
            self.radioSetConfig()
            if self.req:
                ip = self.gui.appSettings['reqRadio']
                self.gui.radioReq.API.radio_SavePreset_Request(ip, name, lock)
            else:
                ip = self.gui.appSettings['respRadio']
                self.gui.radioResp.API.radio_SavePreset_Request(ip, name, lock)
            self.radioGetPresets()
            self.gui.updateConsole("\nPreset saved\n")
            self.dropMenuPresets.setCurrentText(name)
            # print(len(self.dropMenuPresets))
            # for i in range(len(self.dropMenuPresets)):
            #     print(self.dropMenuPresets.itemText(i))

    # Saves preset with locked write permissions
    def radioLockSavePreset(self):
        name = self.dispNewPresetName.text()
        if name == "":
            print("Please enter a preset name")
            self.gui.updateConsole("\n== Please enter a preset name == \n")
        else:
            lock = "true"
            ip = ""
            if self.req:
                ip = self.gui.appSettings['reqRadio']
                self.gui.radioReq.API.radio_SavePreset_Request(ip, name, lock)
            else:
                ip = self.gui.appSettings['respRadio']
                self.gui.radioResp.API.radio_SavePreset_Request(ip, name, lock)
            self.gui.updateConsole("\nLocked preset saved\n")
            self.radioGetPresets()

    # Causes a preset to be applied to the radio.
    def radioApplyPreset(self):
        name = self.dropMenuPresets.currentText()
        if name == "" or name == "No Stored Presets":
            print("Need to first save a preset before it can be applied")
            self.gui.updateConsole("\n== Need to first save a preset before it can be applied ==\n")
        else:
            persist = 0
            ip = ""
            if self.req:
                ip = self.gui.appSettings['reqRadio']
                self.gui.radioReq.API.radio_ApplyPreset_Request(ip, name, persist)
            else:
                ip = self.gui.appSettings['respRadio']
                self.gui.radioResp.API.radio_ApplyPreset_Request(ip, name, persist)
            self.gui.updateConsole("\nPreset Applied\n")
            self.radioGetConfig()
            self.gui.windowChipTuning.radioGetTuning()

    # Applies with persistence after reboot.
    def radioPersistPreset(self):
        name = self.dropMenuPresets.currentText()
        if name == "" or name == "No Stored Presets":
            print("Need to first save a preset before it can be applied")
            self.gui.updateConsole("\n== Need to first save a preset before it can be applied ==\n")
        else:
            persist = 1
            ip = ""
            if self.req:
                ip = self.gui.appSettings['reqRadio']
                self.gui.radioReq.API.radio_ApplyPreset_Request(ip, name, persist)
            else:
                ip = self.gui.appSettings['respRadio']
                self.gui.radioResp.API.radio_ApplyPreset_Request(ip, name, persist)
            self.gui.updateConsole("\nPersistent Preset Applied\n")
            self.radioGetConfig()
            self.gui.windowChipTuning.radioGetTuning()

    # Deletes a preset from the radio.
    def radioDeletePreset(self):
        name = self.dropMenuPresets.currentText()
        if name == "" or name == "No Stored Presets" or name == "Current Active Settings":
            print("No presets to delete")
            self.gui.updateConsole("\n== No presets to delete == \n")
        else:
            ip = ""
            if self.req:
                ip = self.gui.appSettings['reqRadio']
                self.gui.radioReq.API.radio_DeletePreset_Request(ip, name)
            else:
                ip = self.gui.appSettings['respRadio']
                self.gui.radioResp.API.radio_DeletePreset_Request(ip, name)
            self.gui.updateConsole("\nSelected Preset Deleted\n")
            self.radioGetPresets()
            self.dropMenuPresets.setCurrentText("Current Active Settings")

    # Indicates that config has changed and needs to be updated on the radio.
    def updateConfigButton(self):
        self.but_setRadioConfig.setStyleSheet("QPushButton {background-color: yellow; color: black;}")

## GUI
    def initGUI(self):
        xStart = 80
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 460
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        if self.req:
            self.labelWindow.setText("Requester Configuration")
        else:
            self.labelWindow.setText("Responder Configuration")
        xStart = 20
        yStart = 240
        xBias = 0
        yBias = 0
        xBump = 210
        yBump = 80
        xWidth = 160
        yWidth = 40
        x = 0
        y = 0
        self.labelNodeID = QLabel(self)
        self.labelNodeID.resize(xWidth,yWidth)
        self.labelNodeID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelNodeID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelNodeID.setFont(self.guiFont.guiFont20)
        self.labelNodeID.setText("NodeID")
        self.dispNodeID = QLineEdit(self)
        self.dispNodeID.setFont(self.guiFont.guiFont20)
        self.dispNodeID.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispNodeID.resize(xWidth,yWidth)
        self.dispNodeID.setStyleSheet(self.gui.lineSheetYellow)
        self.dispNodeID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispNodeID.setText("-")
        self.dispNodeID.editingFinished.connect(self.updateConfigButton)

        x = 1
        y = 0
        self.labelTxPower = QLabel(self)
        self.labelTxPower.resize(xWidth,yWidth)
        self.labelTxPower.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTxPower.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTxPower.setFont(self.guiFont.guiFont20)
        self.labelTxPower.setText("Tx Power")
        self.dispTxPower = QLineEdit(self)
        self.dispTxPower.setFont(self.guiFont.guiFont20)
        self.dispTxPower.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispTxPower.resize(xWidth,yWidth)
        self.dispTxPower.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispTxPower.setText("-")
        self.dispTxPower.setStyleSheet(self.gui.lineSheetYellow)
        self.dispTxPower.setToolTip('Tx Power Valid Range (X - X)')
        self.dispTxPower.editingFinished.connect(self.updateConfigButton)

        x = 2
        y = 0
        self.labelAntDelay = QLabel(self)
        self.labelAntDelay.resize(xWidth,yWidth)
        self.labelAntDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelAntDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelAntDelay.setFont(self.guiFont.guiFont20)
        self.labelAntDelay.setText("Antenna Delay")
        self.dispAntDelay = QLineEdit(self)
        self.dispAntDelay.setFont(self.guiFont.guiFont20)
        self.dispAntDelay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispAntDelay.resize(xWidth,yWidth)
        self.dispAntDelay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispAntDelay.setStyleSheet(self.gui.lineSheetYellow)
        self.dispAntDelay.setText("-")
        self.dispAntDelay.setToolTip('Antenna Electrical Delay (ps)')
        self.dispAntDelay.editingFinished.connect(self.updateConfigButton)
        # self.dispAntDelay.editingFinished.connect(self.updateAntDelay)

        xStart = 20
        yStart = 80
        xBias = 0
        yBias = 0
        xBump = 210
        yBump = 80
        xWidth = 200
        yWidth = 40
        x = 0
        y = 0
        dropMenuOptions = ["16MHz", "64Mhz"]
        self.labelDropMenuPRF = QLabel(self)
        self.labelDropMenuPRF.resize(xWidth,yWidth)
        self.labelDropMenuPRF.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuPRF.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuPRF.setFont(self.guiFont.guiFont20)
        self.labelDropMenuPRF.setText("Pulse Rate(PRF)")
        xWidth = 160
        self.dropMenuPRF = QComboBox(self)
        self.dropMenuPRF.resize(xWidth,yWidth)
        self.dropMenuPRF.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuPRF.setFont(self.guiFont.guiFont20)
        self.dropMenuPRF.addItems(dropMenuOptions)
        self.dropMenuPRF.setEditable(False)
        self.dropMenuPRF.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuPRF.setToolTip("Radio Pulse Rate")
        self.dropMenuPRF.currentTextChanged.connect(self.updateConfigButton)

        xWidth = 260
        x = 1
        y = 0
        dropMenuOptions = ["64", "128", "256", "512", "1024", "1536", "2048", "4096"]
        self.labelDropMenuPreamLen = QLabel(self)
        self.labelDropMenuPreamLen.resize(xWidth,yWidth)
        self.labelDropMenuPreamLen.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuPreamLen.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuPreamLen.setFont(self.guiFont.guiFont20)
        self.labelDropMenuPreamLen.setText("Preamble Length")
        xWidth = 160
        self.dropMenuPreamLen = QComboBox(self)
        self.dropMenuPreamLen.resize(xWidth,yWidth)
        self.dropMenuPreamLen.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuPreamLen.setFont(self.guiFont.guiFont20)
        self.dropMenuPreamLen.addItems(dropMenuOptions)
        self.dropMenuPreamLen.setEditable(False)
        self.dropMenuPreamLen.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuPreamLen.setToolTip("Length Of Preamble Code")
        self.dropMenuPreamLen.currentTextChanged.connect(self.updateConfigButton)

        xWidth = 260
        x = 2
        y = 0
        dropMenuOptions = ["110Kb", "850Kb", "6.8Mb"]
        self.labelDropMenuBitRate = QLabel(self)
        self.labelDropMenuBitRate.resize(xWidth,yWidth)
        self.labelDropMenuBitRate.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuBitRate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuBitRate.setFont(self.guiFont.guiFont20)
        self.labelDropMenuBitRate.setText("Bit Rate")
        xWidth = 160
        self.dropMenuBitRate = QComboBox(self)
        self.dropMenuBitRate.resize(xWidth,yWidth)
        self.dropMenuBitRate.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuBitRate.setFont(self.guiFont.guiFont20)
        self.dropMenuBitRate.addItems(dropMenuOptions)
        self.dropMenuBitRate.setEditable(False)
        self.dropMenuBitRate.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuBitRate.setToolTip("Radio Data Rate")
        self.dropMenuBitRate.currentTextChanged.connect(self.updateConfigButton)

        xWidth = 260
        x = 0
        y = 1
        dropMenuOptions = ["8", "16", "32", "64"]
        self.labelDropMenuPAC = QLabel(self)
        self.labelDropMenuPAC.resize(xWidth,yWidth)
        self.labelDropMenuPAC.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuPAC.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuPAC.setFont(self.guiFont.guiFont20)
        self.labelDropMenuPAC.setText("Preamble Accum")
        xWidth = 160
        self.dropMenuPAC = QComboBox(self)
        self.dropMenuPAC.resize(xWidth,yWidth)
        self.dropMenuPAC.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuPAC.setFont(self.guiFont.guiFont20)
        self.dropMenuPAC.addItems(dropMenuOptions)
        self.dropMenuPAC.setEditable(False)
        self.dropMenuPAC.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuPAC.setToolTip("Preamble Accumulation Count(Integration)")
        self.dropMenuBitRate.currentTextChanged.connect(self.updateConfigButton)

        xWidth = 260
        x = 1
        y = 1
        dropMenuOptions = ["4.5GHz(3)", "6.5GHz(5)", "8GHz(9)"]
        self.labelDropMenuChannel = QLabel(self)
        self.labelDropMenuChannel.resize(xWidth,yWidth)
        self.labelDropMenuChannel.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuChannel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuChannel.setFont(self.guiFont.guiFont20)
        self.labelDropMenuChannel.setText("RF Channel")
        xWidth = 160
        self.dropMenuChannel = QComboBox(self)
        self.dropMenuChannel.resize(xWidth,yWidth)
        self.dropMenuChannel.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuChannel.setFont(self.guiFont.guiFont20)
        self.dropMenuChannel.addItems(dropMenuOptions)
        self.dropMenuChannel.setEditable(False)
        self.dropMenuChannel.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuChannel.setToolTip("RF Channel For Radio Link")
        self.dropMenuChannel.currentTextChanged.connect(self.updateConfigButton)

        xWidth = 260
        x = 2
        y = 1
        dropMenuOptions = ["9", "10", "11", "12", "13"]
        self.labelDropMenuPreamCode = QLabel(self)
        self.labelDropMenuPreamCode.resize(xWidth,yWidth)
        self.labelDropMenuPreamCode.move(x*xBump + xStart, yStart + y*yBump + yBias)
        self.labelDropMenuPreamCode.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDropMenuPreamCode.setFont(self.guiFont.guiFont20)
        self.labelDropMenuPreamCode.setText("Preamble Code")
        xWidth = 160
        self.dropMenuPreamCode = QComboBox(self)
        self.dropMenuPreamCode.resize(xWidth,yWidth)
        self.dropMenuPreamCode.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 30)
        self.dropMenuPreamCode.setFont(self.guiFont.guiFont20)
        self.dropMenuPreamCode.addItems(dropMenuOptions)
        self.dropMenuPreamCode.setEditable(False)
        self.dropMenuPreamCode.setToolTip("Radio Preamble Code")
        self.dropMenuPreamCode.setStyleSheet(self.gui.dropSheetGray)
        self.dropMenuPreamCode.currentTextChanged.connect(self.updateConfigButton)

        xStart = 50
        yStart = 340
        xBias = 0
        yBias = 0
        xBump = 180
        yBump = 80
        xWidth = 160
        yWidth = 40
        x = 0
        y = 0
        self.but_getRadioConfig = QPushButton('Get Config', self)
        self.but_getRadioConfig.setToolTip('Get Radio Configuration')
        self.but_getRadioConfig.resize(xWidth, yWidth)
        self.but_getRadioConfig.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_getRadioConfig.setFont(self.guiFont.guiFont14)
        self.but_getRadioConfig.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_getRadioConfig.clicked.connect(self.radioGetConfig)

        x = 1
        y = 0
        self.but_storeRadioConfig = QPushButton('Store in Flash', self)
        self.but_storeRadioConfig.setToolTip('Store Radio Configuration In Flash')
        self.but_storeRadioConfig.resize(xWidth, yWidth)
        self.but_storeRadioConfig.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_storeRadioConfig.setFont(self.guiFont.guiFont14)
        self.but_storeRadioConfig.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_storeRadioConfig.clicked.connect(self.radioStoreConfig)

        x = 2
        y = 0
        self.but_setRadioConfig = QPushButton('Set Config', self)
        self.but_setRadioConfig.setToolTip('Set Radio Configuration')
        self.but_setRadioConfig.resize(xWidth, yWidth)
        self.but_setRadioConfig.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_setRadioConfig.setFont(self.guiFont.guiFont14)
        self.but_setRadioConfig.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_setRadioConfig.clicked.connect(self.radioSetConfig)

        self.dispSep1 = QLineEdit(self)
        self.dispSep1.move(60, yStart + y*yBump + yBias + 60)
        self.dispSep1.resize(500,1)
        self.dispSep1.setStyleSheet("QLineEdit {background-color: black; color: black;}")

## IP Config
        yStart = 410
        xWidth = 240
        xStart = 20
        x = 1
        y = 0
        self.labelIPConfig = QLabel(self)
        self.labelIPConfig.resize(xWidth,yWidth)
        self.labelIPConfig.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelIPConfig.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelIPConfig.setFont(self.guiFont.guiFont24)
        self.labelIPConfig.setText("IP Configuration")
        yStart = 460
        xWidth = 160
        xStart = 30
        xBump = 200
        x = 0
        y = 0
        self.but_getIP = QPushButton('Get IP Config', self)
        self.but_getIP.setToolTip('Get Current IP config')
        self.but_getIP.resize(xWidth, yWidth)
        self.but_getIP.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_getIP.setFont(self.guiFont.guiFont14)
        self.but_getIP.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_getIP.clicked.connect(self.radioGetIP)
        x = 1
        y = 0
        self.but_setIP = QPushButton('Set IP Config', self)
        self.but_setIP.setToolTip('Set new IP config')
        self.but_setIP.resize(xWidth, yWidth)
        self.but_setIP.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_setIP.setFont(self.guiFont.guiFont14)
        self.but_setIP.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_setIP.clicked.connect(self.radioSetIP)
        x = 2
        y = 0
        self.but_reboot = QPushButton('Reboot', self)
        self.but_reboot.setToolTip('Reboot radio using new IP settings')
        self.but_reboot.resize(xWidth, yWidth)
        self.but_reboot.setStyleSheet("QPushButton {background-color: DarkOrange;}")
        self.but_reboot.setFont(self.guiFont.guiFont14)
        self.but_reboot.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_reboot.clicked.connect(self.radioReboot)

        yStart = 500
        xStart = 10
        xWidth = 200
        xBump = 200
        x = 0
        y = 0
        self.labelIP = QLabel(self)
        self.labelIP.resize(xWidth,yWidth)
        self.labelIP.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelIP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelIP.setFont(self.guiFont.guiFont20)
        self.labelIP.setText("IPV4 Address")
        self.dispIP = QLineEdit(self)
        self.dispIP.setFont(self.guiFont.guiFont20)
        self.dispIP.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispIP.resize(xWidth,yWidth)
        self.dispIP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispIP.setStyleSheet(self.gui.lineSheetYellow)
        self.dispIP.setText("xxx.xxx.xxx.xxx")
        self.dispIP.setToolTip('Enter new IP address as xxx.xxx.xxx.xxx')
        x = 1
        y = 0
        self.labelNetMask = QLabel(self)
        self.labelNetMask.resize(xWidth,yWidth)
        self.labelNetMask.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelNetMask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelNetMask.setFont(self.guiFont.guiFont20)
        self.labelNetMask.setText("Netmask")
        self.dispNetMask = QLineEdit(self)
        self.dispNetMask.setFont(self.guiFont.guiFont20)
        self.dispNetMask.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispNetMask.resize(xWidth,yWidth)
        self.dispNetMask.setStyleSheet(self.gui.lineSheetYellow)
        self.dispNetMask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispNetMask.setText("xxx.xxx.xxx.xxx")
        self.dispNetMask.setToolTip('Enter new netmask as xxx.xxx.xxx.xxx')
        x = 2
        y = 0
        self.labelGateWay = QLabel(self)
        self.labelGateWay.resize(xWidth,yWidth)
        self.labelGateWay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelGateWay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelGateWay.setFont(self.guiFont.guiFont20)
        self.labelGateWay.setText("Gateway")
        self.dispGateWay = QLineEdit(self)
        self.dispGateWay.setFont(self.guiFont.guiFont20)
        self.dispGateWay.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 35)
        self.dispGateWay.resize(xWidth,yWidth)
        self.dispGateWay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispGateWay.setStyleSheet(self.gui.lineSheetYellow)
        self.dispGateWay.setText("xxx.xxx.xxx.xxx")
        self.dispGateWay.setToolTip('Enter new default gateway as xxx.xxx.xxx.xxx')

        self.dispSep2 = QLineEdit(self)
        self.dispSep2.move(60, yStart + y*yBump + yBias + 90)
        self.dispSep2.resize(500,1)
        self.dispSep2.setStyleSheet("QLineEdit {background-color: black; color: black;}")

## Presets
        xWidth = 160
        yStart = 600
        xStart = 20
        x = 1
        y = 0
        self.labelPresets = QLabel(self)
        self.labelPresets.resize(xWidth,yWidth)
        self.labelPresets.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelPresets.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelPresets.setFont(self.guiFont.guiFont24)
        self.labelPresets.setText("Presets")

        xStart = 20
        yBump = 50
        x = 0
        y = 1
        self.but_savePreset = QPushButton('Store/Update', self)
        self.but_savePreset.setToolTip('Store/Update listed radio preset')
        self.but_savePreset.resize(xWidth, yWidth)
        self.but_savePreset.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_savePreset.setFont(self.guiFont.guiFont14)
        self.but_savePreset.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_savePreset.clicked.connect(self.radioSavePreset)

        x = 0
        y = 1
        xBias = 180
        self.dispNewPresetName = QLineEdit(self)
        self.dispNewPresetName.setFont(self.guiFont.guiFont20)
        self.dispNewPresetName.setToolTip('Enter name of preset to create or update')
        self.dispNewPresetName.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispNewPresetName.resize(400,yWidth)
        self.dispNewPresetName.setStyleSheet(self.gui.lineSheetYellow)
        self.dispNewPresetName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispNewPresetName.setText("Default")

        self.dispSep3 = QLineEdit(self)
        self.dispSep3.move(60, yStart + y*yBump + yBias + 65)
        self.dispSep3.resize(500,1)
        self.dispSep3.setStyleSheet("QLineEdit {background-color: black; color: black;}")

        xBump = 200
        xBias = 0
        xStart = 30
        yBias = 40
        x = 0
        y = 2
        self.but_applyPreset = QPushButton('Apply Preset', self)
        self.but_applyPreset.setToolTip('Apply Listed Radio Preset')
        self.but_applyPreset.resize(xWidth, yWidth)
        self.but_applyPreset.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_applyPreset.setFont(self.guiFont.guiFont14)
        self.but_applyPreset.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_applyPreset.clicked.connect(self.radioApplyPreset)

        x = 1
        y = 2
        self.but_persistPreset = QPushButton('Persist Preset', self)
        self.but_persistPreset.setToolTip('Preset persists after reboot')
        self.but_persistPreset.resize(xWidth, yWidth)
        self.but_persistPreset.setStyleSheet("QPushButton {background-color: DarkOrange}")
        self.but_persistPreset.setFont(self.guiFont.guiFont14)
        self.but_persistPreset.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_persistPreset.clicked.connect(self.radioPersistPreset)

        x = 2
        y = 2
        self.but_deletePreset = QPushButton('Delete Preset', self)
        self.but_deletePreset.setToolTip('Delete Preset Listed in Drop Menu')
        self.but_deletePreset.resize(xWidth, yWidth)
        self.but_deletePreset.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_deletePreset.setFont(self.guiFont.guiFont14)
        self.but_deletePreset.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_deletePreset.clicked.connect(self.radioDeletePreset)

        x = 0
        y = 3
        xStart = 50
        xWidth = 80
        xBias = 0
        # dropMenuOptions = ["HDR - Omni", "HDR - Directional", "MDR - Omni", "MDR - Directional"]
        self.dropMenuPresets = QComboBox(self)
        self.dropMenuPresets.resize(520,yWidth)
        self.dropMenuPresets.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dropMenuPresets.setFont(self.guiFont.guiFont20)
        self.dropMenuPresets.addItems(dropMenuOptions)
        self.dropMenuPresets.setEditable(False)
        self.dropMenuPresets.setStyleSheet(self.gui.dropSheetBlue)
        self.dropMenuPresets.setToolTip("Selects which preset to load")
        self.dropMenuPresets.currentTextChanged.connect(self.radioUpdatePresets)

# Class for window for data transfer
class windowDataTransfer(QWidget):
    def __init__(self, gui):
        super().__init__()
        self.setWindowTitle("Data Transfer")
        self.setGeometry(0, 0, 800, 540)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.guiFont = guiFonts()
        self.radioData = TDSR_radioControl.dataCmds(self.gui)
        self.dataDestination = 0
        self.dataDestinationSlot = 0
        self.initGUI()

    def displayWindow(self):
        if self.gui.radioMode != 'networking':
            self.dropMenuDestination.clear()
            self.dropMenuDestination.addItems([str(self.gui.appSettings['respID'])])
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowDataTransfer.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def getTransferFilename(self):
        if self.gui.platform == "linux":
            xfrFileName = QFileDialog.getOpenFileName(self, 'Pick File to Transfer', "./Uploads", options=QFileDialog.Option.DontUseNativeDialog)
        else:
            xfrFileName = QFileDialog.getOpenFileName(self, 'Pick File to Transfer', "./Uploads")
        if xfrFileName != "":
            xfrFileName = xfrFileName[0]
            self.dispfileSelect.setText(str(xfrFileName))
# Update settings for Download Path.
    def updateDownloadName(self):
        self.gui.appSettings['downloadDirectory'] = self.dispDownloads.text()

    def getDownloadPath(self):
        if self.gui.platform == "linux":
            downloadPath = QFileDialog.getExistingDirectory(self, 'Choose Download Directory', str(self.gui.appSettings['downloadDirectory']), options=QFileDialog.Option.DontUseNativeDialog)
        else:
            downloadPath = QFileDialog.getExistingDirectory(self, 'Choose Download Directory', str(self.gui.appSettings['downloadDirectory']))
        if downloadPath != "":
            downloadPath = downloadPath + "/"
            self.dispDownloads.setText(str(downloadPath))
            self.gui.appSettings['downloadDirectory'] = downloadPath
# Update settings for Download Path.
    def updateDownloadName(self):
        self.gui.appSettings['downloadDirectory'] = self.dispDownloads.text()

    def updateRespAvailable(self):
        if self.gui.connectedResponder == 1:
            if self.gui.windowDataTransfer.isVisible():
                self.resize(800,715)    # if visible, resize it in place vs moving it
            else:
                self.setGeometry(10, 10, 800, 715)  # if not open, initialize the geometry to known
            self.labelRespTextReceived.setHidden(False) # Show the extra fields
            self.dataRespTextReceived.setHidden(False)
            self.dataRespTextReceivedScrollBar.setHidden(False)
        else:
            if self.gui.windowDataTransfer.isVisible():     # if not connected, hide the responder fields.
                self.labelRespTextReceived.setHidden(True)
                self.dataRespTextReceived.setHidden(True)
                self.dataRespTextReceivedScrollBar.setHidden(True)
                self.resize(800,540)
            else:
                self.setGeometry(10, 10, 800, 540)

    def updateDropMenuDest(self):
        tmpDest = -1
        forwardSlot = -1
        backSlot = -1
        self.dataBackSlot = 0
        #first pass is triggered by clear and is invalid. Immediately followed by population of node data
        if self.dropMenuDestination.currentText() != "":
            tmpDest = int(self.dropMenuDestination.currentText())  # Where do we want to send
            # print("dest", tmpDest)
            if self.gui.windowNetwork.slotMap:
                for i in range(len(self.gui.windowNetwork.slotMap)):
                        # Check for route to destination
                    # print("target, reqnode", int(self.gui.windowNetwork.slotMap[i]['targetId']), self.gui.radioReqNodeID)
                    # print("owner, dest", int(self.gui.windowNetwork.slotMap[i]['ownerId']), tmpDest)
                    if int(self.gui.windowNetwork.slotMap[i]['targetId']) == tmpDest:
                        forwardSlot = i
                        self.gui.windowNetwork.destSlotDataMax = int(self.gui.windowNetwork.slotMap[i]['maxUserData'])
                        # Check for return route for Ack.
                    if (int(self.gui.windowNetwork.slotMap[i]['targetId']) == self.gui.radioReqNodeID) and (int(self.gui.windowNetwork.slotMap[i]['ownerId']) == tmpDest):
                        backSlot = i
                if tmpDest >= 0 and forwardSlot >= 0 and backSlot >=0:
                      self.dataDestinationSlot = forwardSlot
                      self.dataDestination = tmpDest
                      self.dataBackSlot = backSlot
                else:
                    if forwardSlot == -1:
                        tmp = "\n===\nNo data slot to destination.\n  Need to adjust slotmap\n===\n"
                        self.gui.updateConsole(tmp)
                        self.dataDestinationSlot = 0
                        self.dataBackSlot = 0
                    if backSlot == -1:
                        tmp = "\n===\nNo data slot back from destination for\n  acknowledge. Need to adjust slotmap\n===\n"
                        self.gui.updateConsole(tmp)
                        self.dataDestinationSlot = forwardSlot
                        self.dataDestination = tmpDest
                        self.dataBackSlot = -1

    def initGUI(self):
        xStart = 275
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 250
        yWidth = 40
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText("Data Transfer")

        xStart = 10
        yStart = 65
        xBias = 0
        yBias = 0
        xBump = 190
        yBump = 0
        xWidth = 180
        yWidth = 40
        x = 2
        y = 0
        self.labelDestination = QLabel(self)
        self.labelDestination.resize(xWidth,yWidth)
        self.labelDestination.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelDestination.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelDestination.setFont(self.guiFont.guiFont20)
        self.labelDestination.setText("Send To:")
        x = 2
        xBias = 120
        self.dropMenuDestination = QComboBox(self)
        self.dropMenuDestination.resize(xWidth,yWidth)
        self.dropMenuDestination.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias - 10)
        self.dropMenuDestination.setFont(self.guiFont.guiFont20)
        self.dropMenuDestination.setEditable(False)
        self.dropMenuDestination.setStyleSheet(self.gui.dropSheetBlue)
        self.dropMenuDestination.setToolTip("Which radio are we sending to?")
        self.dropMenuDestination.currentTextChanged.connect(self.updateDropMenuDest)
        xBias = 0
        x = 0
        y = 0
        self.labelTextInput = QLabel(self)
        self.labelTextInput.resize(xWidth,yWidth)
        self.labelTextInput.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTextInput.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelTextInput.setFont(self.guiFont.guiFont20)
        self.labelTextInput.setText("Text to Transmit")
        xStart = 200
        yStart = 60
        xWidth = 60
        yWidth = 40
        self.but_textSend = QPushButton('Send', self)
        self.but_textSend.setToolTip('Sends text from requester to responder')
        self.but_textSend.resize(xWidth, yWidth)
        self.but_textSend.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_textSend.setFont(self.guiFont.guiFont14)
        self.but_textSend.move(x*xBump + xBias + xStart, y*yBump + yBias - 5 + yStart)
        self.but_textSend.clicked.connect(self.radioData.reqSendTextData)
        xStart = 10
        yStart = 100
        xWidth = 780
        yWidth = 100
        self.dataTextInput = QTextEdit(self)
        self.dataTextInput.setGeometry(xStart,yStart,xWidth, yWidth)
        self.dataTextInput.setText("")
        self.dataTextInputScrollBar = self.dataTextInput.verticalScrollBar()
        self.dataTextInput.setStyleSheet("QTextEdit {background-color: rgb(240,240,240);}")
        xStart = 10
        yStart = 220
        xWidth = 200
        yWidth = 40
        self.labelTextReceived = QLabel(self)
        self.labelTextReceived.resize(xWidth,yWidth)
        self.labelTextReceived.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTextReceived.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelTextReceived.setFont(self.guiFont.guiFont20)
        self.labelTextReceived.setText("Received Text")
        xStart = 10
        yStart = 255
        xWidth = 780
        yWidth = 100
        self.dataReqTextReceived = QTextBrowser(self)
        self.dataReqTextReceived.setGeometry(xStart,yStart,xWidth, yWidth)
        self.dataReqTextReceived.setText("")
        self.dataReqTextReceivedScrollBar = self.dataReqTextReceived.verticalScrollBar()
        self.dataReqTextReceived.setStyleSheet("QTextBrowser {background-color: rgb(240,240,240);}")

        yStart = 380
        xStart = 10
        xBias = 0
        yBias = 0
        xBump = 210
        yBump = 30
        xWidth = 200
        yWidth = 40
        x = 0
        y = 0
        self.labelTransfers = QLabel(self)
        self.labelTransfers.resize(xWidth,yWidth)
        self.labelTransfers.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelTransfers.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelTransfers.setFont(self.guiFont.guiFont20)
        self.labelTransfers.setText("File Transfer")
        x = 0
        y = 1
        self.but_fileSelect = QPushButton('Choose File', self)
        self.but_fileSelect.setToolTip('Pick File to Transfer')
        self.but_fileSelect.resize(xWidth, yWidth)
        self.but_fileSelect.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_fileSelect.setFont(self.guiFont.guiFont14)
        self.but_fileSelect.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_fileSelect.clicked.connect(self.getTransferFilename)
        xWidth = 500
        x = 1
        y = 1
        self.dispfileSelect = QLineEdit(self)
        self.dispfileSelect.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispfileSelect.setFont(self.guiFont.guiFont18)
        self.dispfileSelect.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispfileSelect.resize(xWidth,yWidth)
        self.dispfileSelect.setAlignment(Qt.AlignmentFlag.AlignLeft)
        xStart = 730
        xWidth = 60
        x = 0
        self.but_fileSend = QPushButton('Send', self)
        self.but_fileSend.setToolTip('Pick File to Transfer')
        self.but_fileSend.resize(xWidth, yWidth)
        self.but_fileSend.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_fileSend.setFont(self.guiFont.guiFont14)
        self.but_fileSend.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_fileSend.clicked.connect(self.radioData.reqSendBase64File)
        # self.dispfileSelect.setText("-")
        xStart = 10
        xWidth = 200
        yWidth = 40
        yBias = 20
        x = 0
        y = 2
        self.labelIncoming = QLabel(self)
        self.labelIncoming.resize(xWidth,yWidth)
        self.labelIncoming.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelIncoming.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelIncoming.setFont(self.guiFont.guiFont20)
        self.labelIncoming.setText("Incoming Files")
        xWidth = 200
        x = 0
        y = 3
        self.but_Downloads = QPushButton('Download Directory', self)
        self.but_Downloads.setToolTip('Pick Download Directory Name')
        self.but_Downloads.resize(xWidth, yWidth)
        self.but_Downloads.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_Downloads.setFont(self.guiFont.guiFont14)
        self.but_Downloads.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_Downloads.clicked.connect(self.getDownloadPath)
        xWidth = 570
        x = 1
        y = 3
        self.dispDownloads = QLineEdit(self)
        self.dispDownloads.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispDownloads.setFont(self.guiFont.guiFont18)
        self.dispDownloads.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispDownloads.resize(xWidth,yWidth)
        self.dispDownloads.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.dispDownloads.setText(str(self.gui.appSettings['downloadDirectory']))
        self.dispDownloads.editingFinished.connect(self.updateDownloadName)
        self.guiLogName = 1

        xStart = 10
        yStart = 570
        xWidth = 400
        yWidth = 40
        xBump = 0
        yBump = 0
        xBias = 0
        yBias = 0
        x = 0
        y = 0
        self.labelRespTextReceived = QLabel(self)
        self.labelRespTextReceived.resize(xWidth,yWidth)
        self.labelRespTextReceived.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelRespTextReceived.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelRespTextReceived.setFont(self.guiFont.guiFont20)
        self.labelRespTextReceived.setText("Connected Responder Received Text")
        self.labelRespTextReceived.setHidden(False)
        yBias = 35
        xWidth = 780
        yWidth = 100
        self.dataRespTextReceived = QTextBrowser(self)
        self.dataRespTextReceived.setGeometry(xStart,yStart + yBias,xWidth, yWidth)
        self.dataRespTextReceived.setText("")
        self.dataRespTextReceived.setHidden(False)
        self.dataRespTextReceivedScrollBar = self.dataRespTextReceived.verticalScrollBar()
        self.dataRespTextReceivedScrollBar.setHidden(False)
        self.dataRespTextReceived.setStyleSheet("QTextBrowser {background-color: rgb(240,240,240);}")

# Class for window to display and set data logging options.
class windowLogFile(QWidget):
    def __init__(self, gui):
        super().__init__()
        # self.setGeometry(10, 10, 800, 400)
        self.setFixedSize(730,350)
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.setWindowTitle("Data Logging")
        self.guiFont = guiFonts()
        self.initGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowLogging.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)
# Display name for name based logging.
    def updateLogName(self):
        self.gui.logFile.closeLogFile()
        self.gui.appSettings['logFile'] = self.dispLogName.text()
# Display root directory for log storage.
    def updateLogDirName(self):
        self.gui.logFile.closeLogFile()
        self.gui.appSettings['logDirectory'] = self.dispLogDir.text()
# Turn logging on and off
    def toggleLogging(self):
        if self.gui.appSettings['enableLogging'] == 1:
            self.gui.appSettings['enableLogging'] = 0
            self.but_enableLogging.setText("Logging Disabled")
            self.but_enableLogging.setStyleSheet(self.gui.buttonSheetBlue)
            self.gui.logFile.closeLogFile()
        else:
            self.gui.appSettings['enableLogging'] = 1
            self.but_enableLogging.setText("Logging Enabled")
            self.but_enableLogging.setStyleSheet("QPushButton {background-color: coral;}")
            # self.gui.logFile.logToFile(None, self.gui.appSettings['reqRadio'])
# Sets whether logs are one large file or broken up by a determined length of time.
    def updateLogSegmented(self):
        self.gui.appSettings['segmentTime'] = self.dispSegmentTime.text()
        if self.check_logSegmented.isChecked():
            self.gui.appSettings['logSegmented'] = 1
        else:
            self.gui.appSettings['logSegmented'] = 0
# Sets log names to autogenerated based on date/time
    def updateLogDateBased(self):
        if self.check_logDateBased.isChecked():
            self.gui.appSettings['logDateBased'] = 1
        else:
            self.gui.appSettings['logDateBased'] = 0
# Sets whether logs are full json or very appreviated for reduced filesize.
    def updateLogJson(self):
        if self.check_logJson.isChecked():
            self.gui.appSettings['logJson'] = 1
        else:
            self.gui.appSettings['logJson'] = 0
# Sets whether all json messages are logged or just range_info messges.
    def updateLogRangeInfo(self):
        if self.check_logRangeInfo.isChecked():
            self.gui.appSettings['logRangeInfoOnly'] = 1
        else:
            self.gui.appSettings['logRangeInfoOnly'] = 0
# Sets whether all logging happens when radio is idle or just while ranging.
    def updateWhileIdle(self):
        if self.check_logIdle.isChecked():
            self.gui.appSettings['logWhileIdle'] = 1
        else:
            self.gui.appSettings['logWhileIdle'] = 0

# Get root directory for log storage.
    def getLogPath(self):
        if self.gui.platform == "linux":
            logPath = QFileDialog.getExistingDirectory(self, 'Choose Log Directory', str(self.gui.appSettings['logDirectory']), options=QFileDialog.Option.DontUseNativeDialog)
        else:
            logPath = QFileDialog.getExistingDirectory(self, 'Choose Log Directory', str(self.gui.appSettings['logDirectory']))
        if logPath != "":
            logPath = logPath + "/"
            self.dispLogDir.setText(str(logPath))
            self.gui.appSettings['logDirectory'] = logPath
# Get name for name based logging.
    def getLogFilename(self):
        logDir = Path(str(self.gui.appSettings['logDirectory']))
        if logDir.is_dir() == True:
            if self.gui.platform == "linux":
                logDir = QFileDialog.getSaveFileName(self, 'Choose Logfile Name', str(self.gui.appSettings['logDirectory']) + "/" + str(self.gui.appSettings['logFile']), "log (*.log)", options=QFileDialog.Option.DontUseNativeDialog)

            else:
                logDir = QFileDialog.getSaveFileName(self, 'Choose Logfile Name', str(self.gui.appSettings['logDirectory']) + "/" + str(self.gui.appSettings['logFile']), "log (*.log)")
        else:
            if self.gui.platform == "linux":
                logDir = QFileDialog.getSaveFileName(self, 'Choose Logfile Name', "./" + str(self.gui.appSettings['logFile']), "log (*.log)", options=QFileDialog.Option.DontUseNativeDialog)
            else:
                logDir = QFileDialog.getSaveFileName(self, 'Choose Logfile Name', "./" + str(self.gui.appSettings['logFile']), "log (*.log)")
        logName = logDir[0].split("/")
        if logDir[0] != '':
            logName = logName[len(logName) - 1]
            logDir = logDir[0].split(logName)
            logDir = logDir[0]
            self.dispLogName.setText(str(logName))
            self.gui.appSettings['logFile'] = logName
            self.dispLogDir.setText(str(logDir))
            self.gui.appSettings['logDirectory'] = logDir

    def initGUI(self):
        xStart = 190
        yStart = 10
        xBias = 0
        yBias = 0
        xBump = 160
        yBump = 80
        xWidth = 350
        yWidth = 50
        x = 0
        y = 0
        self.labelWindow = QLabel(self)
        self.labelWindow.resize(xWidth,yWidth)
        self.labelWindow.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWindow.setFont(self.guiFont.guiFont34)
        self.labelWindow.setText("Data Logging")
        self.labelWindow.setStyleSheet("QLabel {color: black;}")

        yStart = 70
        xStart = 0
        xBias = 0
        yBias = 0
        xBump = 220
        yBump = 60
        xWidth = 500
        yWidth = 40
        x = 1
        y = 0
        self.dispLogName = QLineEdit(self)
        self.dispLogName.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispLogName.setFont(self.guiFont.guiFont18)
        self.dispLogName.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispLogName.resize(xWidth,yWidth)
        self.dispLogName.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.dispLogName.setText(str(self.gui.appSettings['logFile']))
        self.dispLogName.editingFinished.connect(self.updateLogName)
        self.guiLogName = 1

        y = 1
        x = 1
        xWidth = 500
        self.dispLogDir = QLineEdit(self)
        self.dispLogDir.setStyleSheet("QLineEdit {background-color: lightyellow;}")
        self.dispLogDir.setFont(self.guiFont.guiFont18)
        self.dispLogDir.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.dispLogDir.resize(xWidth,yWidth)
        self.dispLogDir.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.dispLogDir.setText(str(self.gui.appSettings['logDirectory']))
        self.dispLogDir.editingFinished.connect(self.updateLogDirName)
        self.guiLogDir = 1

        xStart = 10
        xWidth = 200
        x = 0
        y = 0
        self.but_LogFile = QPushButton('Base LogFile Name', self)
        self.but_LogFile.setToolTip('Pick LogFile Name')
        self.but_LogFile.resize(xWidth, yWidth)
        self.but_LogFile.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_LogFile.setFont(self.guiFont.guiFont14)
        self.but_LogFile.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_LogFile.clicked.connect(self.getLogFilename)
        x = 0
        y = 1
        self.but_LogDir = QPushButton('Log Directory', self)
        self.but_LogDir.setToolTip('Pick LogFile Directory')
        self.but_LogDir.resize(xWidth, yWidth)
        self.but_LogDir.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_LogDir.setFont(self.guiFont.guiFont14)
        self.but_LogDir.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_LogDir.clicked.connect(self.getLogPath)
        yStart = 70
        yStart = 100
        xBias = 0
        yBias = 0
        xBump = 260
        yBump = 40
        xWidth = 500
        yWidth = 40
        x = 0
        y = 2
        self.check_logJson = QCheckBox('Log json', self)
        self.check_logJson.setToolTip('Log Full Messages')
        self.check_logJson.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.check_logJson.resize(200,40)
        self.check_logJson.setFont(self.guiFont.guiFont18)
        self.check_logJson.setStyleSheet(self.gui.checkBoxSheet)
        if self.gui.appSettings['logJson'] == 0:
            self.check_logJson.setChecked(False)
        else:
            self.check_logJson.setChecked(True)
        self.check_logJson.stateChanged.connect(self.updateLogJson)

        x = 0
        y = 3
        self.check_logRangeInfo = QCheckBox('Log RangeInfo Only', self)
        self.check_logRangeInfo.setToolTip('Log Only Range Info Messages')
        self.check_logRangeInfo.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.check_logRangeInfo.resize(300,40)
        self.check_logRangeInfo.setFont(self.guiFont.guiFont18)
        self.check_logRangeInfo.setStyleSheet(self.gui.checkBoxSheet)
        if self.gui.appSettings['logRangeInfoOnly'] == 0:
            self.check_logRangeInfo.setChecked(False)
        else:
            self.check_logRangeInfo.setChecked(True)
        self.check_logRangeInfo.stateChanged.connect(self.updateLogRangeInfo)

        x = 0
        y = 4
        self.check_logIdle = QCheckBox('Log While Idle', self)
        self.check_logIdle.setToolTip('Log data when radio idle as well as ranging')
        self.check_logIdle.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.check_logIdle.resize(300,40)
        self.check_logIdle.setFont(self.guiFont.guiFont18)
        self.check_logIdle.setStyleSheet(self.gui.checkBoxSheet)
        if self.gui.appSettings['logWhileIdle'] == 0:
            self.check_logIdle.setChecked(False)
        else:
            self.check_logIdle.setChecked(True)
        self.check_logIdle.stateChanged.connect(self.updateWhileIdle)

        x = 1
        y = 2
        self.check_logDateBased = QCheckBox('Time Based Naming', self)
        self.check_logDateBased.setToolTip('Generate Log Names based on radio ID and logging times')
        self.check_logDateBased.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.check_logDateBased.resize(300,40)
        self.check_logDateBased.setFont(self.guiFont.guiFont18)
        self.check_logDateBased.setStyleSheet(self.gui.checkBoxSheet)
        if self.gui.appSettings['logDateBased'] == 0:
            self.check_logDateBased.setChecked(False)
        else:
            self.check_logDateBased.setChecked(True)
        self.check_logDateBased.stateChanged.connect(self.updateLogDateBased)

        x = 1
        y = 3
        self.check_logSegmented = QCheckBox('Time Segmented', self)
        self.check_logSegmented.setToolTip('Break into multiple logs based on run time')
        self.check_logSegmented.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.check_logSegmented.resize(300,40)
        self.check_logSegmented.setFont(self.guiFont.guiFont18)
        self.check_logSegmented.setStyleSheet(self.gui.checkBoxSheet)
        if self.gui.appSettings['logSegmented'] == 0:
            self.check_logSegmented.setChecked(False)
        else:
            self.check_logSegmented.setChecked(True)
        self.check_logSegmented.stateChanged.connect(self.updateLogSegmented)

        x = 2
        y = 2
        xWidth = 160
        self.labelSegmentTime = QLabel(self)
        self.labelSegmentTime.resize(xWidth,yWidth)
        self.labelSegmentTime.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelSegmentTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelSegmentTime.setFont(self.guiFont.guiFont18)
        self.labelSegmentTime.setText("Seg Time(Sec)")
        self.labelSegmentTime.setStyleSheet("QLabel {color: GhostWhite;}")
        self.dispSegmentTime = QLineEdit(self)
        self.dispSegmentTime.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        self.dispSegmentTime.setFont(self.guiFont.guiFont18)
        self.dispSegmentTime.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias + 40)
        self.dispSegmentTime.resize(xWidth,yWidth)
        self.dispSegmentTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispSegmentTime.setText(str(self.gui.appSettings['segmentTime']))
        self.dispSegmentTime.editingFinished.connect(self.updateLogSegmented)
        self.guiSegmentTime = 1

        xStart = 265
        yStart = 255
        xBias = 0
        yBias = 0
        xBump = 220
        yBump = 60
        xWidth = 200
        yWidth = 40
        x = 0
        y = 0
        self.labelLoggingStatus = QLabel(self)
        self.labelLoggingStatus.resize(xWidth,yWidth)
        self.labelLoggingStatus.move(x*xBump + xStart + xBias, yStart + y*yBump + yBias)
        self.labelLoggingStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelLoggingStatus.setFont(self.guiFont.guiFont20)
        self.labelLoggingStatus.setText("Logging Status")
        self.labelLoggingStatus.setStyleSheet("QLabel {color: black;}")
        yStart = 295
        self.but_enableLogging = QPushButton('Enable Logging', self)
        self.but_enableLogging.setToolTip('Toggle Data Logging')
        self.but_enableLogging.resize(xWidth, yWidth)
        self.but_enableLogging.setFont(self.guiFont.guiFont20)
        self.but_enableLogging.move(x*xBump + xBias + xStart, y*yBump + yBias + yStart)
        self.but_enableLogging.clicked.connect(self.toggleLogging)
        if self.gui.appSettings['enableLogging'] == 1:
            self.but_enableLogging.setText("Logging Enabled")
            self.but_enableLogging.setStyleSheet("QPushButton {background-color: coral;}")
        else:
            self.but_enableLogging.setText("Logging Disabled")
            self.but_enableLogging.setStyleSheet(self.gui.buttonSheetBlue)

# Class for large range window that can more easily be seen from a distance.
class windowNetwork(QWidget):
    def __init__(self, gui):
        super().__init__()
        self.setGeometry(10, 10, 975, 60)
        self.setMinimumWidth(975)
        self.setWindowTitle("Radio Network Settings")
        self.gui = gui
        # self.setStyleSheet("QWidget {background-color: rgb(200,200,200);}")
        self.setStyleSheet(self.gui.windowSheet)
        self.guiFont = guiFonts()
        self.layoutSlots = None
        self.layoutStats = None
        self.layoutTop = None
        self.layoutNetRanges = None
        self.layoutNetStats = None
        self.layoutNetRangePlots = None
        self.slotMap = None
        self.startField = 2
        self.netPlot1 = []
        self.netPlot2 = []
        self.netPlotT = []
        self.netPlotB = []
        self.netRangeArray = []
        self.netRangeFilteredArray = []
        self.netPowerArray = []
        self.netMaxNoiseArray = []
        self.netStdNoiseArray = []
        self.netXArray = []
        self.netRangeCount = 0
        self.netYScale = 0
        self.netGuiTimer = QTimer()
        self.netGuiTimer.setInterval(1000)
        self.netGuiTimer.timeout.connect(self.netGuiPacketUpdate)
        self.netDispSlot = 0
        self.netGuiUpdate = 1
        self.savedNodeId = ""
        self.localSlots = []
        self.localSlotFirst = 0     # First and last slot index that the locally connector radio is the requester for.
        self.localSlotLast = 0      # Used for GUI update timing.

    def displayWindow(self):
        if self.layoutSlots == None:
            self.initGUI()
            self.buttonHandlerGetMap()
        self.show()
        self.resize(self.width(),self.sizeHint().height())
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowNetwork.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def netGuiPacketUpdate(self):
        self.netGuiUpdate = 1

    def processRange(self,slot,packet):
        # Data arrays initialized by getMap which is called when network window is opened
        self.layoutNetRanges.itemAt(slot+1).itemAt(0).widget().setText(str(packet['RANGE_INFO']['requesterId']))
        self.layoutNetRanges.itemAt(slot+1).itemAt(1).widget().setText(str(packet['RANGE_INFO']['responderId']))
        self.layoutNetRanges.itemAt(slot+1).itemAt(5).widget().setText(str(packet['RANGE_INFO']['precisionRangeM']))
        self.layoutNetRanges.itemAt(slot+1).itemAt(6).widget().setText("%.1f" % (packet['RANGE_INFO']['rxPower']))
        if packet['RANGE_INFO']['requesterId'] == self.gui.radioReqNodeID:
            # This sets the update rate of the GUI so it doesn't bog down the app with constant updates
            if self.netGuiUpdate == 1:
                self.netGuiTimer.stop()
                if slot == self.localSlots[self.netDispSlot][0]:
                    self.netDispSlot = self.netDispSlot + 1
                    if self.netDispSlot > (len(self.localSlots) - 1):
                        self.netDispSlot = 0
                    if packet['RANGE_INFO']['rangeStatus'] == 0 and packet['RANGE_INFO']['precisionRangeM'] != 0.0:
                        self.netGuiUpdate = 0
                        self.gui.guiPacketUpdates(packet)
                    # else:
                        # print("Process Range Error")
                    self.netGuiTimer.start()

            # Only update X axis array and rangecount once when first slot in line hits
            if slot == self.localSlotFirst: #0:
                self.netRangeCount = self.netRangeCount + 1
                self.netXArray.append(self.netRangeCount) # only increment x when new slot 0 to keep arrays same size
                # print("XArrayLen", len(self.netXArray))

            # This section updates the arrays and only starts when X Array is positive (saw first slot)
            #   so that it doesn't start on any slot. Waits for the beginning to avoid starting mid-slotmap.
            if len(self.netXArray) > 0:  # only start appending once Xarray sees first slot and starts advancing
                # if range was successful
                if packet['RANGE_INFO']['rangeStatus'] == 0 and packet['RANGE_INFO']['precisionRangeM'] != 0.0:
                    self.gui.checkChartRange(packet)
                    # Condition RX power so that it doesn't add/plot bogus results
                    rxPower = str(packet['RANGE_INFO']['rxPower'])
                    if rxPower != "-Infinity" and rxPower != "-inf":
                        rxPower = round(float(packet['RANGE_INFO']['rxPower']))
                    else:
                        rxPower = -120
                    # Store the current range info in the array for the current slot, which should only be local slots
                    try:
                        self.netRangeArray[slot].append(float(packet['RANGE_INFO']['precisionRangeM']))
                    except:
                        print("a: Slot, ArraySize:", slot, len(self.netRangeArray))
                    try:
                        # THIS NEEDS TO CHANGE TO FILTERED WHEN API SUPPORTS IT
                        self.netRangeFilteredArray[slot].append(float(packet['RANGE_INFO']['filteredRangeM']))
                    except Exception as e:
                        print(e)
                        print(packet)
                        print("b: Slot, ArraySize:", slot, len(self.netRangeFilteredArray))
                    self.netPowerArray[slot].append(rxPower)
                    self.netMaxNoiseArray[slot].append(int(packet['RANGE_INFO']['maxNoise']))
                    self.netStdNoiseArray[slot].append(int(packet['RANGE_INFO']['stdNoise']))
                # if not a successful range
                else:
                    # print("Process Range Error 2")
                    if self.gui.check_plotDrops.isChecked():
                        self.netRangeArray[slot].append(float(packet['RANGE_INFO']['precisionRangeM']))
                        self.netRangeFilteredArray[slot].append(float(packet['RANGE_INFO']['filteredRangeM']))
                        self.netPowerArray[slot].append(rxPower)
                        self.netMaxNoiseArray[slot].append(int(packet['RANGE_INFO']['maxNoise']))
                        self.netStdNoiseArray[slot].append(int(packet['RANGE_INFO']['stdNoise']))
                    else:
                        if len(self.netRangeArray[slot]) > 0: #make sure we have a point to copy
                            self.netRangeArray[slot].append(self.netRangeArray[slot][len(self.netRangeArray[slot])-1])  # copy last data point
                            self.netRangeFilteredArray[slot].append(self.netRangeFilteredArray[slot][len(self.netRangeFilteredArray[slot])-1])
                            self.netPowerArray[slot].append(self.netPowerArray[slot][len(self.netPowerArray[slot])-1])
                            self.netMaxNoiseArray[slot].append(self.netMaxNoiseArray[slot][len(self.netMaxNoiseArray[slot])-1])
                            self.netStdNoiseArray[slot].append(self.netStdNoiseArray[slot][len(self.netStdNoiseArray[slot])-1])
                        else:  #if not, make up a point
                            self.netRangeArray[slot].append(0)
                            self.netRangeFilteredArray[slot].append(0)
                            self.netPowerArray[slot].append(-120)
                            self.netMaxNoiseArray[slot].append(1100)
                            self.netStdNoiseArray[slot].append(60)
        # update plot when last slot is done
        if slot == self.localSlotLast and len(self.netRangeArray[self.localSlots[0][0]]) > 0:
            if len(self.netRangeArray[0]) > int(self.gui.appSettings['memoryDepth']):
                for i in range(len(self.netRangeArray)):
                    self.netRangeArray[i] = self.netRangeArray[i][1:]
                    self.netRangeFilteredArray[i] = self.netRangeFilteredArray[i][1:]
                    self.netPowerArray[i] = self.netPowerArray[i][1:]
                    self.netMaxNoiseArray[i] = self.netMaxNoiseArray[i][1:]
                    self.netStdNoiseArray[i] = self.netStdNoiseArray[i][1:]
                self.netXArray = self.netXArray[1:]
            self.gui.plotData()

    def initGUI(self):
        self.layoutTop = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.netSlotsTab(), "SlotMap")
        tabs.addTab(self.netRangesTab(), "Ranges")
        # tabs.addTab(self.netPlottingTab(), "Graphs")
        tabs.addTab(self.netStatsTab(), "Stats")
        self.layoutTop.addWidget(tabs)
        but_networkRunToggle = QPushButton("Start Network")
        but_networkRunToggle.setStyleSheet(self.gui.buttonSheetBlue)
        but_networkRunToggle.clicked.connect(self.buttonHandlerNetworkToggle)
        self.layoutTop.addWidget(but_networkRunToggle,1)
        self.setLayout(self.layoutTop)

    def netSlotsTab(self):
        self.slotTab = QWidget()
        self.layoutSlots = QVBoxLayout()
        controlLine = self.makeControlLine()
        self.layoutSlots.addLayout(controlLine)
        slotLabels = self.makeSlotLabels()
        self.layoutSlots.addLayout(slotLabels)
        slot = self.makeSlotLine()
        self.layoutSlots.addLayout(slot)
        self.layoutSlots.setContentsMargins(2,2,2,2)
        self.layoutSlots.setSpacing(2)
        self.slotTab.setLayout(self.layoutSlots)
        return self.slotTab

    def netRangesTab(self):
        tab = QWidget()
        self.layoutNetRanges = QVBoxLayout()
        rangeLabels = self.makeRangeLabels()
        self.layoutNetRanges.addLayout(rangeLabels)
        tab.setLayout(self.layoutNetRanges)
        return tab

    def netPlottingTab(self):
        tab = QWidget()
        self.layoutNetRangePlots = QVBoxLayout()
        tab.setLayout(self.layoutNetRangePlots)
        return tab

    def netStatsTab(self):
        tab = QWidget()
        self.layoutNetStats = QVBoxLayout()
        tab.setLayout(self.layoutNetStats)
        return tab

    def makeControlLine(self):
        controlLine = QHBoxLayout()
        height = 30
        width = 120
        # Button to send slotmap to radio
        self.but_slotMapSetMap = QPushButton("Set Map")
        self.but_slotMapSetMap.setFixedSize(width,height)
        self.but_slotMapSetMap.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_slotMapSetMap.clicked.connect(self.buttonHandlerSetMap)
        # Button to get slotmap from radio
        but_slotMapGetMap = QPushButton("Get Map")
        but_slotMapGetMap.setFixedSize(width,height)
        but_slotMapGetMap.setStyleSheet(self.gui.buttonSheetBlue)
        but_slotMapGetMap.clicked.connect(self.buttonHandlerGetMap)
        # Button to load slotmap from disk
        but_slotMapLoad = QPushButton("Load Map")
        but_slotMapLoad.setFixedSize(width,height)
        but_slotMapLoad.setStyleSheet(self.gui.buttonSheetBlue)
        but_slotMapLoad.clicked.connect(self.buttonHandlerLoadMap)
        # Button to clear slotmap
        but_slotMapClear = QPushButton("New Map")
        but_slotMapClear.setFixedSize(width,height)
        but_slotMapClear.setStyleSheet(self.gui.buttonSheetBlue)
        but_slotMapClear.clicked.connect(self.buttonHandlerClearMap)
        # Button to save slotmap to disk
        but_slotMapSave = QPushButton("Save Map")
        but_slotMapSave.setFixedSize(width,height)
        but_slotMapSave.setStyleSheet(self.gui.buttonSheetBlue)
        but_slotMapSave.clicked.connect(self.buttonHandlerSaveMap)
        # Button to get network stats from the radio
        but_networkStats = QPushButton("Show Stats")
        but_networkStats.setFixedSize(width,height)
        but_networkStats.setStyleSheet(self.gui.buttonSheetBlue)
        but_networkStats.clicked.connect(self.buttonHandlerShowStats)
        controlLine.addWidget(self.but_slotMapSetMap,1)
        controlLine.addWidget(but_slotMapGetMap,1)
        controlLine.addWidget(but_slotMapLoad,1)
        controlLine.addWidget(but_slotMapClear,1)
        controlLine.addWidget(but_slotMapSave,1)
        controlLine.addWidget(but_networkStats,1)
        return controlLine

    def makeSlotLabels(self):
        layoutSlotLabel = QHBoxLayout()
        height = 30
        width = 80
        # Labels for slot fields
        slot = QLabel("Slot")
        slot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slot.setFixedSize(width,height)
        layoutSlotLabel.addWidget(slot,0)
        slotType = QLabel("Type")
        slotType.setFixedSize(width,height)
        slotType.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(slotType,0)
        configID = QLabel("Config ID")
        configID.setFixedSize(width,height)
        configID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(configID,0)
        ownerID = QLabel("OwnerID")
        ownerID.setFixedSize(width,height)
        ownerID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(ownerID,0)
        targetID = QLabel("Target ID")
        targetID.setFixedSize(width,height)
        targetID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(targetID,0)
        period = QLabel("Period")
        period.setFixedSize(width,height)
        period.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(period,0)
        maxData = QLabel("MaxData")
        maxData.setFixedSize(width,height)
        maxData.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(maxData,0)
        orderUp = QLabel("Order")
        orderUp.setFixedSize(width,height)
        orderUp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(orderUp,0)
        orderDown = QLabel("Order")
        orderDown.setFixedSize(width,height)
        orderDown.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(orderDown,0)
        numberAdd = QLabel("Number")
        numberAdd.setFixedSize(width,height)
        numberAdd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(numberAdd,0)
        numberDel = QLabel("Number")
        numberDel.setFixedSize(width,height)
        numberDel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutSlotLabel.addWidget(numberDel,0)
        return layoutSlotLabel

    def makeSlotLine(self):
        # Define a slot entry line
        if self.gui.connectedRequester == 1:
            base = self.gui.radioReqNodeID + 1
        else:
            base = 100
        height = 30
        width = 80
        layoutSlotData = QHBoxLayout()
        # Slot Number Field
        # slot = len(self.layoutSlots)-self.startField
        # idColor = self.gui.pen[slot].color().getRgb()
        # idColor = idColor[0:3]
        # idColor = "QLineEdit {background-color: rgb" + str(idColor) + ";}"
        slotNum = QLineEdit(str(len(self.layoutSlots)-self.startField))
        slotNum.setStyleSheet(self.gui.lineSheet)
        slotNum.setReadOnly(True)
        slotNum.setFixedSize(width,height)
        # slotNum.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # slotNum.setStyleSheet(idColor)
        # What type of slot is it?
        slotType = QComboBox(self)
        slotType.addItems(["Range", "Data"])
        slotType.setFixedSize(width,height)
        slotType.setStyleSheet(self.gui.dropSheetGray)
        # Which configuration does this slot use?
        slotConfig = QLineEdit("0")
        slotConfig.setFixedSize(width,height)
        slotConfig.setStyleSheet(self.gui.lineSheet)
        # Who is the requester for this slot?
        slotReq = QLineEdit(str(self.gui.radioReqNodeID))
        slotReq.setFixedSize(width,height)
        slotReq.setStyleSheet(self.gui.lineSheet)
        # Who are we ranging to?
        slotResp = QLineEdit(str(base + len(self.layoutSlots) - self.startField))
        slotResp.setFixedSize(width,height)
        slotResp.setStyleSheet(self.gui.lineSheet)
        # How long does this slow have in table?
        slotPeriod = QLineEdit("20")
        slotPeriod.setFixedSize(width,height)
        slotPeriod.setStyleSheet(self.gui.lineSheet)
        # Maximum size of data allowed in this slot
        slotDataMax = QLineEdit("100")
        slotDataMax.setFixedSize(width,height)
        slotDataMax.setStyleSheet(self.gui.lineSheet)
        # Button to move slot down
        but_slotUp = QPushButton("Up")
        but_slotUp.setFixedSize(width,height)
        but_slotUp.setStyleSheet(self.gui.buttonSheetGray)
        but_slotUp.clicked.connect(self.buttonHandlerUp)
        # Button to move slot down
        but_slotDown = QPushButton("Down")
        but_slotDown.setFixedSize(width,height)
        but_slotDown.setStyleSheet(self.gui.buttonSheetGray)
        but_slotDown.setObjectName(str(len(self.layoutSlots)))
        but_slotDown.clicked.connect(self.buttonHandlerDown)
        # Button to move slot down
        but_slotAdd = QPushButton("Add")
        but_slotAdd.setFixedSize(width,height)
        but_slotAdd.setStyleSheet(self.gui.buttonSheetGray)
        but_slotAdd.clicked.connect(self.buttonHandlerAdd)
        # Button to move slot down
        but_slotDel = QPushButton("Del")
        but_slotDel.setFixedSize(width,height)
        but_slotDel.setStyleSheet(self.gui.buttonSheetGray)
        but_slotDel.setObjectName(str(len(self.layoutSlots)))
        but_slotDel.clicked.connect(self.buttonHandlerDel)
        #Add them all to the horizontal line
        layoutSlotData.addWidget(slotNum,0)
        layoutSlotData.addWidget(slotType,0)
        layoutSlotData.addWidget(slotConfig,0)
        layoutSlotData.addWidget(slotReq,0)
        layoutSlotData.addWidget(slotResp,0)
        layoutSlotData.addWidget(slotPeriod,0)
        layoutSlotData.addWidget(slotDataMax,0)
        layoutSlotData.addWidget(but_slotUp,0)
        layoutSlotData.addWidget(but_slotDown,0)
        layoutSlotData.addWidget(but_slotAdd,0)
        layoutSlotData.addWidget(but_slotDel,0)
        return layoutSlotData

    def makeRangeLabels(self):
        height = 30
        width = 80
        layoutRangeLabel = QHBoxLayout()
        # Labels for range fields
        requester = QLabel("Requester")
        requester.setFixedSize(width,height)
        requester.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(requester,1)
        responder = QLabel("Responder")
        responder.setFixedSize(width,height)
        responder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(responder,1)
        averaging = QLabel("Averaging")
        averaging.setFixedSize(width,height)
        averaging.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(averaging,1)
        rangeType = QLabel("Range Type")
        rangeType.setFixedSize(width,height)
        rangeType.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(rangeType,1)
        packetType = QLabel("Packet Type")
        packetType.setFixedSize(width,height)
        packetType.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(packetType,1)
        range = QLabel("Range")
        range.setFixedSize(width,height)
        range.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(range,1)
        signal = QLabel("Signal")
        signal.setFixedSize(width,height)
        signal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(signal,1)
        lastHeard = QLabel("Last Heard")
        lastHeard.setFixedSize(width,height)
        lastHeard.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(lastHeard,1)
        lastRange = QLabel("Last Range")
        lastRange.setFixedSize(width,height)
        lastRange.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(lastRange,1)
        success = QLabel("Success %")
        success.setFixedSize(width,height)
        success.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutRangeLabel.addWidget(success,1)
        return layoutRangeLabel

    def makeRangeLine(self, idColor):
        height = 30
        width = 80
        # Define a range entry line
        layoutRangeData = QHBoxLayout()
        # Requester nodeID Field
        requester = QLineEdit("")
        requester.setFixedSize(width,height)
        requester.setReadOnly(True)
        requester.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Responder nodeID Field
        responder = QLineEdit("")
        responder.setFixedSize(width,height)
        responder.setReadOnly(True)
        responder.setStyleSheet(idColor)
        # responder.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Averaging level for display
        averaging = QComboBox(self)
        averaging.setFixedSize(width,height)
        # averaging.addItems(["1", "2", "4", "8", "16", "32"])
        averaging.addItems(["1"])
        # Type of range should be displayed
        rangeType = QComboBox(self)
        rangeType.setFixedSize(width,height)
        rangeType.addItems(["Precision"])
        # What type of packet last came in
        packetType = QLineEdit("")
        packetType.setFixedSize(width,height)
        packetType.setReadOnly(True)
        packetType.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Actual range data
        rangeData = QLineEdit("")
        rangeData.setFixedSize(width,height)
        rangeData.setReadOnly(True)
        rangeData.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Signal strength
        signalData = QLineEdit("")
        signalData.setFixedSize(width,height)
        signalData.setReadOnly(True)
        signalData.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Time since radio last year from?
        lastHeard = QLineEdit("")
        lastHeard.setFixedSize(width,height)
        lastHeard.setReadOnly(True)
        lastHeard.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Last range received
        lastRange = QLineEdit("")
        lastRange.setFixedSize(width,height)
        lastRange.setReadOnly(True)
        lastRange.setStyleSheet("QLineEdit {background-color: lightgrey;}")
        # Success rate
        successRate = QLineEdit("")
        successRate.setFixedSize(width,height)
        successRate.setReadOnly(True)
        successRate.setStyleSheet("QLineEdit {background-color: lightgrey;}")

        #Add them all to the horizontal line
        layoutRangeData.addWidget(requester,1)
        layoutRangeData.addWidget(responder,1)
        layoutRangeData.addWidget(averaging,1)
        layoutRangeData.addWidget(rangeType,1)
        layoutRangeData.addWidget(packetType,1)
        layoutRangeData.addWidget(rangeData,1)
        layoutRangeData.addWidget(signalData,1)
        layoutRangeData.addWidget(lastHeard,1)
        layoutRangeData.addWidget(lastRange,1)
        layoutRangeData.addWidget(successRate,1)
        return layoutRangeData

    def buttonHandlerSetMap(self):
        if self.gui.radioMode == "networking":
            self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")
            tmp = "== Must stop network before setting new slotmap! ==\n"
            self.gui.updateConsole(tmp)
        else:
            # self.updateTabs()
            # print("set\n",self.slotMap)
            # print("totalTime", self.slotMapTime)
            if self.gui.connectedRequester == 1:
                self.makeMap()
                status = self.gui.radioReq.API.network_SetSlotMap_Request(self.gui.appSettings['reqRadio'], self.slotMap,1)
                # print("status:", status)
                text = "Slotmap sent to radio\n"
                self.gui.updateConsole(text)
                self.buttonHandlerGetMap()
            else:
                text = "Need to connect to a primary radio@!\n"
                self.gui.updateConsole(text)
                self.slotMap = [{"slotIdx":0,"slotType":"SLOT_RANGE","configId":0,"ownerId":100,"targetId":101,"period":20,"maxUserData":10}]
                self.populateMap()
            self.but_slotMapSetMap.setStyleSheet(self.gui.buttonSheetBlue)


    def buttonHandlerGetMap(self):
        if self.gui.connectedRequester == 1:
            status, self.slotMap, addr = self.gui.radioReq.API.network_GetSlotMap_Request(self.gui.appSettings['reqRadio'])
            self.slotMap = self.slotMap['NETWORKING_GET_SLOT_MAP_CONFIRM']['slotMap']
        else:
            self.slotMap = []
            text = "Need to connect to a primary radio@!\n"
            self.gui.updateConsole(text)
        # print("getMapStatus", status)
        # print(self.slotMap)
        if self.slotMap:
            self.clearMap()
            self.populateMap()
            text = "Slotmap retreived from radio\n"
            self.gui.updateConsole(text)
        else:
            print("No slotmap found, generating default")
            self.buttonHandlerClearMap()
            # self.buttonHandlerSetMap()
        # print("Get\n",self.slotMap)
        self.resetDataArrays()
        self.updateDestMenu()
        self.updateTabs()
        self.but_slotMapSetMap.setStyleSheet(self.gui.buttonSheetBlue)

    def resetDataArrays(self):
        self.gui.plotYT = []
        self.gui.plotYB = []
        self.gui.plotX = []
        self.gui.rangeMax = 0
        self.gui.rangeMin = 1000000
        self.gui.powerMax = -200
        self.gui.powerMin = 0
        self.gui.stdNoiseMax = -10
        self.gui.stdNoiseMin = 20000
        self.gui.maxNoiseMax = -10
        self.gui.maxNoiseMin = 20000
        self.netRangeCount = 0
        self.netYScale = 0
        self.netDispSlot = 0
        self.gui.chartData1.setData(self.gui.plotX, self.gui.plotYT)
        self.gui.chartData2.setData(self.gui.plotX, self.gui.plotYT)
        self.gui.chartDataT.setData(self.gui.plotX, self.gui.plotYT)
        self.gui.chartDataB.setData(self.gui.plotX, self.gui.plotYB)
        self.netXArray = []
        for i in range(len(self.netRangeArray)):
            self.netRangeArray[i] = []
            self.netRangeFilteredArray[i] = []
            self.netPowerArray[i] = []
            self.netMaxNoiseArray[i] = []
            self.netStdNoiseArray[i] = []
            self.netPlot1[i].setData(self.netXArray, self.netRangeArray[i])
            self.netPlot2[i].setData(self.netXArray, self.netRangeFilteredArray[i])
            self.netPlotT[i].setData(self.netXArray, self.netRangeArray[i])
            self.netPlotB[i].setData(self.netXArray, self.netRangeArray[i])
        self.localSlotFirst = -1
        self.localSlotLast = -1
        self.localSlots = []
        self.netRangeCount = 0
        for i,slot in enumerate(self.slotMap):
            # if slot['ownerId'] == self.gui.radioReqNodeID:
                if slot["ownerId"] == self.gui.radioReqNodeID:
                    self.localSlots.append([slot["slotIdx"],slot["targetId"]])
                plotX = []
                # T = top chart, B = Bottom chart
                plotYT = []
                plotYB = []
                rangeArray = []
                rangeFilteredArray = []
                powerArray = []
                maxNoiseArray = []
                stdNoiseArray = []
                self.netPlot1.append(self.gui.dataWindow.plot(plotX, plotYT, pen=self.gui.pen[i]))
                self.netPlot2.append(self.gui.dataWindow.plot(plotX, plotYT, pen=self.gui.pen[18]))
                self.netPlotT.append(self.gui.dataWindowT.plot(plotX, plotYT, pen=self.gui.pen[i]))
                self.netPlotB.append(self.gui.dataWindowB.plot(plotX, plotYB, pen=self.gui.pen[i]))
                # print(i, self.gui.pen[i].color().getRgb())
                self.netRangeArray.append(rangeArray)
                self.netRangeFilteredArray.append(rangeFilteredArray)
                self.netPowerArray.append(powerArray)
                self.netMaxNoiseArray.append(maxNoiseArray)
                self.netStdNoiseArray.append(stdNoiseArray)
        if len(self.localSlots) > 0:
            self.localSlotFirst = self.localSlots[0][0]
            self.localSlotLast = self.localSlots[len(self.localSlots)-1][0]

    def buttonHandlerShowStats(self):
        status, stats, addr = self.gui.radioReq.API.network_Stats_Request(self.gui.appSettings['reqRadio'])
        print(stats)

    def buttonHandlerLoadMap(self):
        self.clearMap()
        if self.gui.platform == "linux":
            filename = QFileDialog.getOpenFileName(self, 'Open SlotMap File', "./slotMaps/slotMap.map", "map (*.map)", options=QFileDialog.Option.DontUseNativeDialog)
        else:
            filename = QFileDialog.getOpenFileName(self, 'Open SlotMap File', "./slotMaps/slotMap.map", "map (*.map)")
        filename = filename[0]
        f = open(filename, "r")
        self.slotMap = loads(f.read())
        self.populateMap()
        self.updateTabs()
        text = "Slotmap loaded\n"
        self.gui.updateConsole(text)
        self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")

    def buttonHandlerClearMap(self):
        self.clearMap()
        slotLine = self.makeSlotLine()
        self.layoutSlots.addLayout(slotLine)
        self.resize(self.width(),self.sizeHint().height())
        text = "Slotmap Cleared\n"
        self.gui.updateConsole(text)
        self.updateTabs()
        self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")

    def buttonHandlerSaveMap(self):
        self.makeMap()
        if self.gui.platform == "linux":
            saveName = QFileDialog.getSaveFileName(self, 'Choose SlotMap Name', "./slotMaps/slotMap.map","map (*.map)", options=QFileDialog.Option.DontUseNativeDialog)
        else:
            saveName = QFileDialog.getSaveFileName(self, 'Choose SlotMap Name', "./slotMaps/slotMap.map","map (*.map)")
        saveName = saveName[0]
        try:
            f = open(saveName, "w")
            f.write(dumps(self.slotMap))
            f.close()
            text = "Slotmap save successful\n"
            self.gui.updateConsole(text)
        except:
            print("== Invalid filename, save aborted")
            text = "== Invalid filename, save aborted\n"
            self.gui.updateConsole(text)

    def buttonHandlerNetworkToggle(self):
        if self.gui.connectedRequester == 1:
            self.gui.radioStateReq,addr = self.gui.radioReq.API.radio_GetState_Request(self.gui.appSettings['reqRadio'])
            if self.gui.radioMode == 'idle':
                self.savedNodeId = self.gui.dispRespID.text() # network changes this while running, so save value before network start
                status = self.gui.radioRanging.rangingSetup('networking')
                if status == True:
                    # setup the networking state
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['state'] = "RADIO_STATE_NETWORKING"
                    self.layoutTop.itemAt(len(self.layoutTop)-1).widget().setText("Stop Network")
                    self.layoutTop.itemAt(len(self.layoutTop)-1).widget().setStyleSheet("QPushButton {background-color: coral; color: black;}")
                    self.gui.radioMode = 'networking'
                    self.gui.radioCheckTimer.stop()
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['flags']  = ""
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['persistFlag'] = 1
                    self.gui.radioReq.API.radio_SetState_Request(self.gui.appSettings['reqRadio'],self.gui.radioStateReq)
                    self.gui.windowDataTransfer.radioData.reqMsgTimer.stop()
                    self.gui.windowDataTransfer.radioData.respMsgTimer.stop()
                    self.updateDestMenu()
                    self.resetDataArrays()
                    self.gui.checkChartRange(None)
                    # clear the stale messages
                    for i in self.gui.radioReq.messageQueues:
                        while not self.gui.radioReq.messageQueues[i].empty():
                            dump = self.gui.radioReq.messageQueues[i].get()
                    self.gui.windowDataTransfer.radioData.networkConfirmQueue = []
                    text = "\n==============\n Network Starting\n"
                    self.gui.updateConsole(text)
                    self.gui.radioRanging.networkTimer.start()
                    self.netGuiTimer.start()
                else:
                    text = "Could not connect to requester radio, check cables and IP addresses.\n"
                    self.gui.updateConsole(text)
                    self.gui.radioMode = 'idle'
                    self.gui.radioCheckTimer.start()
            else:
                if self.gui.radioMode == 'networking':
                    # self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['state'] = "RADIO_STATE_IDLE"
                    self.gui.dispRespID.setText(str(self.savedNodeId))
                    self.gui.dispRespID.setStyleSheet("QLineEdit {background-color: lightgreen;}")
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['state'] = "RADIO_STATE_RANGING"
                    self.layoutTop.itemAt(len(self.layoutTop)-1).widget().setText("Start Network")
                    self.layoutTop.itemAt(len(self.layoutTop)-1).widget().setStyleSheet(self.gui.buttonSheetBlue)
                    self.gui.radioMode = 'idle'
                    self.gui.radioCheckTimer.start()
                    self.gui.radioRanging.networkTimer.stop()
                    # self.gui.guiUpdateTimer.stop()
                    self.netGuiTimer.stop()
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['flags']  = ""
                    self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['persistFlag'] = 1
                    self.gui.radioReq.API.radio_SetState_Request(self.gui.appSettings['reqRadio'],self.gui.radioStateReq)
                    if self.gui.connectedResponder == 1:
                        self.gui.windowDataTransfer.radioData.respMsgTimer.start()
                    if self.gui.connectedRequester == 1:
                        self.gui.windowDataTransfer.radioData.reqMsgTimer.start()
                    text = "\n==============\n Network Stopping\n"
                    self.gui.updateConsole(text)
                else:
                    if self.gui.radioMode == 'ranging':
                        text = "=====\nRadio is in Ranging Mode.\n  Stop ranging before starting network\n=====\n"
                        self.gui.updateConsole(text)

    def buttonHandlerUp(self):
        name = self.sender()
        row,col = self.findLine(name)
        moveSlotNum = row - 2
        if moveSlotNum > 0:
            tmp = self.slotMap[moveSlotNum - 1]
            self.slotMap[moveSlotNum - 1] = self.slotMap[moveSlotNum]
            self.slotMap[moveSlotNum] = tmp
            self.slotMap[moveSlotNum - 1]['slotIdx'] = moveSlotNum - 1
            self.slotMap[moveSlotNum]['slotIdx'] = moveSlotNum
            self.clearMap()
            self.populateMap()
            self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")
        else:
            print("Already at the top, can't move up")

    def buttonHandlerDown(self):
        # for k in range(len(self.layoutSlots)):
        #     print(self.layoutSlots.itemAt(k))
        name = self.sender()
        row,col = self.findLine(name)
        moveSlotNum = row - 2
        if moveSlotNum < (len(self.slotMap) - 1):
            tmp = self.slotMap[moveSlotNum + 1]
            self.slotMap[moveSlotNum + 1] = self.slotMap[moveSlotNum]
            self.slotMap[moveSlotNum] = tmp
            self.slotMap[moveSlotNum + 1]['slotIdx'] = moveSlotNum + 1
            self.slotMap[moveSlotNum]['slotIdx'] = moveSlotNum
            self.clearMap()
            self.populateMap()
            self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")
        else:
            print("Already at the bottom, can't move down")

    def buttonHandlerAdd(self):
        slot = self.makeSlotLine()
        self.layoutSlots.addLayout(slot)
        self.makeMap()
        self.clearMap()
        self.populateMap()
        self.updateTabs()
        self.resize(self.width(),self.sizeHint().height())
        self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")

    def buttonHandlerDel(self):
        if len(self.layoutSlots) > self.startField + 1:
            name = self.sender()
            # print(name.objectName())
            row,col = self.findLine(name)
            # print(f"Fount at row {row} and column {col}")
            slotLine = self.layoutSlots.itemAt(row)
            self.deleteLayoutLine(slotLine)
            self.layoutSlots.removeItem(self.layoutSlots.itemAt(row))
            slotLine.deleteLater()
            for k in range(self.startField,len(self.layoutSlots)):
                slotLine = self.layoutSlots.itemAt(k)
                slotNum = slotLine.itemAt(0).widget()
                slotNum.setText(str(k - self.startField))  # because of startField
            self.makeMap()
            self.clearMap()
            self.populateMap()
            self.updateTabs()
            self.slotTab.adjustSize()
            self.resize(self.width(),self.sizeHint().height())
            self.but_slotMapSetMap.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")
        else:
            print("Can't delete last row")

    def updateDestMenu(self):
        nodes = []
        for i in range(len(self.slotMap)):
            if self.slotMap[i]["ownerId"] != self.gui.radioReqNodeID:
                if str(self.slotMap[i]["ownerId"]) not in nodes:
                    nodes.append(str(self.slotMap[i]['ownerId']))
            if str(self.slotMap[i]['targetId']) not in nodes:
                nodes.append(str(self.slotMap[i]['targetId']))
        self.gui.windowDataTransfer.dropMenuDestination.clear()
        self.gui.windowDataTransfer.dropMenuDestination.addItems(nodes)

    def updateTabs(self):
        self.clearRangeTab()
        self.clearStatsTab()
        self.clearGraphTab()
        self.buildRangeTab()
        self.buildStatsTab()

    def findLine(self, object):
        for k in range(1,len(self.layoutSlots)):
            slotLine = self.layoutSlots.itemAt(k)
            for j in range(len(slotLine)):
                widget = slotLine.itemAt(j).widget()
                if widget == object:
                    return k,j

    def deleteLayoutLine(self, layoutLine):
        for k in range(len(layoutLine)):
            widget = layoutLine.itemAt(0).widget()
            layoutLine.removeWidget(widget)
            widget.deleteLater()

    def clearMap(self):
        self.resize(self.width(),60)
        for k in range(self.startField, len(self.layoutSlots)):
            slotLine = self.layoutSlots.itemAt(self.startField)
            self.deleteLayoutLine(slotLine)
            self.layoutSlots.removeItem(self.layoutSlots.itemAt(self.startField))
            slotLine.deleteLater()

    def clearRangeTab(self):
        for k in range(1,len(self.layoutNetRanges)):
            rangeLine = self.layoutNetRanges.itemAt(1)
            self.deleteLayoutLine(rangeLine)
            self.layoutNetRanges.removeItem(self.layoutNetRanges.itemAt(1))
            rangeLine.deleteLater()

    def clearStatsTab(self):
        for k in range(1,len(self.layoutNetStats)):
            statLine = self.layoutNetStats.itemAt(1)
            self.deleteLayoutLine(statLine)
            self.layoutNetStats.removeItem(self.layoutNetStats.itemAt(1))
            statLine.deleteLater()

    def clearGraphTab(self):
        ...

    def populateMap(self):
        for k in range(len(self.slotMap)):
            slotLine = self.makeSlotLine()
            slotLine.itemAt(0).widget().setText(str(self.slotMap[k]['slotIdx']))
            if self.slotMap[k]['slotType'] == 'SLOT_RANGE':
                slotLine.itemAt(1).widget().setCurrentIndex(0)
            else:
                slotLine.itemAt(1).widget().setCurrentIndex(1)
            slotLine.itemAt(2).widget().setText(str(self.slotMap[k]['configId']))
            slotLine.itemAt(3).widget().setText(str(self.slotMap[k]['ownerId']))
            slotLine.itemAt(4).widget().setText(str(self.slotMap[k]['targetId']))
            slotLine.itemAt(5).widget().setText(str(self.slotMap[k]['period']))
            slotLine.itemAt(6).widget().setText(str(self.slotMap[k]['maxUserData']))
            self.layoutSlots.addLayout(slotLine)

    def buildRangeTab(self):
        for k in range(len(self.slotMap)):
            idColor = self.gui.pen[k].color().getRgb()
            idColor = idColor[0:3]
            idColor = "QLineEdit {background-color: rgb" + str(idColor) + ";}"
            rangeLine = self.makeRangeLine(idColor)
            # rangeLine.itemAt[1].widget().setStyleSheet(idColor)
            self.layoutNetRanges.addLayout(rangeLine)

    def buildStatsTab(self):
        ...

    def makeMap(self):
        self.localSlotFirst = -1
        self.localSlotLast = -1
        self.localSlots = []
        self.slotMap = []
        # print(f"len: {len(self.layoutSlots)}")
        for k in range(2,len(self.layoutSlots)):
            slot = dict()
            slotLine = self.layoutSlots.itemAt(k)
            slot["slotIdx"] = int(slotLine.itemAt(0).widget().text())
            tmp = slotLine.itemAt(1).widget().currentText()
            if tmp == "Range":
                slot["slotType"] = "SLOT_RANGE"
            else:
                slot["slotType"] = "SLOT_DATA"
            slot["configId"] = int(slotLine.itemAt(2).widget().text())
            slot["ownerId"] = int(slotLine.itemAt(3).widget().text())
            slot["targetId"] = int(slotLine.itemAt(4).widget().text())
            if slot["ownerId"] == self.gui.radioReqNodeID:
                self.localSlots.append([slot["slotIdx"],slot["targetId"]])
            slot["period"] = int(slotLine.itemAt(5).widget().text())
            slot["maxUserData"] = int(slotLine.itemAt(6).widget().text())
            self.slotMap.append(slot)
        if len(self.localSlots) > 0:
            self.localSlotFirst = self.localSlots[0][0]
            self.localSlotLast = self.localSlots[len(self.localSlots)-1][0]
        self.updateDestMenu()
        # print(f"MakeMap: {self.slotMap}")

    def findWidget(self):
        print("================\n\nDown")
        butAddr = self.sender()
        print("Button Addr", butAddr)
        butName = butAddr.objectName()
        print("widgetName", butName)
        widget = self.layoutSlots.itemAt(int(butName)).itemAt(4).widget()
        print("text", widget.text())
        print("\nTop Children ", self.layoutSlots.children())
        slotLine = self.layoutSlots.itemAt(int(butName))
        print("\nslotLine", slotLine)
        print("  Slotline Position 4 Widget:",slotLine.itemAt(4))
        print()
        for k in range(len(slotLine)):
            widget = slotLine.itemAt(k).widget()
            print("SlotLine Widget(pos,type):", k, widget)
            if butAddr == actualWidget:
                print("   Found it here)")

# Class for large range window that can more easily be seen from a distance.
class windowRangeLarge(QWidget):
    def __init__(self, gui):
        super().__init__()
        # self.setGeometry(10, 10, 1100, 540)
        self.setFixedSize(1100,540)
        self.setWindowTitle("Range Output")
        self.gui = gui
        self.setStyleSheet(self.gui.windowSheet)
        self.guiFont = guiFonts()
        self.initGUI()

    def displayWindow(self):
        self.show()
        xOffset = self.gui.x() + self.gui.mainWindowWidth + 5
        yOffset = self.gui.y()
        self.gui.windowRangeLarge.move(self.gui.monitor.left()+xOffset, self.gui.monitor.top()+yOffset)

    def processData(self, range, shade):
        # range = float(range)
        # precRange = f"{range:.3f}"
        self.dispRange.setText(range)
        tmp = "QLineEdit {background-color: rgb(255," + str(shade) + "," + str(shade) + ");}"
        if range != "-":
            if range != "0.0":
                self.dispRange.setStyleSheet(tmp)
            else:
                self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,0,0);}")
        else:
            self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,255,255);}")

    def initGUI(self):
        self.guiFont = guiFonts()
        yStart = 0
        xStart = 10
        xWidth = 1080
        yWidth = 160
        self.labelRange = QLabel(self)
        self.labelRange.resize(xWidth,yWidth)
        self.labelRange.move(xStart, yStart)
        self.labelRange.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelRange.setFont(self.guiFont.guiFont100)
        self.labelRange.setText("Range(m)")
        yWidth = 350
        self.dispRange = QLineEdit(self)
        self.dispRange.setStyleSheet("QLineEdit {background-color: rgb(255,255,255);}")
        self.dispRange.setFont(self.guiFont.guiFont200)
        self.dispRange.move(xStart, yStart + 160)
        self.dispRange.resize(xWidth,yWidth)
        self.dispRange.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispRange.setText("-")
        self.guiRange = 1

# This class makes it easier to change fonts across the whole GUI all in one place with a higher level name.
class guiFonts():
    def __init__(self):
        self.guiFont14 = QFont()
        self.guiFont14.setPixelSize(18)
        self.guiFont18 = QFont()
        self.guiFont18.setPixelSize(22)
        self.guiFont20 = QFont()
        self.guiFont20.setPixelSize(24)
        self.guiFont24 = QFont()
        self.guiFont24.setPixelSize(30)
        self.guiFont30 = QFont()
        self.guiFont30.setPixelSize(38)
        self.guiFont34 = QFont()
        self.guiFont34.setPixelSize(40)
        self.guiFont50 = QFont()
        self.guiFont50.setPixelSize(60)
        self.guiFont100 = QFont()
        self.guiFont100.setPixelSize(120)
        self.guiFont200 = QFont()
        self.guiFont200.setPixelSize(240)

class TDSR():
    def logo(self):
        self.getBytes()
        ba = QByteArray(self.tdsrBytes)
        tdsr_logo = QPixmap()
        tdsr_logo.loadFromData(ba, "PNG")
        return tdsr_logo

    def getBytes(self):
        self.tdsrBytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x85\x00\x00\x00@\x08\x06\x00\x00\x004\xff\xb4;\x00\x00\x00\xe1iCCPsRGB\x00\x00\x18\x95c``<\xcd\x00\x04L\x0e\x0c\x0c\xb9y%EA\xeeN\n\x11\x91Q\n\x0cH 1\xb9\xb8\x80\x017`d`\xf8v\rD20\\\xd6\r,a\xe5\xc7\xa3\x16\x1b\xe0,\x02Z\x08\xa4?\x00\xb1H:\x98\xcd\xc8\x02b\'A\xd8\x12 vyIA\t\x90\xad\x03b\'\x17\x14\x81\xd8@\x173\xf0\x14\x85\x049\x03\xd9>@\xb6B:\x12;\t\x89\x9d\x92Z\x9c\x0cd\xe7\x00\xd9\xf1\x08\xbf\xe5\xcfg`\xb0\xf8\xc2\xc0\xc0<\x11!\x964\x8d\x81a{;\x03\x83\xc4\x1d\x84\x98\xcaB\x06\x06\xfeV\x06\x86m\x97\x11b\x9f\xfd\xc1\xfee\x14;T\x92ZQ\x02\x12\xf1\xd3wd(H,J\x04K3\x83\x024-\x8d\x81\xe1\xd3r\x06\x06\xdeH\x06\x06\xe1\x0b\x0c\x0c\\\xd1\x10w\x80\x01k10\xa0I\x0c\'B\x00\x00r\xd86\x84\xa3\x1fG\xb3\x00\x00\x00\tpHYs\x00\x00\\F\x00\x00\\F\x01\x14\x94CA\x00\x00\x01\xaezTXtXML:com.adobe.xmp\x00\x008\x8du\x94\xcbn\xc20\x10E\xf7|\x85\x95\xae\xf1\xd8\x81V\xc2\n^\x14\xd4]U\xd4\x87D\x96&1\xad\xdb$\x8el#\xc2\xdf\xd7yP\xd2\x10\xb2\xb2\xef\xdc3~L\xc6Q\xc5\xaa\xbc\xcc\xa5\x13\xa8\xca\xb3\xc2\xb2j\x19\x88T\xef$\xf3\xe3Z\x86\x005\x16\xf7\xb3\x0c\xb6\xcf\x1b\xb4\xd2F\xa2{<\xc7$\xe0\x13\x84Pd\xd2={]?u\xb8\x9f-\x83/\xe7J\x06p<\x1e\xf1q\x86\xb5\xf9\x04\xbaX,\x80\x84\x10\x86S\xef\x98\xdaS\xe1D5-\xec]\x9b\xe4\x9cg-mbT\xe9\x94.P=\x17;}p\xcb \xe8<\xed\xd7.\x94&\x7f\xeb\x94\x07\x935\xab\xa4\t\xc8L\xe6\xb2p\x16(\xa60\xc6\xf9\xa3\xfc\x81\x85\xc5\xcdYq\xa2s\xa8D\xe9!2\n\xc9J\xed\xc7\xa9:r\x13sj\x7f\x03\xab#-\xc6/\\\x94&\xcc\x1ev\xdf2q\xfc_\xb6\xe6n\x1e\xc5\'\xf4\xcd0\xea\x8e\xfc\xf9\xd8\xb3N\xd5\xfe\xb4\x16N\xf2\x90\x84\x94\x91{F\xe6\x88\x92z0\xa7\x11\x0c<\x03ze\xa4p\xda\xbck\x9d\xf1\x8d\xaad\x96\xd7S4\xc3\x0b\x1c\xb6l\xdf\xd1\x83\xeb\xbb`\r\xb1]+_\x05\xeb\xcb\xc8\xe9l\x16\xc1hd\x94\x8c/\xf1\x87y\x1f\x8co\x83+\x9di\xf3V\x8aDr\xda!=\xa9\xe7\xaeo\xdd\x87\xf2\xd2H\xdbd"\x11\\iC\xff\xf6UZ\x9d\x1d\\\xb3%r&\xfa\xea\x90\xb8\x84>\n\xe5x\xd8!\x03yH\xbd\x18\xe5\x7f\\\xd1d\xa4\x1d\xd2\xd7\x86\xfext_\xf1\xf5\xbe"\x18\xb4V\xdb\xb7\xd05.\x9f\xf8\xa2\x9e\x1f\x01>\xf9\x056\\:\xb1)\x9a!\x8d\x00\x00\x19\xceIDATx\x9c\xed}i\xb8]U\x99\xe6\xfb\xae}\xf6\xd9\xc3\xb9d&!\xc8$C\x80@\x18\x03\x14 \x8a@\x80\x12\x8bA&\xc1\x81\xb2\x10\x1b\xa9\xd2\xae\xd2\xa7\x9e\xae*\xdb\xb6\xd5\xb2\xbb\xda\xae\xa7\x1f\xaa\xb4\xaal[E)\x01\xa3b\x11i\x11AH(\x90y\x900\t\x06H\x80\x100\x84\xdc\xdc\xdcs\xce\x1e\xd7\xdb?\xf6\xbe\xe4\xe6\xde\xbd\xef\x9c\x84\xaa\xce\xfb<\xe7\xc7\xd9k\xed\xbd\xbe\xbd\xce\xb7\xbe\xf5\x8d\xeb\x10[\xa3\xa7\xd1h|\x11\xc0g\xb0\x13\xff_\xc2Z\xfb\xd9\xc6\xa0\xef\xf4}\xff(\x92\x17\x93\xdcaD\xed\xc4\x8e\x83\xa4g%\xddh\x06]\x9bM\xf2*\x92\xef\xd8aT\xed\xc4\x8eD&\xe9o\xa2(zy\x80)\x18\x04\xc1{I^\xb8C\xc9\xda\x89\x1d\x89\x15\xbe\xef\xdf\x04\xc0\x0el\x1f\xbb\x01\xf8\x14\x00S\x7f\xcfN\xfc{\x85\xa4\xcd\xd6\xda\xaf\xf5\xf6\xf6\xf6\x01\x05\x138A\x10\xfc)\xc9\x93v0m;\xb1\x83 \xe9kq\x1c\xdf\x06\xc0\x02@#\x08\x82c\x01\\&)\xdf\x11\xf4\x00\xb0$\x1b\x18AJI\xb2e\xdf\x9d\x98Z8\x00\x1e\xb4\xd6.\x05\x10\r\\$\x80}=\xcf;\x14\xc0\xf6f\n\x01\x10\xc9\xdf#\xf9\x9fHz\x15}2k\xed/\xad\xb5\xdf$\x19\xa3\xa0w\'\xa6\x0e\x8e\xa4\xd5I\x92<\x03 \x1d\xb8\xd8\x00\xf0b\x1c\xc7/\xee\x00\x82\xd4j\xb5\xe6I\xba\x00@\xb3\xb2\x83\xf4Z\x96e\x7f\x9be\xd9r\x94\xa2\xad\x02;\x82Q\xc6*\xb5&B\xdbTJ\xc4\xb1\x8c?l\xbc\xc6\x14\x131\x1e8y\x9e/1\xc6\x9c\x8bj\xe2\x13k\xed\xf5Y\x96\xdd\x87-\x0c\xd1\x18\xd2\xc7\xa2\x9eY\xb65\x0c\xea\xb7<\x95\x9f\x89\xd06\xd2s\xc7\x8a\x81\xb1\'\xf4\xdb\x0e\x9d\xe4\xed\x06\xcf\xf3\xf6%\xf9I\x003k\xba<\x05\xe0\xdb\x00:\x00\xe8y\xde;\x8d1\x7f \xa9\x07\xc5\xb6\x93Iz\x95\xe4\xf3\x00^\xeav\xbb}\x00\xda\xd8vL\xe2\x00\x08<\xcf\x9b\x0b\xe0\x00\x92\xbb\x93\x9c-i\xa8\x94\xb3$;\x00^\x97\xb4\x96\xe4\x9an\xb7\xfbfI\xdbh\xa0\xe7y\xa74\x1a\x8dc$Mh\xc1\x92\xcc\xad\xb5\xfd\xd6\xda\x17%\xbd\xe0\xfb\xfek}}}}\x00\xb2\xb1>cG1\x85\xe78\xce%\x00\x16\xa3FJ\xe4y\xfe\xcd8\x8e\xd7\x00\xc0\xb4i\xd3f\xa6iz\x05\xc9\xcf\x90l\xa2\x9c,\x92 \xd9\'\xe9E\xcf\xf3~e\x8cYN\xf2\xdeN\xa7\xb3\x1e\xe3\x98\x841`\xa6\xe7y\'\x19cN%y*\x80\x03\x00\xb8(\x98\xb3\x8a~\xa2d\x0eIO{\x9e\xb7\xbc\xd1h\xfc\xa0\xddn?\x87\x82\xc9\xeb\xe0\x18c\xde\'\xe9\x8fQ\xb3\xa5\x8e\x06I \t\xc7qR\x00\xeb\xb3,\xbb\xcf\xf7\xfd\x9b\x8c1wv:\x9dW\xc7\xf2\x0cg"\x03O\x16a\x18\x1e.\xe9\x0b\x00\xe6\xd5\xb8\xd4\xef\x04\xf0\xbf\xb2,\xdb\x80b\xa2\xce$y\x15\n\x7f\nPL\xfa\xc0\xc7\x974\xcf\x18\xb3\xd8\x18s\x06\x80\x83\x1c\xc7\xf1\x1a\x8dF_\x96e\xbd\x93$\xd5\xf4\xf4\xf4,t\x1c\xe7OJ\x86<U\xd2\xbc\xd2Z\xe2\x08\x9f\x01\x1a\x9b$w7\xc6\x1c+\xe9\xb8f\xb39\xc3\x18\xb3.\xcf\xf37\xeb\xc6s]\xf7\x14\x92\xc7b\xf2\x0b\xd6\x01\xb0\x8b\xa4\x03I\x9e\x0e`\x7f\xdf\xf7\xdfH\x92d-F\x91\xa6;\x82)\x82F\xa3\xf1\x17\x00N%Y5~\x9f\xa4/FQ\xf40\x80\xdc\xf3\xbc\x03\x8c1\x9f\x07p\x04j&\xaa\\\xad\x04\xe0\x03XH\xf2\xdd\x00\x16\x18c\x92<\xcf\xd7\x01\x88\'Dh\x10\x1cC\xf2\xcf%}\x98\xe4<\x00N\x8dd\x18\t,\xef\xdb]\xd2\xbb\x8c1{\xb9\xae\xbb*M\xd3u\x15}\x8d\xeb\xba\xa7\x91<\x0eS$\xc5I\x1a\x92\x1e\xc9\x83%-n6\x9b}i\x9a>\x8b\x11$\xe9vg\x8aV\xab\xf5AI\x9f!9\xad\xaa]\xd2\xdfw\xbb\xddk\x01\xf4\x03h\xf9\xbe\xff\x97\x92..\xb7\x8d\xb1" y\xb01\xe6T\xd7u\xf7w]\xf7\xe54M\xdf\xc4\xf8\xcc\xee\xfd\x9b\xcd\xe6\xff\x00p6I\x7f\x1c\xf7\xd5\xa2\x940\x0b%\x1d\xed8\xce\x9a<\xcf\x9f\x1f\xd2e\xca\x99b\xf0\xf0\x00\xe6\x028\xd9q\x9c\xa0T\xe0+\x19c\xbb2E\x18\x86\xbb\x93\xfc\x12\x80\x83Q\xada\xaf\xcc\xb2\xec\x7fZkW\x01`\xab\xd5z\x8f\xa4\xbf 9c\x82C\xb6\x00\x1c\x04`A\xb3\xd9D\x9a\xa6\xab\x00$\xa3\xdd4g\xce\x9c]$]b\x8c\xf9(\x80`\x82c\xd7\x82\xe4<c\xccn\xc6\x98{\xf3<\xdf8\xa8i[2\xc5\x00\x06\x16\xcc\x86<\xcf\x1f\xa9\xea\xb0]c\x1d$?"\xe9(T0\xa3\xa4D\xd2\xf7\xd24}\x12\x85"9\xc3Z{\xa5\xa4\xdd\'9\xac\x0f\xe0\x14I\x7f\x1e\x86\xe1\x87\x01TJ\xa8\xc1d\xb6\xdb\xed\x83I\x9e)i\xb4\xbe\xc0\x16\xb3x\xe03\x16\x8b\xc1\x91t\xa21\xe6\x93\x18\x9f/C(Vw>\xc2g,\xd6\xd7\xae\xc6\x98\x8f\xbb\xae{dU\xe3v\xb3>\xc20<\xdaZ{\x01\xc9\xe95]n\xedv\xbb\xb7\xa0\xd86\xe8\xfb\xfey\xa5n0\x8cqK\r\xfb&I/\x028\x1c\xc0Q\xa3H\x13\x03\xe0 I\xff\xd1\xf3<\xc5q|\x03\x80\xbe\x9a\xbe\x01\xc9\xc5($L\x152IOI\xfa1\xc9\xe7Hn%y$\x19I\xbb\x90<\x98\xe4\x19\x92\x0e#9\xec\x1dH\xb6\x00\x9c\x19\x86\xe1\x0f:\x9dN\xe5\x8a\x1d\x826\x80\x1bI^/\xa9\xca\xfb;0\xbec\xad\x9d\xe78\xce\xfb$\xbd\x97dOU?\x92G5\x1a\x8d\x0f\xa7i\xfa\xd8\xd0\xb6\xed\xc5\x14\x9e\xb5\xf6r\x92\x0bQ\xbd2^\xce\xf3\xfc:\x00\xbf\x05\x00\xdf\xf7\xf7!\xf9q\x00\xb3\xaa\x1eF\xf2\x89<\xcf\xbf\x11\xc7\xf1C\x00Z\x9e\xe7\x1dJ\xf2\x1cc\xccY\x00\xdeQ3\x06I\x1e\xe88\xce\x95A\x10l\xecv\xbb?F\xf5\xaa\xda\xc5Z\xbb\xc8\x183\xaf\xa2-\x97t\xbf\xa4\xcfEQ\xf4(\x06\xc5\x0b\x06\x8f\x83\x82\t}\xd7uot\x1c\xe7c$?\x84j\t\xb5\x17\xc9\xf3\x01\x8c\x85)R\x92\xbfi\xb7\xdb\xb7a\xf4m\xbf\x01`\x99\xeb\xbag5\x1a\x8d\xcf\x91\xdc\xa7\xa2\x8fC\xf2\xa40\x0c\xe7w:\x9duCo\xde\xe6\x08\x82\xe0l\x00\xa7\x91\x0c+\x9a%\xe9\xc6$IV\xa0\x10\x7f\x8e1\xe6rI\x87\xa2z{K\xad\xb5K\xe38~\x10\xc0F\x00o\xc6q\xbc\x0e\xc0}a\x18.\x93\xf4\x97\xe5\x9e\\\xa5\x98\x12\xc0\xa1$\xaf\xf0<\xef\xf18\x8e\x9f\x1d\xda\xc1\xf3\xbc]\x8c1s\x01T\xad\xc6\xf5\xc6\x98\x9b\xda\xed\xf6\xdd\x18}\x9b\x88\xd34}\xd8\x18\xd3\x8b\xe2G\xfcx\xc5\xfb\xf4\xe4y~4\n\x86\xa9\x93\\\x03\x18\xec\xa5\x1c\xcd\x07\x93\x01X\x97\xa6\xe9\xb5\xc6\x18\xe38\xce\x7fG\xf5\x02\xdb_\xd2;\x01l\xc5\x14\xdbC\xa7\xd8\x03\xc0\xf9$\xf7\xaej\x94\xb4.M\xd3\x9f\x01X\x0f\x00a\x18\x1e!\xe9\xf7\xeb\xc4\x9e\xa4{\xcaX\xc8\xe0I\xcc\x00\xf4v:\x9d;$}^\xd2OHn\xae\xa1\xa7\x01\xe0\xc8\xd2\xa71l+\x93\x14\xa2PP\xab\xd0\x96\xf4\x1c\xc6\xeeiT\x1c\xc7k\xb2,\xbb\x15\xc0\xef*\xda\x8d1f\xae\xeb\xba\xef\x1c\xc3\xb3&\x12GI\xe28\xbe\x11\xc0\xc3\xa8\xa0Y\xd2\x8c<\xcf\xf7\x18F\xd4\x04\x06\x1a\x0f\x18\x04\xc1E$OA\xf5\xca\xcd%\xdd\x91e\xd9\x03(\x88\x0e\x00\xfc!\x8a\xfd\xbcj\x12\xde yc\x96e+Qm^&Q\x14\xdd\x9d\xe7\xf9_K\xfa\xd1\x08\x8c1\xdb\x18s\xb6\xef\xfb\x87a\xf8\x1c\x0c(r\xc3 \xc9\x91T\xc70uHH\xae\x94\xf4R\xcd3{\x8c1{\x8e\xf3\x99\xe3\xc1\x06k\xed]\xa8\xf0\xd5\x90\xa4\xe38\xf31d\xae\xb75S\xec^\xee\x99\xbbV5Jz^\xd2u\x006\x03@\x18\x86\xa7J:\xbdf\x9b\x81\xa4\xdb;\x9d\xcer\x14\xcah\x1dl\x92$O\x91\xbc\xdaZ{\x1b\xaa\xf7}H:\xd2\x18s*\x86H\x0bcL\xbf\xa4^TK\x83\xd9e2\xd2\xb8L\xe48\x8e7K\xaa\xa3\xd91\xc6L\x89\x1f\xa4\x0e$_\x904l\xcb!\x892\x96\xb4\x95\x1a\xb1\xcdt\x8a\xf9\xf3\xe7\x87}}}\x1f\x92tlU\xbb\xa4\xcd\x00\xbe\x19\xc7\xf1\n\x00\xf0<\xef\x00\x00W\x91\xdc\xbf\xa6\xff\xcb\xd6\xda\xef\x02\x18\xa6\x07T\xa1\xddn?\xe1\xba\xeeW\\\xd7\x9d\x0e\xe0=(b\x15\x831K\xd2\xe9\xbe\xef\xffk\x14Ew\xa1\x94\x0eQ\x14m\xf2}\xffY\x92o\x02\x98=\xf8\x06\x92\xbb\x008\xdf\xf7\xfd\x86\xa4\xff\xeb8\xce\xdaF\xa3\xb1\xd9Z\xdb\xdb\xdf\xdf\xbf\x195\x0c\x08 #\xb9\xbe\xa6M\xd8\xc6\xb9,y\x9e;\x8e3\\7\x95\xde\xe2\xfb\xad\x16\xc06c\x8a\xde\xde\xdeE\xa5\xd6]5\x86H>\x90\xe7\xf9\xbf\xa0\x10kn\x994|,\xaaM\xd0X\xd2\xf28\x8e\x1f\xc18&0M\xd3\xc7]\xd7\xfd!\ng\xd9\xb0,uc\xcc\x82<\xcf\x8f\x05p?\xb6\x04\xaa\xda\x92\x1e\x93\xf4\n\xc9\xd9C\xefA\x11\xaf\xb9\xc4\x18s<\x80\xd7\xb2,k[k\xfb\x82 x\x13\xc0\x0b\xd6\xdag\x1c\xc7yj\x88F\xdfg\xad\xfd\x8e\xe38mI\xe7\x92|K\xe9+\x83f\xaf\x8d\xf5\x9d&\x82F\xa3q\x08\xeasVz1dN\xb7\tS\xcc\x9c9sz\x1c\xc7\x1f\x01pHM\x97\r\x92\xbe3\x10\x05\xf5}\xffx\x92\xe7\xa0\xde\x04}\xceZ\xfbC\x00u\x81\xa4:XI\xb7\x008\x0b\xc0\xb4r\xa5\xbf\x05I\xb3H\x1e6c\xc6\x8c\xb9\xbd\xbd\xbd\xab\xcb\xcb\x19\xc9\xc7I\xde\x03`!\x86K\x98\x01\x89\xb1\xa8|?\x19c\x84"s\xa9\xd7q\x9cW%=\x17\x86\xe1\xddy\x9e\xdf\x16\xc7\xf1\xf3\x00\xb28\x8eWx\x9e\xb7\xca\x18\xf3\x94\xa4O\x0f(\xde\x926v\xbb\xddm\x96\xe4\xe4\xfb\xfe\xde\x00\xde[\xf5\x1e\x00\xac\xe38k1DRl\x0b\x9d\xc2dYvr\xb9\xf2\xab\xecik\xad\xbd\xa5\xdb\xed\xfe\x12\x05\x87\x06\xc6\x98KH\x1e\x86j\xe5r\xa3\xb5\xf6\xfa\xd2\x04\x1dw~A\xb7\xdb]g\xad\xbd\x8d\xe4\xaa\x8af\x92\xdc/\x8a\xa2\xfd0h.\xa2(Z\x9b$\xc9O\x00<7\xca\xe3\r\x8awl\xa0P\x92\xe7\xa3p\xa4\x9d\x0f\xe0\xaf\x8c1W{\x9e\xf7\xc99s\xe6\xccGa\t\xbc\xd0\xedv\xaf\x91\xf4y\x00\xcf\x00\xe8\x90\\\x89j\xcbd*0O\xd2g%U\xce\xad\xa4\xd7\xd24]=\xf4\xfa\x94K\x8a0\x0cw\xcb\xf3\xfcJ\x14\xc1\x97a\x90\xb4\x06E\xf2\xcc\x06\x00\x08\x82\xe0\x08Ig\xd4\x04\x9d\xac\xa4_EQt\xc3@\xff\t\xc0JZ!\xe9\x04\x00GV\x049\xe7\x19c\xf6\xc6\xd6\x93\x96gY\xf6\xa0\xeb\xba\xd7\x00\xb8\xb2N\xcf\xa9\x01Q\x88\xea=H\xces\x1c\xe7\xf0N\xa7s\xb4\xe7y_\x8d\xe3\xf8\xb7\x006FQtS\xb3\xd9\xcc\x1c\xc7\xf9\x84\xb5\xf6\xe7\x18{b\x90\xc1\xd8~3\xdf\xf3\xbc\xe3\x8d1\x1f%\xf9>\x00\x95\x8a;\x80g\xd24}a\xe8\xc5\xa9f\nG\xd2\xbbI\x1eS\xd3n%\xdd\x1eE\xd1\xd3(&b\x1a\xc9\xd3P\xb1\xdf\x97\xd8`\xad\xbd\x19\xc0\xab\x98DFU\x92$\xeb\xc20|IR\x17\xc3\x03\\\xd3%\xed\x8ab.\x06\xef\xad\xfdy\x9e\xff\xcc\x183\x07\xc0\x85\xa5Wp\xbc\x01D\x17\xc0\x9e\x92\xde\x0f\xe0M\xd7u\xaf+c;\x9b\x93$\xb93\x08\x82\xdc\x18\xf3\xf8X\x1e$\xa9)\xe9\xf80\x0c\xaf\xa8\xc8\xf6\x1a\x00\x01P\xd2,c\xccbI\xc7\xa0fK\x96\x14I\xba\x0f\x15N\xb3\xa9f\x8a=\x01|\x02C\xb4\xf6A\x84<\x97e\xd9\xb5(t\x03\xb6Z\xadc%}\x10\xd5J\x90-\x95\xcb\x9b1(\xd3x\x82\xe8\x07\xf0\x12\xc9\r(\x9ci\x83\xd1c\x8c\xd9\x15E\xe0l+[>I\x92g\x01\xfc\xa3\xef\xfb/\x90\xfc\x00\x80CQL\xb2\x8fql\xbd\xa5\xc4\xb8\xdc\x18\xb3g\x10\x04W\xf7\xf5\xf5=\x04\xe0\xf5\xd2\xd5>\xa6-\x91d \xe9\x14\x00\xc7\x8f\x92\xd2aP0~0J\xbf\x07\xca\xd4\xfea\x98J\xa6p\x82 \xb8\x00\xc0q5\xed\x89\xa4\xeb\xb3,{\x02\xc5\xaa\x9f\x9b\xe7\xf9%$\x0f\xac!\xfe\x15k\xed\xf7\x00L\x85f.I\x1bHV\xb9\x92\x1b\x92vA\xb5[[\x00^\x9e9s\xe6u\xbd\xbd\xbdOHZd\x8c9R\xd2A$gI\xea)}*>\x8a\x1fb$\x7f\xc3,\x92\xe7\xa6i\xea\xf4\xf4\xf4|\xa9\xbf\xbf\xffI\x8cO\xfa\xb1\x0c\xa2\x8d\xea<\x1b-\x0fH\xd2\x1aI\xff\'I\x92\'\xab\xda\xa7\x8c)Z\xad\xd6!\x92>\x82\x9a\xfdK\xd2\x03Q\x14-C\xe1\xa8r\x82 8\xa5\xdc\xef\xaaDr\x0e`Y\x1c\xc7\xf7aj\xb2\xcdE\xb2\x8d\xfa\x0c,\x1f\xd5\xda9\x00`\xdd\xbau\x1d\x14f\xebc\x00n\x0f\x82`\xb7<\xcf\xa7I\x9an\x8c\x99a\x8c\x99\'i\x01\x80E\xc6\x98}$\xd59\xb7|Ig\xe5y\xfe\n\x80/\xa3\x88\xddlOX\x00k\xf2<\xffF\x92$\xcb\xea:M\x15SL\x93\xf4\x19\x14\xfe\x80*\xac\xcb\xf3\xfc\x1f\x00\xfc\x06\x80\x9a\xcd\xe6A$?\x85-9\x97[A\xd2\xfdy\x9e\x7f\x13\xdbw\xd2\xc6\xc2|1\x80\xd5\xddnw\xf5\xa0k\x03\x8a\xe5.\xae\xeb\xee\xd5l6\xdf-\xe9\\\x00\x8b\xcb\x95\xbd\x15\x8c1\xa1\xa4\xcbZ\xad\xd6\xcb\xedv\xfbk\x98\xda\x04\xe3\xd1\x10YkoH\x92\xe4j\x8c\x90l4%&i\x10\x04g\x00X\x82\x8a\xd5\xa6\xa2\xe4oY\x92$w\x97\x84\xf8\x8dF\xe3bIG\xd4<\xae\x9f\xe4\xf7\x93$\x19\x9a\xaa6\x19\xb0\x8cY\xd4\xe5!D\x98\xf8\x8f\xe3\xa0x\xaf7\xd24}\xd4u\xdd\xefZk\xbf\x02\xe0\xa6:\xd7v\xb9\xf5\\\xda\xd3\xd3\xb3`\x82cN\x14\r\x92\xfb{\x9eW\x19\x9c|\xab\xd3dG\t\x82`\x0f\x92\x97\xa1f\xd5\x93|\xb4t<\xbd\x06\x00\x8dFc1\x8a\xa8im|\xa3\x8cYt\'K\xdb \x98\xd2;Y\x95\xd3\x90\x96.\xf7\xa1[K\xab\xa7\xa7\'\xec\xef\xef\xdf\x08\x00\xcdf\xf3@\x14\xa9\xfd\xc6\x18\xb3!\x08\x82_o\xdc\xb8q\x93\xef\xfb\xef(C\xf5\xaft\xbb\xdd\x95\xbd\xbd\xbd\xbd\x00\x96\x87a\xd8K\x12\xd6\xda\x0f\x90\xacJ\xe9;\xc0Z{\x1e\x80\xa7\xc7\xf8\x0e\x92\xd4&\xd9\x8f\xe1>\x07\x02pK\x1d\xa7v\x1bD\xe19>\x93\xe4F\x00\x9fC\x8d\x99?Y\xa6 \x80K\x01\x1c\x8fj\xf7tj\xad\xbd\xaet<Y\x00\xd3\x9a\xcd\xe6\xc7$\xbd\xb3F\x19Z\x9b\xe7\xf9\xf7\x93$ye\x92t\rE\x0b\xc0^\x92fW\x8c\xdb\x8f\xc2y48n\xe1\xb5Z\xad\x93\xf2<?\xc0\xf7\xfdeQ\x14\xbd\xe28\xce\x81$//u\x87\x97\xb2,\xfb:\x80\x7f\x89\xa2\x88A\x10\x9cCrn\x10\x04?\xb7\xd6\xde\x14\xc7\xf1\x0b\x9dN\xe7\xd1 \x08\xfeI\xd2\x1c\x92gT\xd0\xb4\x8b\xa43}\xdf\xff\xe7(\x8a*#\xa8\x83Q\x9a\xd3w\x00\xf8\x19\x86Xk\x92\x0c\n\xbdh\x9e\xb5v!\xc9CIVE^\t`\x9a1\xe6\x02\xcf\xf3\x9e\x8c\xe3\xf8\xebUcM\x8a)<\xcf\xdb\x17\xc0\x19\xa8\xb1\x85\x01\xac\xb6\xd6\xae@Y\x1d\xe5\xfb\xfeQ\x92N\xaaY9\x92t\x971\xe6\x11\x8c!\xb9v<h6\x9b\xbbK\xda\x1b\xd5I\xb8}\xc6\x98\xad\x8a\x87\xc20\x9cm\xad]\x02\xe0hc\xcc\xf3\x00^&\xb9\xdaZ\xbb\xc6\x18s\x9a\xa4\xdd\xb2,;\r\xc0\n\x00k%=k\x8c9\x1d\xc0~\xc6\x18\x00\xf8\x1e\x80\r\xddnw\xa5\xe7y\xb7JZ\\\x11G1$\xf7,=\xb9\xa32\x05\xc9\x84\xe4\x03\xedv\xfb\x9a\xba.\x00\xa6\xfb\xbe\xbf\x08\xc0\xfb%\x9dOr\x0fT+\xf2\xb3\x1d\xc79\'\x08\x82e\xddn\xf7\xe5\xa1\x8d\x93\xd1)\x0c\xc9?,\xf3\x19\xab\x10\x19c~Z:k\x00`\x06\xc9O\xa0\xf0e\x0c\x83\xa4\x17\xac\xb5\xdf\x8f\xa2h\xaa\xa5\x84C\xf2d\x92\x0bk\xa4\xd3ky\x9e\xbf\x84-\x8af3\xcb\xb2\x13$-!y\xac\xb5\xf6l\x00{w:\x9d\'\xb2,\xbbN\xd2\xd3e\x02\xd0\xa9\xcdf\xf3,\x00y\xa3\xd1\xf8\xb1\xa4\x07\x01\xec\x03\xe0\xcf<\xcf\xbb\x10\x85\xfe\xb2Y\xd2m(\x8a\x9b\xaa0\x03@\x9d\xa3\xaf\n\x16\x05\xf3V}R\x00oDQ\xb4\xbc\xdb\xed~N\xd2\x97%\xadD\xbd\xd9\xbb\x18\xc0\xf9U\r\x13f\x8af\xb3y\xa0\xe38\xe7\xa1&;Z\xd2\xc3i\x9a^[\x12\xccV\xabu.\xc9\xf7\xd4\xb8\xb3\x13\x927x\x9e\xf7\x00\xa68\x8c\x1c\x04\xc1n\xc6\x98\xd3%U\xb9\xaa\xad\xa4U\xbe\xef\xafB9y\xcdfs_\xc7q\xce3\xc6,@\xe1\x00:\xc5\xf7\xfd\xf7\x02p\xb2,{\x12\xc0\xf5\x92\xba$\xf7u\x1c\xe7\x03===\x07\xf6\xf7\xf7?\x9be\xd9\xf5\x92^"\xb9\x871\xe6\xb20\x0c\x0f\x05\x80$IV[k\xefE\xb5\xf4\xeb\x91\xb4\x08\x13,\x11\x1c\x01Q\x14E\xdf\xce\xf3\xfc+\x92~[\xd3g\x86\xa4\xd3P!=\'\xca\x14\xbe\xe38gK:\xb0\xa6}\xa3\xb5vi\x92$+\x01\xc0\xf3\xbc\xfd$}\x08@U2,H\xde\x07`Y__\xdfx\xa3\xa0\xa3\xc1!\xf9~\x92GW\xa5\xf7\x959\x13+{{{\x07r\x1dZ\x8e\xe3,a\x91E\xee\x95}\xf6#yv\xab\xd5:\x10\xc0\xa6<\xcfo%y7\n\xa5\xed\xc4\xd2\xfcD\x92$\xbf\x94t;\x8a\x04\xdb\x05\xd6\xda\xdfG!\xd2#\x00OK\xaa\nz9$\xe7\xa3FI\x9f,\x92$\xb9I\xd2\xf7%U\x167\x93<\xd8\xf3\xbc\xbd\x86^\x9f\x10S4\x1a\x8d\xc5$/A\xb5Nb\x01\xdc\x13\xc7\xf1\x8f\xca\xef^\xd9\xb7\xb2\xde\x03@,i\xe9\xdc\xb9s+\xbdk\x93\x81\xeb\xba\x87K\xba\x085\xcch\xad\xfd\xad\xa4\x87PX\x1e\x0c\xc3pa\xe9P\x1b\x1c\x8b1\x00N\xb0\xd6\x9e\x0e`Vi*/E\xa1\xb9\xcf\xb5\xd6\xbe\xaf\xd4\xad^w\x1cg)\x8a\x8c\xf4i$\x17\x01\xe8)\x86\xb1\xaf\x1bc6\xd5\x90\xe95\x9b\xcd\xba\xb2\x87\xc9"\x97t=\xc9:i1\x1f\x15\xdb\xf9D\x98b\x0f\xd7u\xff\x04E\xbd\xc50Hz1I\x92\xaf\x02x\x1d\x00J\xcd\xfc#\xa8WF\xff\x15\xc0M\xabW\xaf\xae\xcbZ\x9a\x10Z\xad\xd6aez\xfb\x89\xa8f\xde\r$\x7f\x11E\xd1c\x00\xf2\xf2\x00\x95K\x00\xbc\x1bCL>\x92s\x01\\\x14\x86\xe1\x05(\x18\xe8VI\xd7I\xb2$\x8fq\x1c\xe7\xd2\x993gNo\xb7\xdb\xf7\x92\xfc\x0e\x8b\xa3\x08\xe6\xf8\xbe?\x07\x00\x8c1\x9b\xad\xb5uG\x11\xf8\xcdf\xb3\xee8\x86I#\x8e\xe3\x17\xf2<_!iX\xfc\x88d\xe08\xce0\x9f\xc5x\x99\xa2\xe1\xfb\xfe\x12\x92g\xd5\xb4\'\x92~\x98e\xd9\xfd@\x91lC\xf2\x83$\xf7\xad\xe9\xbf\xceZ\xbb\xb4\xd3\xe9Le\xe6\x91)%\xc4g\x8c1KP\xe3\xb0"\xf9\x98\xb5\xf6\x0e\x00\x9b\x00\x984MO\x90\xb4\x04\xf5a\xe6C%]\xdcl6\x17t:\x9d\xd7$\xfd\x94\xe4\xa3\xe5\xf3\xcf\xe9v\xbb\x8bQ\xe4G\xfc<\xcf\xf3{\x01\x18I.\x00\x18c\x12\xd4\x04\xf5T\x14\x0fm\xd3\x1cMk\xedV\xc7\x17\r\x19\x7f\x16\x86H\xf0q1Ey\xd0\xc8\xc7Q\x88\xc5\xaa\x01\x9e\x8a\xa2\xe8\xbb(\xcd\xbbN\xa7s"\xc9\x93\x87\x0eZ"\x93tG\x14E?\xc5\xd4\x9d\xa6\xe3\xf9\xbe\x7fr\xa3\xd1\xf8+\x00\xe7\x97\x81\xae*l\xb0\xd6.\x8b\xa2\xe8q\x00\x9a>}\xfa>\xc6\x98?0\xc6\xd4\xe9H \xe9\x93<\xdc\x18s1\x00\'\x8a\xa2G\xac\xb5?A\xc1T\x0b\x01\\\x1c\x86\xe1\xfc\xfe\xfe\xfe\xe7\x01\\\x0f\xe0\x8d\x81{%9\xa8\x0f\xbb+\xcf\xf3\xc9F\x81GD\xa9;U*\xf0\xa5{`\xc2L\xe1\x19c\xce.\xbdw\xc3P:\xaa\xfe\x19\xc0\x0b\x00\x10\x86\xe1|\xc7q.\x90T)\x1a%\xbdj\xad\xbd\x0e\x83&o\x12h\x00\x98\x15\x86\xe1i$\xbfH\xf2\\\xd40.\x8a\x15\xf3H\xe95\xdd\x0c\xc0\xc4q\xfc.cLUr\xefP\xcc2\xc6\x9c\x19\x04\xc1\x91\x00z\xf3<\xbf\x1d\xc0\xbd(\xf4\xa6\xd3$\xfd\x1e\x80,\x8a\xa2{$\xfd\xc2\xf7\xfd\x0c\x00\xac\xb5A\x8do\x06$Sc\xccH\xd9\xe9S\x81\x91,\xbaa<0f\xe7\x95\xeb\xba\x07\x19c\xae(\xb9\xbe\n\xf7\xc6q\xbc\x14\x85\x940i\x9a\x9e\xe6\xban\xa5\x1d\x0c &\xf9\xd38\x8e\x7f\x85\x82K\'R\xe8\xd2@!\xba\xa7\x97\xe6\xdfy\x00\xce$\xb9\xfb\x08\xcf\x13\x80\'%}+\x8e\xe3U\x00\xd0l6\x0fa\x91\x1f:\x96\xda\x0b\xb28\xe7\xe1R\x00O\xa6i\xfa\x84\xe38?!y\x12\xc9\xbd\x00\\\xe6\xfb\xfe#Q\x14\xad\x89\xa2\xe8\x07Q\x14%@Q\xdb!\xc9\xaf\xf1\x93$y\x9e\x8fV\x1d\xb6]1V\xa6\x08]\xd7\xbd\xb2\xc6\xd6G\x19\xf8\xf9;\x94\xcae\xb3\xd9\\\xd0h4\xfe\x03\xea+\xbc;\xd6\xda\xdf\x95\x81\xb4\t\x81\xe4\xf4\xd2$>\xceZ{\x941\xa6N2\xbcE&\x80\xdfXk\xff1\x8a\xa2_\xa0\xb0\x92z\x1c\xc79\x13E\t\xc0\x98\xe6BE\xf1\xf0\xe9A\x10\xdc\xdd\xedvo\x04p\xbb\xa4\x07X\x14<\x9dH\xf2<\x00\xdf\xc0\x96\xda\x14\x87\xc5y\xe7\x95\x12\x93d\xdbu\xdd7\xe3xB\xe7\xaal\x13\x8ci"<\xcf;\t\xc0\x85\xa8\xd9n$\xfd0\x8a\xa2\x15(\xc4\x94o\x8c\xb9\x08\xc0\x89#<r:\xc9/\xb0\xfa$\x9b1c`\xe5\x8d\x96TR\xd2\xf5,\x80\xab\xa3(Z\x8ab\xdb\xa0\xef\xfb\xc7\x028\x87\xe4x\xb4\x7f\x02\xd8\x0f\xc0EA\x10<\xd0\xedv\xd7\xf8\xbe\xbf\xb4L\xbcy\x07\x80K\\\xd7\xbd+M\xd3_\x97\xfd\x03c\xcc\xc2\n77P\x98\xe3\xab\xdb\xed\xf6D\xf3O\xb7\t\xc6\xa2SLw\x1c\xe7\xd3\xa8\xe1tIkH~\x1b@/P$\xe2\x1ac.\x1fm\xdc\xc92\xc48\xd0\x05p\'\xc9\xafv:\x9d\x1bPV\xa3\x01\xd8\x8d\xe4\xfbQ\x1c\x9b4^+\xacY\x9a\xba\x1f@\xe1\xc4\xbaE\xd2\n\x009\xc9\xbd\x1d\xc7y+-\xa0\xd9l\xeeU\x86\x02\xaa\xde\xb7Cr\xbc\x19X\xdb\x1c\xa3J\x8a0\x0c/$\xf9\xae2\x127\x14\x19\xc9kZ\xad\xd6\xcan\xb7+\x14n\xdb+\xca\xfd\xf5\xed\x80\xdf\x01\xb8\x19\xc0?\xb4\xdb\xed\xa7\xb1%<n\x82 8\xa9\x8c^\x8e\xb76t\x00\xbb\x038;\x0c\xc3\xfb:\x9d\xceC\x9e\xe7]o\xad=\x02\xc0\xeaF\xa3\xf1P\xd9\'0\xc6\x9c@\xf2\x84\xaa\x07H\xea\xb5\xd6>:\xc1\xf1\xb7\x19Fd\x8a0\x0c\x17\x93\xfc\xd3:\xd3.\xcf\xf3\x9f\xc7q|m\xa7\xd3\xe9\x07\x00\xdf\xf7/,M\xb6\x1d\x8d7$\xddY\x86\xed\x97c\x8bt\x18\xc0^\x92.#Yk\x82\x8e\x01$y<\x80?\xdau\xd7]\x9fY\xbf~\xfd\x9d===\x9fN\xd3tm\x7f\x7f\xff\xb3\x00L\xa3\xd18\x9a\xe4\xc7P\xe1\xc6.\x9dI\x0fGQt\xef$h\xd8&\x18\x89)\x9a\xd6\xda?.m\xf7\xaaB\x92~I\xd7bK\xd8wOc\xcc\x95\x98\xf8\xca\x9b0$\x89\xa4\x05\xb0I\xd2/%\xdd\x0c\xe0\xee\x81\n\xb4\xc1\x987o^k\xd3\xa6M\'\xb38\x96p\xb2[X\x08`\xc9\xe6\xcd\x9b\x8f\x00pO\x7f\x7f\xff[\xd1P\xcf\xf3\xf6w\x1c\xe7r\x14\xd1\xc8a \xb9\x89\xe4\xcd\x18_2\xd1v9r\xba\x96)\x9a\xcd\xe69\xe5\x19\x0eU\'\xbf\x12\xc0\xa3I\x92,Gi\x03\xfb\xbe\x7f9\x8a\x14\xf8\xedz\xac3\xc9^\x00\xab\xf2<\xff\x95\xa4\x15\xae\xeb>\xd0n\xb7\xd7\xa3\xda6\xe7\xe6\xcd\x9b\x17\x18c\xce\x070g\nh%\x8a\xd3h.\xea\xe9\xe9y\xae\xbf\xbf\x7f \xe85\x8f\xc5\xf9^\x17\xb1\xfaT?\x8b\xa2\xfa\xec\xf6\x8a\xb6\xc1&\xfa\x00}\x03\xf5\x1c\x13\r`\x0ef\xfe\xc1\xef<\xf4\xecO\x00#0\x05\xc9\xcd\x92\xfe\xaeX\x84\xdcR\x9e\\|\xcf\xcb@\xd2\x80\xd6\xdc\x04\xb0J\xd2\x97&H\xf4D\x90\xe5y\xbeV\xd2\xf3\xae\xeb\xbe\x12\xc7\xf1f\x00\x9d$IFR\xdaL\x96e1\xc9\x9bI\xdeGrJ\xc2\xf4\xda\xba@x/\xcf\xf3\xfe\xcc\x18\xf3G\xa8w\x99\xf7Zk\xff)\x8a\xa2\xd7\x87\\\xb7\xa5\x94{URc\xf0\xbc\xa3\xd0\x87\xee\x9f\x08},J\x13\xbf\xa0!ED\x92\\\x92\xcb1$?u$q4\x9aS)\xc7\xd6\\\xb7#\x8et\x9e\xc8\x81\xedSq \xfa`\x08\xc5\xbb\xb7\x1a\x8d\xc6\xd1\xae\xeb^UFZ\xeb\xaa\xbc\x13c\xcc\r\xedv\xfbS\x18\xae\xeb\x8cF\xdfD\x0f\xa8\'\xea\xb7\xcaa\xcf\xac\xfb!9\xc6\xc1\xb7\xaa\xbf\x1cC\xffm\x81\xf1\xee\xb3Sq\x1e\xc4@M\xa7\x17\x04\xc14k\xed"\x92\xe7\x91<\x97d\xe5\x01-\x83\xc6~\x94\xe4\xdfbk\x86\xe0\x90>#\xd17Q\xbdb\xcc\xcf\x1c\xca\x14\xae\xeb\xba\x87\xb8\xae\xbb\x0f\xdef\xb6\xf3\xdb\x05*\x8f8\x924\xdb\x18\xb3\xa7\xa4\xa3\x8d1\xc7\xd5\xc56\x06\xc1\xa2p\xb1\xff\xe7\xfe\xfe\xfe\xa7\xcak\xd3=\xcf;\xc6q\x9c\x16\xde\x1e\xff|d:\x9d\xce\xaf\xb7b\n\xd7u\x17\xba\xae\xfb-\x00G\xe3\xedA\xe4\xdb\x0e,0\xf8\xfb\x98\xee\x93t\xbf\xb5\xf6o\xca\x93{\x84\xe2o">j\x8c\xf9\n\xea\x83w\xdb\x15\x92^w]\xf7\xdc\xc1L\x11\x18c.E\xc1\x10\xc0\xce\xbff\x9a*\xe4\x92\x1e\x95\xf4_J\x9f\x89\x05\x00\xcf\xf3\x96\x18c>\xcb!\x07\xa9\xecH\x90\xbc&M\xd3\x87\x06\x98\xc2\x04Ap&\x80\xabv$Q\xff\x0e\xf1:\xc9\x1fdY\xf6\xadA\xc5\xbcN\xb3\xd9\xbc\xd8q\x9c\xff\x06`\xc4J\xad\xed\tI+\xba\xdd\xee\xdfc\xe0\x7fI\xa7M\x9b6#M\xd3OU%\xb7\xee\xc4\xc4 \xe9^\x00_w\x1c\xe7\xf6$I\xde\xca\x19i6\x9b\x179\x8e\xf3E\xbc\x8d\x18\x02E\x8e\xc9\xd7PF\xb9\x1b\x00L\x92$\xe7\x1acv\xfe/\xe9$\xa1\xa2n\xf6~\x00?\xb2\xd6\xdeR\x9ew\x95\x03@\xab\xd5\xda\xcdZ{\x19\x8b\xbf\xc8z;1\x04\xac\xb5\x03Qn\x01@\xc3\xf3\xbc\xfdH\xfeW\xec\xc0\xff\x13\xfb\xb7\x8c2\x97\xe4I\x00\x0f\xe6y~g\xe9Q}\x13[\xea<\x9cV\xab\xb5\xc8Z\xfbe\x14\x07\x92m\xf70\xc0H\x90\xf4J\x96e\xff\x1b\x83*\xfc\x1by\x9e\xef\'\xe9N\x92\xdb\xb3$\xfe\xdf2"\x00kH\xae\x97\xf4;k\xed\xda\xf2\xdc\xa8\x18@\x9a$\xc9P7\xf2\x9ei\x9a\x9e\xc5\xe2\x7fW\xef\xc2\xdb\xcb\xaakZk\x7f\x9ce\xd9#\x18D\xd7\xff\x03\n&\x86@a\x1c\xc1z\x00\x00\x00\x00IEND\xaeB`\x82'
