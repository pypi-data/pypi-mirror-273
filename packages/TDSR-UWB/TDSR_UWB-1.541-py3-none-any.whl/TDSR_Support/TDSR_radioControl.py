from PyQt6.QtCore import QTimer
from json import loads
from time import time, sleep
from math import sqrt, log10
from numpy import power
from pathlib import Path
from base64 import b64encode, b64decode
from threading import Thread

__version__ = "1.541"

# Primary ranging functions
class rangeCmds():
    def __init__(self, gui):
        self.gui = gui
        self.appSetup()

# Shutdown signal triggers shutdown of radios and closing of any open logfiles.
    def closeApp(self):
        if self.running == 1:
            print("App closed while ranging, aborting run.")
            self.toggleRun()

    def rangingApp(self):
        if self.gui.connectedRequester == 1:
            self.rangingSetup('ranging')

# only runs once on startup. Initial setup for application
    def appSetup(self):
        self.running = 0
        self.rangeTimer = QTimer()
        # self.rangeTimer.setInterval(10)
        self.rangeTimer.timeout.connect(self.rangeRequest)
        self.networkTimer = QTimer()
        self.networkTimer.setInterval(10)
        self.networkTimer.timeout.connect(self.networkCheck)
        self.rangeArray = []
        self.rangeFilteredArray = []
        self.rangeFPPArray = []
        self.chartPointsX = []
        self.packetDisplay = None
        self.missedComms = 0

# Runs on startup and before each ranging run. Resets everything to known state.
    def rangingSetup(self, mode):
        # confirm radio is connected at each ranging start
        status = False
        self.gui.radioConnectReq()
        self.rangeCountValid = 0
        if self.gui.connectedRequester == 1:
            status, msg, addr = self.gui.radioReq.API.network_GetSlotMap_Request(self.gui.appSettings['reqRadio'])
            if msg:
                self.gui.windowNetwork.slotMap = msg['NETWORKING_GET_SLOT_MAP_CONFIRM']['slotMap']
            self.gui.appSettings['reqRadio'] = self.gui.dropMenuReqRadio.currentText()
            self.gui.appSettings['respRadio'] = self.gui.dropMenuRespRadio.currentText()
            self.gui.updateMemoryDepth()
            if (self.gui.dispReqID.text() == self.gui.dispRespID.text()) or self.gui.dispReqID.text() == "-":
                if self.gui.dispReqID.text() == "-":
                    text = "  == ERROR, invalid requester nodeID ==\n"
                else:
                    text = "  == ERROR, requester and responder must have different nodeIDs ==\n"
                self.gui.updateConsole(text)
                self.gui.dispRespID.setStyleSheet("QLineEdit {background-color: red;}")
                self.running = 1
                self.toggleRun()
            text = "-- Ready to Range\n"
            self.gui.updateConsole(text)
            self.nodeIPs =[]
            self.gui.plotX = []
            self.gui.plotY = []
            self.gui.plotYT = []
            self.gui.plotYB = []
            self.gui.yScalePos = 1
            self.gui.yScaleNeg = 100000
            self.gui.dataWindow.setYRange(self.gui.yScaleNeg,self.gui.yScalePos,padding = 0)
            self.gui.dataWindow.enableAutoRange(axis="x", enable = True)
            self.gui.dataWindowT.setYRange(self.gui.yScaleNeg,self.gui.yScalePos,padding = 0)
            self.gui.dataWindowT.enableAutoRange(axis="x", enable = True)
            self.gui.dataWindowB.setYRange(self.gui.yScaleNeg,self.gui.yScalePos,padding = 0)
            self.gui.dataWindowB.enableAutoRange(axis="x", enable = True)
            self.firstMsg = 0
            self.errors = 0
            self.packets = 0
            self.successRateRate = 0
            self.rangeArray = []
            self.rangeFilteredArray = []
            self.rxPowerWattsArray = []
            self.rxPowerArray = []
            self.rangeFPPWattsArray = []
            self.maxNoiseArray = []
            self.stdNoiseArray = []
            self.chartPointsX = []
            self.rxPowerArrayAll = []
            self.maxNoiseArrayAll = []
            self.stdNoiseArrayAll = []
            self.rangeArrayAll = []
            self.rangeFilteredArrayAll = []
            self.chartPointsXAll = []
            self.rangeValidSum = 0
            self.rangeFilteredValidSum = 0
            self.rangeRXPowerSum = 0
            self.rangeFPPowerSum = 0
            self.packetDisplay = None
            self.rangeCount = 0
            self.rangeCountValid = 0
            self.rangeTimeArray = []
            if self.gui.radioMode == 'idle':
                self.gui.updateRunTotal()
                self.nodeIPs.append(self.gui.appSettings['reqRadio'])
                self.targetNodes = int(self.gui.dispRespID.text())
                if self.gui.connectedResponder == 1:
                    self.gui.radioStateResp, addr = self.gui.radioResp.API.radio_GetState_Request(self.gui.appSettings['respRadio'])
                    self.gui.radioStateResp[list([self.gui.radioStateResp.keys()][0])[0]]['flags']  = ""
                    self.gui.radioStateResp[list([self.gui.radioStateResp.keys()][0])[0]]['state'] ="RADIO_STATE_RANGING"
                    self.gui.radioStateResp[list([self.gui.radioStateResp.keys()][0])[0]]['persistFlag'] = 1
                    self.gui.radioResp.API.radio_SetState_Request(self.gui.appSettings['respRadio'],self.gui.radioStateResp)
                else:
                    if mode != 'networking':
                        print("Unabled to connect to responder. Make sure it is in active mode.")
                        text =  "Unabled to connect to responder. Make sure it is in active mode.\n"
                        self.gui.updateConsole(text)
        if self.gui.connectedRequester == 1:
            status, packet, addr = self.gui.radioReq.API.radio_GetInfo_Request(self.gui.appSettings['reqRadio'])
            self.gui.radioStateReq, addr = self.gui.radioReq.API.radio_GetState_Request(self.gui.appSettings['reqRadio'])
            status = True
        else:   # If couldn't connect, then shutdown run and reset
            status = False
            if mode != 'networking':
                self.running = 1
                print("Ranging setup error, can't reach requester, aborting run.")
                self.rangeTimer.stop()
                self.toggleRun()
        if (self.gui.appSettings['reqRadio'] == self.gui.appSettings['respRadio']) and self.gui.appSettings['connectResp'] == 1:
            print("Ranging setup error. Primary and Secondary radios are the sane.")
            status = False
        return status

# Procedure for starting a new run or ending a current run depending on the state of self.running when togglerun is called.
    def toggleRun(self):
        if self.running == 0 and self.gui.radioMode == 'idle':
            for i in self.gui.radioReq.messageQueues:
                while not self.gui.radioReq.messageQueues[i].empty():
                    dump = self.gui.radioReq.messageQueues[i].get()
                    # print("dumping:",i)
            # print("Tx Len:", self.gui.radioReq.TxQueue.qsize())
            status = self.rangingSetup('ranging')
            if status == True:
                self.gui.windowNetwork.netXArray = []
                for i in range(len(self.gui.windowNetwork.netRangeArray)):
                    self.gui.windowNetwork.netRangeArray[i] = []
                    self.gui.windowNetwork.netPowerArray[i] = []
                    self.gui.windowNetwork.netMaxNoiseArray[i] = []
                    self.gui.windowNetwork.netStdNoiseArray[i] = []
                    self.gui.windowNetwork.netPlot1[i].setData(self.gui.windowNetwork.netXArray, self.gui.windowNetwork.netRangeArray[i])
                    self.gui.windowNetwork.netPlot2[i].setData(self.gui.windowNetwork.netXArray, self.gui.windowNetwork.netRangeArray[i])
                    self.gui.windowNetwork.netPlotT[i].setData(self.gui.windowNetwork.netXArray, self.gui.windowNetwork.netRangeArray[i])
                    self.gui.windowNetwork.netPlotB[i].setData(self.gui.windowNetwork.netXArray, self.gui.windowNetwork.netRangeArray[i])
                self.gui.plotYT = []
                self.gui.plotX = []
                self.gui.chartData1.setData(self.gui.plotX, self.gui.plotYT)
                self.gui.radioStateReq,addr = self.gui.radioReq.API.radio_GetState_Request(self.gui.appSettings['reqRadio'])
                self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['state'] = "RADIO_STATE_RANGING"
                self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['flags']  = ""
                self.gui.radioStateReq[list([self.gui.radioStateReq.keys()][0])[0]]['persistFlag'] = 1
                self.gui.radioReq.API.radio_SetState_Request(self.gui.appSettings['reqRadio'],self.gui.radioStateReq)
                self.gui.windowDataTransfer.dropMenuDestination.clear()
                self.gui.windowDataTransfer.dropMenuDestination.addItems([str(self.gui.appSettings['respID'])])
                self.gui.checkChartRange(None)
                self.running = 1
                self.gui.but_run.setText("Stop")
                self.gui.but_run.setStyleSheet("QPushButton {background-color: coral;}")
                if self.gui.connectedRequester == 0:
                    self.gui.radioConnectReq()
                if self.gui.connectedRequester == 1:
                    # self.rangeTimer.setInterval(int(self.gui.dispRangeDelay.text()))
                    self.runStartTime = time()
                    self.rangeTimer.start()
                    self.gui.rangingActive = True
                    self.gui.guiUpdateTimer.start()
                    text = "Executing " + str(self.gui.appSettings['rangeRequests']) + " Ranging Attempts\n"
                    self.gui.updateConsole(text)
                    self.gui.radioMode = 'ranging'
                    self.gui.radioCheckTimer.stop()
                else:
                    text = "Could not connect to requester radio, check cables and IP addresses.\n"
                    self.gui.updateConsole(text)
                    self.gui.radioMode = 'idle'
                    self.running = 0
                    self.gui.radioCheckTimer.start()
            else:
                text = "Could not connect to requester radio, check cables and IP addresses.\n"
                self.gui.updateConsole(text)
                self.gui.radioMode = 'idle'
                self.running = 0
                self.gui.radioCheckTimer.start()
        else:
            if self.gui.radioMode == 'networking':
                text = "=====\nRadio is in Network Mode.\n  Stop network before ranging\n=====\n"
                self.gui.updateConsole(text)
            else:
                self.rangeTimer.stop()
                self.runStopTime = time()
                self.running = 0
                # clear the stale messages
                for i in self.gui.radioReq.messageQueues:
                    while not self.gui.radioReq.messageQueues[i].empty():
                        dump = self.gui.radioReq.messageQueues[i].get()
                #         print("dumping:",i)
                # print("Tx Len:", self.gui.radioReq.TxQueue.qsize())
                self.gui.rangingActive = False
                print("Stopping Run")
                self.gui.but_run.setText("Start\nRanging")
                self.gui.but_run.setStyleSheet(self.gui.buttonSheetBlue)
                self.gui.logFile.closeLogFile()
                self.computeRunStats()
                self.gui.guiUpdateTimer.stop()
                self.gui.updateGUI()
                self.gui.radioMode = 'idle'
                self.gui.radioCheckTimer.start()

    def networkCheck(self):
        if self.gui.connectedRequester == 1:
            self.networkTimer.stop()
            while not self.gui.radioReq.messageQueues['RANGE_INFO'].empty():
                packet =  self.gui.radioReq.messageQueues['RANGE_INFO'].get()
                slot = int(packet['RANGE_INFO']['slotIdx'])
                self.gui.windowNetwork.processRange(slot,packet)
            while not self.gui.radioReq.messageQueues['DATA_INFO'].empty():
                packet =  self.gui.radioReq.messageQueues['DATA_INFO'].get()
                self.gui.windowDataTransfer.radioData.processNetworkDataInfo(packet)
            self.networkTimer.start()

# Requests range from designated responder nodeID.
    def rangeRequest(self):
        # self.rangeTimer.stop()
        if self.missedComms > 4:
            print("rangeRequest abort")
            self.gui.radioReq.disconnect()
            self.gui.dropMenuReqRadio.setCurrentIndex(0)
            self.missedComms = 0
            self.gui.windowDataTransfer.dataReadyStatus = -1
            self.gui.windowDataTransfer.packetList = []
            self.gui.windowDataTransfer.sendCount = 0
            self.gui.windowDataTransfer.txResendCount = 0
            self.gui.windowDataTransfer.packetListComplete = []
            self.gui.windowDataTransfer.radioData.packetTimer.stop()
            self.gui.windowDataTransfer.radioData.dataTimeoutTimer.stop()
        if self.gui.connectedRequester == 1:
            self.gui.rangeInProgress = 1
            # if there is data to send, append it to the ranging packet
            if self.gui.windowDataTransfer.radioData.dataReadyStatus > 0:
                data = self.gui.windowDataTransfer.radioData.getDataPacket()
            else:
                data = ""
            # if 0 then hold ranges to allow confirmation data packet to come in.
            if self.gui.windowDataTransfer.radioData.dataReadyStatus != 0:
                if len(data) > 0:
                    status, pkt, addr = self.gui.radioReq.API.range_Send_Request(self.gui.appSettings['reqRadio'],self.targetNodes, "4pkt TWR", "ENCODING_BASE64", data)
                    if status == False:
                        self.missedComms = self.missedComms + 1
                else:
                    status, pkt, addr = self.gui.radioReq.API.range_Send_Request(self.gui.appSettings['reqRadio'],self.targetNodes, "2pkt TWR", "ENCODING_BASE64", data)
                    if status == False:
                        self.missedComms = self.missedComms + 1
            if self.gui.windowDataTransfer.radioData.dataReadyStatus == 1:  # indicated last in transmission
                self.gui.windowDataTransfer.radioData.dataReadyStatus = 0   # enter hold until confirmation cycle
            self.startRange = time()
            # Once range request is set, wait for answer and process the data
            self.rangeProcessData(None)
        else:
            text = "== Not connected to Requester Radio" + self.gui.appSettings['reqRadio'] + " ==\n"
            self.gui.updateConsole(text)
            print("Ranging requested while not connected to requester, aborting run.")
            self.toggleRun()

# Processes ranging data when it comes in from the API
    def rangeProcessData(self, packet):
        if packet == None: # case for ranging mode
            try:
                packet = self.gui.radioReq.messageQueues['RANGE_INFO'].get(timeout = 0.2)
            except:
                # print("Miss")
                packet = {"RANGE_INFO":{"rangeStatus":4,"precisionRangeM":0.0,"rxPower":0.0}}
                packet['RANGE_INFO']['rangeStatus'] = 4
                packet['RANGE_INFO']['precisionRangeM'] = 0.0
                packet['RANGE_INFO']['filteredRangeM'] = 0.0
                packet['RANGE_INFO']['maxNoise'] = 0.0
                packet['RANGE_INFO']['stdNoise'] = 0.0
                pass
        # If count = desired requests then stop run, otherwise, range transaction is complete, start the next one.
            self.gui.rangeInProgress = False
            if self.rangeCount == self.gui.appSettings['rangeRequests']:
                print("Run Complete.")
                self.toggleRun()
            else:
                ...
                # self.rangeTimer.start()
        # Find starting place for message IDs and then determine packet count
            if self.firstMsg == 0:
                if packet['RANGE_INFO']['rangeStatus'] == 0  and packet['RANGE_INFO']['precisionRangeM'] != 0.0:
                    self.firstMsg = int(packet['RANGE_INFO']['msgId'])
            self.packets = self.rangeCount + 1
        # Count Ranging Errors and compute success rate, store them in the packet
            if packet['RANGE_INFO']['rangeStatus'] != 0 or packet['RANGE_INFO']['precisionRangeM'] == 0.0:
                # print("rangeProcessData range error")
                self.errors = self.errors + 1
            if self.rangeCount > 0:
                self.successRate = "%0.2f" % (100 - (100*(self.errors / self.packets)))
                # print(f"errors {self.errors}, count {self.packets}")
            else:
                self.successRate = "0"
            packet['RANGE_INFO']['packets'] = str(self.packets)
            packet['RANGE_INFO']['successRate'] = self.successRate
    # Build Range array, range attempt count, successful range count and sum. Used for final stats.
        self.rangeCount = self.rangeCount + 1
        tmpRxPower = 0
        tmpFPPower = 0
        if packet['RANGE_INFO']['rangeStatus'] == 0 and packet['RANGE_INFO']['precisionRangeM'] != 0.0:
            tmpRxPower = str(packet['RANGE_INFO']['rxPower'])
            if tmpRxPower != "-Infinity" and tmpRxPower != "-inf":
                tmpRxPower = tmpRxPower.split(".")
                if len(tmpRxPower) < 2:
                    print("Short Tmp:", tmpRxPower)
                else:
                    if len(tmpRxPower[1]) < 1:
                        print("Short Tmp[1]:", tmpRxPower)
                        tmpRxPower = float(tmpRxPower[0] + "." + tmpRxPower[1][:1])
                    else:
                        tmpRxPower = float(tmpRxPower[0] + "." + tmpRxPower[1][:1])
            else:  # this is a catch debug print for negative infinity rxPower
                print("Infinity Fail:", tmpRxPower)
                print("\n-Infinity Found")
                print("rxPower: ", str(packet['RANGE_INFO']['rxPower']))
                print("MaxGrowCIR: ", str(packet['RANGE_INFO']['maxGrowthCIR']))
                print("rxPreamCount: ", str(packet['RANGE_INFO']['rxPreamCount']))
                print("precRange: ", str(packet['RANGE_INFO']['precisionRangeM']))
                print("rangeStatus: ", str(packet['RANGE_INFO']['rangeStatus']))
                tmpRxPower = -120.0
            if tmpRxPower < -120:
                tmpRxPower = -120.0
            tmpRxPowerWatts = (10 ** (tmpRxPower/10)) / 1000
            tmpFPPower = str(packet['RANGE_INFO']['firstPathPower'])
            if tmpFPPower != "-Infinity" and tmpFPPower != "-inf":
                tmpFPPower = tmpFPPower.split(".")
                if len(tmpFPPower) < 2:
                    print("Short Tmp:", tmpFPPower)
                else:
                    if len(tmpFPPower[1]) < 1:
                        print("Short Tmp[1]:", tmpFPPower)
                        tmpFPPower = float(tmpFPPower[0] + "." + tmpFPPower[1][:1])
                    else:
                        tmpFPPower = float(tmpFPPower[0] + "." + tmpFPPower[1][:1])
            else:  # this is a catch debug print for negative infinity rxPower
                print("Infinity Fail:", tmpFPPower)
                print("\n-Infinity Found")
                print("rxPower: ", str(packet['RANGE_INFO']['rxPower']))
                print("MaxGrowCIR: ", str(packet['RANGE_INFO']['maxGrowthCIR']))
                print("rxPreamCount: ", str(packet['RANGE_INFO']['rxPreamCount']))
                print("precRange: ", str(packet['RANGE_INFO']['precisionRangeM']))
                print("rangeStatus: ", str(packet['RANGE_INFO']['rangeStatus']))
                tmpFPPower = -120.0
            if tmpFPPower < -120:
                tmpFPPower = -120.0
            tmpFPPowerWatts = (10 ** (tmpFPPower/10)) / 1000
            if self.gui.radioMode == 'ranging' and tmpRxPower != -120 and tmpFPPower != -120:
                self.rangeCountValid = self.rangeCountValid + 1
                self.rangeValidSum = self.rangeValidSum + float(packet['RANGE_INFO']['precisionRangeM'])
                self.rangeFilteredValidSum = self.rangeFilteredValidSum + float(packet['RANGE_INFO']['filteredRangeM'])
                self.rangeRXPowerSum = self.rangeRXPowerSum + tmpRxPowerWatts
                self.rangeFPPowerSum = self.rangeFPPowerSum + tmpFPPowerWatts
                self.rxPowerArray.append(tmpRxPower)
                self.rxPowerWattsArray.append(tmpRxPowerWatts)
                self.rangeFPPWattsArray.append(tmpFPPowerWatts)
                self.maxNoiseArray.append(int(packet['RANGE_INFO']['maxNoise']))
                self.stdNoiseArray.append(int(packet['RANGE_INFO']['stdNoise']))
                self.rangeArray.append(float(packet['RANGE_INFO']['precisionRangeM']))
                self.rangeFilteredArray.append(float(packet['RANGE_INFO']['filteredRangeM']))
                self.chartPointsX.append(int(self.rangeCount))
            self.gui.checkChartRange(packet)
            # self.gui.plotData()

        self.rxPowerArrayAll.append(tmpRxPower)
        self.maxNoiseArrayAll.append(int(packet['RANGE_INFO']['maxNoise']))
        self.stdNoiseArrayAll.append(int(packet['RANGE_INFO']['stdNoise']))
        self.rangeArrayAll.append(float(packet['RANGE_INFO']['precisionRangeM']))
        try:
            self.rangeFilteredArrayAll.append(float(packet['RANGE_INFO']['filteredRangeM']))
        except:
            print(packet)
        self.chartPointsXAll.append(int(self.rangeCount))
        # self.gui.checkChartRange(packet)
            # self.gui.plotData()
        if len(self.rangeArray) > int(self.gui.appSettings['memoryDepth']):
            self.rxPowerWattsArray = self.rxPowerWattsArray[1:]
            self.rxPowerArray = self.rxPowerArray[1:]
            self.rangeFPPWattsArray = self.rangeFPPWattsArray[1:]
            self.maxNoiseArray = self.maxNoiseArray[1:]
            self.stdNoiseArray = self.stdNoiseArray[1:]
            self.rangeArray = self.rangeArray[1:]
            self.rangeFilteredArray = self.rangeFilteredArray[1:]
            self.chartPointsX = self.chartPointsX[1:]
        if len(self.rangeArrayAll) > int(self.gui.appSettings['memoryDepth']):
            self.rxPowerArrayAll = self.rxPowerArrayAll[1:]
            self.maxNoiseArrayAll = self.maxNoiseArrayAll[1:]
            self.stdNoiseArrayAll = self.stdNoiseArrayAll[1:]
            self.rangeArrayAll = self.rangeArrayAll[1:]
            self.rangeFilteredArrayAll = self.rangeFilteredArrayAll[1:]
            self.chartPointsXAll = self.chartPointsXAll[1:]
    # Update GUI
        # self.gui.guiPacketUpdates(packet)
        self.packetDisplay = packet

# computes various stats abot the radio run upon completion. Prints output to GUI Console.
    def computeRunStats(self):
        if self.rangeCountValid > 0:
            rangeAvg = self.rangeValidSum / self.rangeCountValid
            rangeFilteredAvg = self.rangeFilteredValidSum / self.rangeCountValid
            rangeRXPowerWattsAvg = self.rangeRXPowerSum / self.rangeCountValid
            # print(rangeRXPowerWattsAvg)
            rangeFPPowerWattsAvg = self.rangeFPPowerSum / self.rangeCountValid
            # print(rangeFPPowerWattsAvg)
            devSquares = []
            sumSquares = 0
            for k in range(len(self.rangeArray)):
                devSquares.append((self.rangeArray[k] - rangeAvg) * (self.rangeArray[k] - rangeAvg))     # squares of the deviations
            for k in range(len(devSquares)):                                                                       # sum of the squares
                sumSquares = sumSquares + devSquares[k]
            variance = sumSquares / self.rangeCountValid
            rangeStdDev = "%0.2f" % (sqrt(variance)*1000)

            devSquares = []
            sumSquares = 0
            for k in range(len(self.rangeFilteredArray)):
                devSquares.append((self.rangeFilteredArray[k] - rangeAvg) * (self.rangeFilteredArray[k] - rangeFilteredAvg))     # squares of the deviations
            for k in range(len(devSquares)):                                                                       # sum of the squares
                sumSquares = sumSquares + devSquares[k]
            variance = sumSquares / self.rangeCountValid
            rangeFilteredStdDev = "%0.2f" % (sqrt(variance)*1000)

            devSquares = []
            sumSquares = 0
            for k in range(len(self.rxPowerWattsArray)):
                # print(self.rxPowerWattsArray[k], rangeRXPowerWattsAvg, self.rxPowerWattsArray[k] * 1e12, rangeRXPowerWattsAvg * 1e12)
                devSquares.append((self.rxPowerWattsArray[k] - rangeRXPowerWattsAvg) * (self.rxPowerWattsArray[k] - rangeRXPowerWattsAvg))     # squares of the deviations
            for k in range(len(devSquares)):                                                                       # sum of the squares
                sumSquares = sumSquares + devSquares[k]
            variance = sumSquares / self.rangeCountValid
            # print(sqrt(variance), rangeRXPowerWattsAvg)
            # print(sqrt(variance)/rangeRXPowerWattsAvg * 100)
            rxPowerStdDev = "%0.1f" % (sqrt(variance)/rangeRXPowerWattsAvg * 100)
            devSquares = []
            sumSquares = 0
            for k in range(len(self.rangeFPPWattsArray)):
                devSquares.append((self.rangeFPPWattsArray[k]  - rangeFPPowerWattsAvg) * (self.rangeFPPWattsArray[k]  - rangeFPPowerWattsAvg))     # squares of the deviations
            for k in range(len(devSquares)):                                                                       # sum of the squares
                sumSquares = sumSquares + devSquares[k]
            variance = sumSquares / self.rangeCountValid
            # print(sqrt(variance), rangeFPPowerWattsAvg)
            # print(sqrt(variance)/rangeFPPowerWattsAvg * 100)
            rangeFPPStdDev = "%0.1f" % (sqrt(variance)/rangeFPPowerWattsAvg * 100)
            rangeAvg = "%0.4f" % rangeAvg
            rangeFilteredAvg = "%0.4f" % rangeFilteredAvg
            rangeRXPower_dBmAvg = (10 * log10(rangeRXPowerWattsAvg)) + 30
            rangeFPPower_dBmAvg = (10 * log10(rangeFPPowerWattsAvg)) + 30
            rangeRXPower_dBmAvg = "%0.2f" % rangeRXPower_dBmAvg
            rangeFPPower_dBmAvg = "%0.2f" % rangeFPPower_dBmAvg
            text = "====\n"
            text = text + "Completed " + str(self.rangeCount) + " Ranging Attempts\n"
            runDuration = "%0.1f" % (self.runStopTime - self.runStartTime)
            text = text + "Run Duration: " + runDuration + " Seconds\n"
            tmp = "%0.1f" % (self.rangeCount / float(runDuration))
            text = text + "Avg Range Rate: " + tmp + " Hz\n"
            if self.errors == 1:
                text = text + "There was " + str(self.errors) + " error for a success rate of " + str(self.successRate) + "%\n"
            else:
                text = text + "There were " + str(self.errors) + " errors for a success rate of " + str(self.successRate) + "%\n"
            text = text + "Range Average: " + rangeAvg + "m   Standard Deviation: " + rangeStdDev + "mm\n"
            text = text + "Filtered Range Average: " + rangeFilteredAvg + "m   Standard Deviation: " + rangeFilteredStdDev + "mm\n"
            text = text + "rxPower Mean: " + rangeRXPower_dBmAvg + "dBm   Standard Deviation: +/-" + rxPowerStdDev + "%\n"
            text = text + "First Path Power Mean: " + rangeFPPower_dBmAvg + "dBm   Standard Deviation: +/-" + rangeFPPStdDev + "%\n"
            text = text + "====\n"
            self.gui.updateConsole(text)
        # Make sure we weren't overrunning the radio ranging rate
            if len(self.rangeTimeArray) > 0:
                avgRangeTime = 0
                for k in range(len(self.rangeTimeArray)):
                    avgRangeTime = avgRangeTime + self.rangeTimeArray[k]
                avgRangeTime = int(avgRangeTime / len(self.rangeTimeArray))
                print(avgRangeTime, int(self.gui.dispRangeDelay.text()))
                if avgRangeTime * 1.15 > int(self.gui.dispRangeDelay.text()):
                    avgRangeTime = int(avgRangeTime * 1.15) + 2
                    text = "Requested ranging rate is too fast, suggest at least " + str(avgRangeTime) + " ms"
                    self.gui.updateConsole(text)
                    self.gui.dispRangeDelay.setStyleSheet("QLineEdit {background-color: coral;}")
                else:
                    self.gui.dispRangeDelay.setStyleSheet("QLineEdit {background-color: lightgreen;}")
        else:
            text = "\n====\nWas not able to successfully range\n"
            self.gui.updateConsole(text)

# Primary ranging functions
class dataCmds():
    def __init__(self, gui):
        self.gui = gui
        self.respMsgTimer = QTimer()
        self.respMsgTimer.setInterval(150)
        self.respMsgTimer.timeout.connect(self.checkDataPacket_Resp)
        self.reqMsgTimer = QTimer()
        self.reqMsgTimer.setInterval(150)
        self.reqMsgTimer.timeout.connect(self.checkDataPacket_Req)
        self.networkDataTimer = QTimer()
        self.networkDataTimer.setInterval(10)
        self.networkDataTimer.timeout.connect(self.networkFileSend)
        if self.gui.connectedResponder == 1:
            self.respMsgTimer.start()
        if self.gui.connectedRequester == 1:
            self.reqMsgTimer.start()
        self.packetBuffer = ""
        self.sendCount = 0
        self.dataReadyStatus = -1
        self.packetList = []
        self.packetListComplete = []
        # self.rxMsgArray = []
        self.rxMsgList = list()
        self.fileName = ""
        self.fileType = ""
        self.lastMsgExpected = 0
        self.msgsReceived = 0
        # self.rxMissingArray = []
        self.rxMissingList = list()
        self.txResendCount = 0
        self.rxResendCount = 0
        self.rxPacketTotal = 0
        self.msgNum = 0
        self.lastRxNum = 0
        self.packetLength = 1000#800#975
        self.packetTimer = QTimer()
        self.packetTimer.setInterval(1)
        self.packetTimer.timeout.connect(self.dataPacketSend)
        # self.packetTimer.timeout.connect(self.dataStartTx)
        self.rxAbortTimer = QTimer()
        self.rxAbortTimer.setInterval(1000)
        self.rxAbortTimer.timeout.connect(self.rxAbort)
        self.txThreadCheckTimer = QTimer()
        self.txThreadCheckTimer.setInterval(100)
        self.txThreadCheckTimer.timeout.connect(self.txStartSend)
        self.rxThreadCheckTimer = QTimer()
        self.rxThreadCheckTimer.setInterval(100)
        self.rxThreadCheckTimer.timeout.connect(self.rxFinish)
        self.threadRunningTx = 0
        self.threadRunningRx = 0
        self.startBuild = 0
        self.stopBuild = 0
        self.dataTimeoutTimer = QTimer()
        self.dataTimeoutTimer.setInterval(2000)
        self.dataTimeoutTimer.timeout.connect(self.dataAbort)
        self.networkDataTXAbortTimer = QTimer()
        self.networkDataTXAbortTimer.setInterval(2000)
        self.networkDataTXAbortTimer.timeout.connect(self.networkDataAbort)
        self.networkDataRXAbortTimer = QTimer()
        self.networkDataRXAbortTimer.setInterval(5000)
        self.networkDataRXAbortTimer.timeout.connect(self.networkDataAbort)
        self.networkConfirmQueue = []
        self.slotMapTime = 0

    ####################
    # Network TX side commands
    ####################

    def networkFileSend(self):
        order = "queue"
        dest = self.gui.windowDataTransfer.dataDestination
        slot = self.gui.windowDataTransfer.dataDestinationSlot
        if len(self.networkConfirmQueue) == 0 and len(self.packetList) > 0:
            dataPacket = self.packetList[0]
            self.packetList = self.packetList[1:]
            self.sendCount = self.sendCount + 1
            command = {"retries":0, "msgType":"d","destination":dest, "slot":slot, "order":order, "msgNum":self.sendCount, "payload":dataPacket}
            # print("Sending:",command)
            if self.sendCount == 1:
                tmp = f"Sending: {len(self.packetList) + 1} packets\n"
                self.gui.updateConsole(tmp)
            # print(f"Sending: {self.sendCount}")
            self.networkConfirmQueue.append(command)
            try:
                status = self.gui.radioReq.API.dataSend_B64_Request(self.gui.appSettings['reqRadio'],dest, slot, order, dataPacket)
            except:
                pass
            self.networkDataTXAbortTimer.start()

    def reqSendTextData(self):
        text = self.gui.windowDataTransfer.dataTextInput.toPlainText()
        msgNum = 1
        text = f"t1,{msgNum},{text}"
        text = self.toBase64(text)
        self.gui.windowDataTransfer.updateDropMenuDest()
        dest = self.gui.windowDataTransfer.dataDestination
        slot = self.gui.windowDataTransfer.dataDestinationSlot
        order = "front"
        localIP = self.gui.appSettings['reqRadio']
        if self.gui.radioMode == 'networking':
            if self.gui.windowDataTransfer.dataBackSlot >= 0:
                command = {"retries":0, "msgType":"t", "destination":dest, "slot":slot, "order":order, "msgNum":msgNum, "payload":text}
                self.networkConfirmQueue.insert(0,command)
                self.networkDataTXAbortTimer.start()
            else:
                tmp = "Sending text but no confirm slot available\n"
                self.gui.updateConsole(tmp)
        else:
            tmp = "Sending text but confirms are unreliable in non-network mode\n"
            self.gui.updateConsole(tmp)
        try:
            status = self.gui.radioReq.API.dataSend_B64_Request(localIP, dest, slot, order, text)
        except:
            pass
        self.gui.windowDataTransfer.dataTextInput.setText("")

    ####################
    # Network RX side commands
    ####################

    def processNetworkDataInfo(self, packet):
        text = ""
        payload = ""
        msgNum = 0
        data = packet['DATA_INFO']['data']
        if data != "":
            fromID = packet['DATA_INFO']['sourceNodeId']
            toID = packet['DATA_INFO']['receivingNodeId']
            if toID == self.gui.radioReqNodeID:
                msgID = packet['DATA_INFO']['msgId']
                data = b64decode(data)
                data = data.decode('utf-8')
                # print(data)
                tmp = data.split(",", 1)        # Splits out type and message number
                if len(tmp) > 1:                # data packets as short as "msgInfo,Data"
                    msgType = tmp[0][0]         # First info byte is msg type t = text, d = data
                    # print("yo: ", tmp)
                    # print("yo2: ", tmp[0])
                    msgNum = int(tmp[0][1:])    # Rest of first entry is msgNum
                    if msgNum == 0:
                        print(f"msgNum0: \n\n{tmp}, \n\n{tmp[0]}\n\n{tmp[0][1:]}")
                    payload = tmp[1]
                    if msgNum > 1 and self.lastMsgExpected == 0:
                        print("processNetworkDataInfo")
                        print(f"Invalid First Network Data Message. Aborting\nPacket:\n {packet}\n\nData:\n{data}\n")
                        print(f"MsgNum: {msgNum}, LastExpected: {self.lastMsgExpected}\n\n")
                        self.rxAbort()
                        return True
                else:
                    text = "==  Invalid Message, Aborting Transfer  ==\n"
                    self.gui.updateConsole(text)
                    self.packetBuffer = ""
                    self.rxMsgList = list()
                    self.lastMsgExpected = 0
                    self.msgsReceived = 0
                    return True
                if msgType == "t":
                    self.processNetworkText(fromID, msgID, msgNum, payload)
                if msgType == "d":
                    self.processNetworkData(fromID, msgID, msgNum, payload)
                if msgType == "c":
                    self.processNetworkConfirm(fromID, msgID, msgNum, payload)
                if msgType == "a":
                    print("Received Abort Command")
                    self.processNetworkDataAbort(fromID, msgID, msgNum, payload)

    def processNetworkText(self, fromID, msgID, msgNum, payload):
        if msgNum == 1:
            print("Text Received")
            payload = payload.split(",", 1)  # first message second field includes total message count and text data
            data = payload[1]
        else:
            data = payload[1]                  # following messages only have text data in the second field
        if not self.gui.windowDataTransfer.isVisible():
            self.gui.windowDataTransfer.displayWindow()
        self.gui.windowDataTransfer.dataReqTextReceived.setText(data)
        self.sendConfirm("t", fromID, msgID, msgNum)
        return True

    def processNetworkData(self, fromID, msgID, msgNum, payload):
        # print(f"Network Data Incoming, message {msgNum} out of {self.lastMsgExpected}")
        msgNum = int(msgNum)
        self.sendConfirm("d", fromID, msgID, msgNum)
        if msgNum == 1:
            msg = payload.split(",", 3)
            # print(f"Updating last message from {self.lastMsgExpected} to {int(msg[0])}, using msg {msg}")
            self.lastMsgExpected = int(msg[0])    # Second field of message 1, field 1 = messages coming
            self.rxPacketTotal = self.lastMsgExpected
            self.rxResendCount = 0
            if msgNum > self.lastMsgExpected:
                print("processNetworkData")
                print("Invalid Message ID", msgNum, "out of", self.lastMsgExpected)
                self.rxAbort()
            if str(msg[1]) == "T":      # Second field of message 1, field 2 = messagee type
                self.fileType = "Text"
            else:
                self.fileType = "Binary"
            self.fileName = str(msg[2]) # Second field of message 1, field 2 = filename
            msg = msg[3]                # Second field of message 1, field 2 = data
            tmp = f"\n===\nReceiving {self.fileType} File: {self.fileName}, expecting {self.lastMsgExpected} packets\n"
            print(tmp)
            text = tmp
            self.gui.updateConsole(text)
            self.rxMsgList = list()
            for k in range(self.lastMsgExpected):
                self.rxMsgList.append("")  # create array to hold each message packet
            self.rxMsgList[0] = msg
            self.msgsReceived = self.msgsReceived + 1
            payload = msg
        self.rxMsgList[msgNum - 1] = payload
        self.msgsReceived = self.msgsReceived + 1
        if (self.msgsReceived % 50) == 0 and self.msgsReceived > 1:
            text = "Received " + str(self.msgsReceived) + " of " + str(self.lastMsgExpected) + " packets.\n"
            self.gui.updateConsole(text)
        # If not at last expected msg, keep looking. Else look for misses or call it complete.
        if int(msgNum) != int(self.lastMsgExpected):
            self.networkDataRXAbortTimer.start()
        # got to last expected message
        else:
            self.networkDataRXAbortTimer.stop()
            self.lastMsgExpected = 0
            self.sendConfirm("p", fromID, msgID, 0)  # p = pass... all done. msgNum = 0
            self.startBuild = time()
            if len(self.rxMissingList) == 0:
                self.packetBuffer = ""
                tmp = "Building file from packet array\n"
                self.gui.updateConsole(tmp)
                self.threadRunningRx = 1
                rxPacketBuild = Thread(target=self.threadRxPacketBuild, daemon=True)
                self.rxThreadCheckTimer.start()
                rxPacketBuild.start()
        return True

    ####################
    # Network TX/RX side confirm, resend, abort commands
    ####################
    def processNetworkDataAbort(self, fromID, msgID, msgNum, payload):
        self.sendConfirm("a", fromID, msgID, 0)
        self.dataReadyStatus = -1
        self.packetList = []
        self.sendCount = 0
        self.msgsReceived = 0
        self.txResendCount = 0
        self.packetListComplete = []
        self.networkDataTXAbortTimer.stop()
        self.networkDataRXAbortTimer.stop()
        print("Transfer aborted by sender")
        tmp = f"==== Transfer aborted by sender====\n"
        self.gui.updateConsole(tmp)

    def processNetworkConfirm(self, fromID, msgID, msgNum, payload):
        self.networkDataTXAbortTimer.stop()
        payload = payload.split(",")
        msgNum = payload[2]
        found = 0
        try:
            msgType = str(payload[1])
        except:
            print(payload)
        # print(f"msgNum: {msgNum}, type was: {msgType}")
        if str(msgType) == "t":
            print("Text receipt confirmed")
        else:
            # print(f"Confirm: {msgNum}")
            if (int(msgNum) % 50) == 0 and int(msgNum) > 1:
                text = f"Confirmed {msgNum} of {str(int(msgNum) + len(self.packetList))} packets.\n"
                self.gui.updateConsole(text)
        if (msgType == "p" or msgType == "a") and int(msgNum) == 0:
            if msgType == "a":
                self.dataReadyStatus = -1
                self.packetList = []
                self.sendCount = 0
                self.txResendCount = 0
                self.packetListComplete = []
                self.networkDataTXAbortTimer.stop()
                self.networkDataRXAbortTimer.stop()
                self.networkConfirmQueue = []
                print("Transfer aborted by sender")
                text = f"==== Transfer abort confirmed ====\n"
                self.gui.updateConsole(text)
                print(text)
            else:
                # text = "Transfer Complete"
                self.sendFinish = time()
                tmp = "File Send Complete\n"
                tmp = tmp + f"\n{self.txResendCount} packets resent out of {str(len(self.packetListComplete))}\n"
                success = "%0.2f" % (((len(self.packetListComplete) - self.txResendCount) / len(self.packetListComplete)) * 100)
                tmp = tmp = tmp + "Data Packet Success = " + success + "%\n"
                print(tmp)
                self.gui.updateConsole(tmp)
                tmp = f"Transmission Time: {(self.sendFinish - self.sendStart):.1f} seconds\n"
                print(tmp)
                self.gui.updateConsole(tmp)
                dataRate = int((self.fileLength * 8) / (self.sendFinish - self.sendStart))
                tmp = f"Transfer Bits / Sec: {dataRate:,}\n"
                print(tmp)
                # tmp = f"Bits / Sec: {tmp:,}\n  Complete\n"
                self.gui.updateConsole(tmp)
                self.resendCount = 0
                self.dataReadyStatus = -1
                self.packetList = []
                self.sendCount = 0
                self.txResendCount = 0
                self.packetListComplete = []
                self.networkDataTXAbortTimer.stop()
                self.networkDataRXAbortTimer.stop()
                self.networkConfirmQueue = []
            self.gui.windowDataTransfer.but_fileSend.setText("Send")
            self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: SteelBlue; color: GhostWhite;}")
        else:
            if len(self.networkConfirmQueue) > 0:
                for i in range(len(self.networkConfirmQueue)):
                    if int(self.networkConfirmQueue[i]["destination"]) == int(fromID) and int(self.networkConfirmQueue[i]["msgNum"]) == int(msgNum):
                        if str(msgType) == str(self.networkConfirmQueue[i]["msgType"]):
                            # print("deleting:",self.networkConfirmQueue[i]["msgNum"] )
                            del self.networkConfirmQueue[i]
                            found = 1
                            if len(self.packetList) > 0:
                                self.networkFileSend()
                            break
            if found == 0:
                print("Got second confirm, so must have missed the first")
                # print("Got confirm but message was not in queue")
                # print("payload:", payload)
                # print("fromID:", fromID)
                # print("msgType:", msgType)
                # for i in range(len(self.networkConfirmQueue)):
                #     print("qLine:",self.networkConfirmQueue[i])
                #     print("qfrom:", self.networkConfirmQueue[i]["destination"])
                #     print("qNum:", self.networkConfirmQueue[i]["msgNum"])
                #     print()

    def sendConfirm(self, msgType, fromID, msgID, msgNum):
        msg = f"c1,{str(msgID)},{str(msgType)},{str(msgNum)}"
        msg = self.toBase64(msg)
        dest = fromID
        if str(msgType) == "p":
            order = "queue"
        else:
            order = "front"
        slotFound = False
        for k in range(len(self.gui.windowNetwork.localSlots)):
            if self.gui.windowNetwork.localSlots[k][1] == fromID:
                slot = self.gui.windowNetwork.localSlots[k][0]
                slotFound = True
        if slotFound == True:
            try:
                status = self.gui.radioReq.API.dataSend_B64_Request(self.gui.appSettings['reqRadio'], dest, slot, order, msg)
            except:
                pass
            if str(msgType) == "t" or str(msgType) == "a":
                if str(msgType) == "t":
                    print("Confirming Text Message")
                else:
                    print("Confirming Tranfer Abort")
            else:
                # print(f"Confirming: {msgNum} out of {self.lastMsgExpected}")
                        ...
        else:
            tmp = "== Received Data Message but ==\n"
            self.gui.updateConsole(tmp)
            tmp = "== no return slot available  ==\n"
            self.gui.updateConsole(tmp)

    def networkDataResend(self):
        self.networkDataTXAbortTimer.stop()
        if len(self.networkConfirmQueue) > 0:
            command = self.networkConfirmQueue[0]
            self.networkConfirmQueue = self.networkConfirmQueue[1:]
            # resends oldest data in resend queue to the front of the transmit line
            print(f"### Resending {command['msgNum']} ###")
            self.txResendCount = self.txResendCount + 1
            localIP = self.gui.appSettings['reqRadio']
            try:
                status = self.gui.radioReq.API.dataSend_B64_Request(localIP, command["destination"], command["slot"], "front", command["payload"])
            except:
                pass
            command["retries"] = command["retries"] + 1
            self.networkConfirmQueue.append(command)
            self.networkDataTXAbortTimer.start()

    def networkDataAbort(self):
        # print(force)
        # print("Queue", self.networkConfirmQueue)
        if len(self.networkConfirmQueue) > 0:
            if int(self.networkConfirmQueue[0]["retries"]) < 5:
                self.networkDataResend()
            else:
                self.dataReadyStatus = -1
                self.packetList = []
                self.sendCount = 0
                self.txResendCount = 0
                self.packetListComplete = []
                self.networkDataTXAbortTimer.stop()
                self.networkDataRXAbortTimer.stop()
                print("Timeout with maximum retries. Aborting transfer.")
                tmp = f"====\nTransfer timeout with maximum retries.\nAborting Transfer, resuming ranging\n====\n"
                self.gui.updateConsole(tmp)
                self.gui.windowDataTransfer.but_fileSend.setText("Send")
                self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: SteelBlue color: GhostWhite;}")
        else:
            self.dataReadyStatus = -1
            self.packetList = []
            self.sendCount = 0
            self.txResendCount = 0
            self.packetListComplete = []
            self.networkDataTXAbortTimer.stop()
            self.networkDataRXAbortTimer.stop()
            print("Transfer timeout and confirm queue empty. Aborting transfer.")
            tmp = f"====\nTranser timeout and confirm queue empty.\nAborting Transfer, resuming ranging\n====\n"
            self.gui.updateConsole(tmp)
            self.gui.windowDataTransfer.but_fileSend.setText("Send")
            self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: SteelBlue color: GhostWhite;}")

    def sendNetworkDataAbort(self):
        msgNum = 0
        msgType = "a"
        msgID = 1
        msg = f"a1,{str(msgID)},{str(msgType)},{str(msgNum)}"
        msg = self.toBase64(msg)
        self.gui.windowDataTransfer.updateDropMenuDest()
        dest = self.gui.windowDataTransfer.dataDestination
        slot = self.gui.windowDataTransfer.dataDestinationSlot
        order = "front"
        localIP = self.gui.appSettings['reqRadio']
        command = {"retries":0, "msgType":"a", "destination":dest, "slot":slot, "order":order, "msgNum":msgNum, "payload":msg}
        self.networkConfirmQueue.insert(0,command)
        self.networkDataTXAbortTimer.start()
        try:
            status = self.gui.radioReq.API.dataSend_B64_Request(localIP, dest, slot, order, msg)
        except:
            pass

    ####################
    # Ranging and Data Mode Specific Commands
    ####################

    def checkDataPacket_Req(self):
        self.reqMsgTimer.stop()
        while not self.gui.radioReq.messageQueues['DATA_INFO'].empty():
            packet = self.gui.radioReq.messageQueues['DATA_INFO'].get(timeout = 0.05)
            self.processReqData(packet)
        self.reqMsgTimer.start()

    def checkDataPacket_Resp(self):
        self.respMsgTimer.stop()
        while not self.gui.radioResp.messageQueues['DATA_INFO'].empty():
            packet = self.gui.radioResp.messageQueues['DATA_INFO'].get(timeout = 0.05)
            self.processRespData(packet)
        self.respMsgTimer.start()

    def processReqData(self,packet):
        self.rxAbortTimer.stop()
        text = ""
        # print("data packet", packet)
        data = packet['DATA_INFO']['data']
        fromID = packet['DATA_INFO']['sourceNodeId']
        toID = packet['DATA_INFO']['receivingNodeId']
        if toID == self.gui.radioReqNodeID:
            if data != "":
                data = b64decode(data)
                data = data.decode('utf-8')
                # print(data)
                tmp = data.split(",", 1)        # Splits out type and message number
                if len(tmp) > 1:                # data packets as short as "msgInfo,Data"
                    msgType = tmp[0][0]         # First info byte is msg type t = text, d = data
                    self.msgNum = int(tmp[0][1:])    # Rest of first entry is msgNum
                    if self.msgNum > 1 and self.lastMsgExpected == 0:
                        print(f"Invalid First Message(Req). Aborting\n  Packet:\n {packet}\n\n{data}\n\n")
                        self.rxAbort()
                        return True
                    if msgType == "c":
                        missedPackets = tmp[1]
                        done = self.transmissionConfirm(missedPackets)
                        return done
                    if msgType == "a":
                        self.processDataAbort()
                    if msgType == "t":
                        tmp = tmp[1]
                        if self.msgNum == 1:
                            tmp = tmp.split(",", 1)  # first message second field includes total message count and text data
                            self.lastMsgExpected = int(tmp[0])
                            data = tmp[1]
                        else:
                            data = tmp                  # following messages only have text data in the second field
                        if not self.gui.windowDataTransfer.isVisible():
                            self.gui.windowDataTransfer.displayWindow()
                        self.gui.windowDataTransfer.dataReqTextReceived.setText(data)
                        if self.msgNum > self.lastMsgExpected:
                            print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                            self.rxAbort()
                        return True
                    if msgType == "d":
                        msg = tmp[1]                    # grab the second field. It's either all data or it breaks out info in msg 1
                        if self.msgNum == 1:
                            msg = msg.split(",", 3)
                            self.lastMsgExpected = int(msg[0])    # Second field of message 1, field 1 = messages coming
                            self.rxPacketTotal = self.lastMsgExpected
                            self.rxResendCount = 0
                            if self.msgNum > self.lastMsgExpected:
                                print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                                self.rxAbort()
                            if str(msg[1]) == "T":      # Second field of message 1, field 2 = messagee type
                                self.fileType = "Text"
                            else:
                                self.fileType = "Binary"
                            self.fileName = str(msg[2]) # Second field of message 1, field 2 = filename
                            msg = msg[3]                # Second field of message 1, field 2 = data
                            tmp = "\n===\nReceiving " + self.fileType + " File: " + self.fileName + "\n"
                            print(tmp)
                            text = tmp
                            self.gui.updateConsole(text)
                            self.rxMsgList = list()
                            for k in range(self.lastMsgExpected):
                                self.rxMsgList.append("")  # create array to hold each message packet
                            self.rxMsgList[0] = msg
                            self.msgsReceived = self.msgsReceived + 1
                        try:
                            self.rxMsgList[self.msgNum - 1] = msg
                            self.msgsReceived = self.msgsReceived + 1
                        except:
                            print("rxMsgList Length:", len(self.rxMsgList))
                            print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                            self.rxAbort()
                        if (self.msgsReceived % 250) == 0 and self.msgsReceived > 1:
                            text = "Received " + str(self.msgsReceived) + " of " + str(self.lastMsgExpected) + " packets.\n"
                            self.gui.updateConsole(text)
                        # If not at last expected msg, keep looking. Else look for misses or call it complete.
                        if int(self.msgNum) != int(self.lastMsgExpected):
                            self.rxAbortTimer.start()
                        # got to last expected message, did we miss any or are we done?
                        else:
                            # check for missed packets
                            self.rxMissingList = list()
                            self.lastMsgExpected = 0
                            for k in range(len(self.rxMsgList)):
                                if self.rxMsgList[k] == "":
                                    self.rxMissingList.append(k + 1)   # store the array index + 1
                                    self.lastMsgExpected = k + 1        # set to message number
                                    if len(self.rxMissingList) == 75:
                                        print("Grabbed first 75 missing packets")
                                        break
                            if len(self.rxMissingList) < 75:
                                print(f"Grabbed final {str(len(self.rxMissingList))} missing packets")
                                if len(self.rxMissingList) > 0:
                                    self.lastMsgExpected = self.rxMissingList[len(self.rxMissingList)-1]
                                    print("New Last should be:", self.lastMsgExpected)
                                else:
                                    self.lastMsgExpected = 0
                            self.rxResendCount = self.rxResendCount + len(self.rxMissingList)
                            # if we found misses, then ask for a resend of all of them
                            slot = self.gui.windowDataTransfer.dataDestinationSlot
                            dest = self.gui.windowDataTransfer.dataDestination
                            src = self.gui.appSettings['reqRadio']
                            order = "queue"
                            if self.lastMsgExpected != 0:
                                print("Requesting following missed packets:", self.rxMissingList)
                                tmp = "c1," + str(self.rxMissingList)
                                # print(tmp)
                                tmp = tmp.encode()
                                tmp = b64encode(tmp)
                                tmp = tmp.decode('utf-8')
                                slot = self.gui.windowDataTransfer.dataDestinationSlot
                                # print(src, dest, slot, order, tmp)
                                self.rxAbortTimer.start()
                                try:
                                    status = self.gui.radioReq.API.dataSend_B64_Request(src, dest, slot, order, tmp)
                                except:
                                    pass
                                # status = self.gui.radioReq.API.dataSend_B64_Request(self.gui.appSettings['reqRadio'],int(self.gui.windowDataTransfer.dropMenuDestination.currentText()), tmp)
                            # if we didn't find any misses, then save the file.
                            else:
                                tmp = "c1," + str(self.rxMissingList)
                                tmp = tmp.encode()
                                tmp = b64encode(tmp)
                                tmp = tmp.decode('utf-8')
                                try:
                                    status = self.gui.radioReq.API.dataSend_B64_Request(src, dest, slot, order, tmp)
                                except:
                                    pass
                                self.startBuild = time()
                                if len(self.rxMissingList) == 0:
                                    self.packetBuffer = ""
                                    tmp = "Building file from packet array\n"
                                    self.gui.updateConsole(tmp)
                                    self.threadRunningRx = 1
                                    rxPacketBuild = Thread(target=self.threadRxPacketBuild, daemon=True)
                                    self.rxThreadCheckTimer.start()
                                    rxPacketBuild.start()
                        return True
                else:
                    text = "==  Invalid Message, Aborting Transfer  ==\n"
                    self.gui.updateConsole(text)
                    self.packetBuffer = ""
                    self.rxMsgList = list()
                    self.lastMsgExpected = 0
                    self.msgsReceived = 0
                    return True

    def processRespData(self,packet):
        self.rxAbortTimer.stop()
        text = ""
        # print("data packet", packet)
        data = packet['DATA_INFO']['data']
        fromID = packet['DATA_INFO']['sourceNodeId']
        toID = packet['DATA_INFO']['receivingNodeId']
        if toID == self.gui.radioRespNodeID:
            if data != "":
                data = b64decode(data)
                srcNode = packet['DATA_INFO']['sourceNodeId']
                data = data.decode('utf-8')
                # print(data)
                tmp = data.split(",", 1)        # Splits out type and message number
                if len(tmp) > 1:                # data packets as short as "msgInfo,Data"
                    msgType = tmp[0][0]         # First info byte is msg type t = text, d = data
                    self.msgNum = int(tmp[0][1:])    # Rest of first entry is msgNum
                    # print("processRespData msgNum:",self.msgNum)
                    if self.msgNum > 1 and self.lastMsgExpected == 0:
                        print(f"Invalid First Message(Resp). Aborting\n  Packet:\n {packet}\n\n{data}\n\n")
                        self.rxAbort()
                        return True
                    if msgType == "c":
                        missedPackets = tmp[1]
                        done = self.transmissionConfirm(missedPackets)
                        return done
                    if msgType == "a":
                        self.processDataAbort()
                    if msgType == "t":
                        tmp = tmp[1]
                        if self.msgNum == 1:
                            tmp = tmp.split(",", 1)  # first message second field includes total message count and text data
                            self.lastMsgExpected = int(tmp[0])
                            data = tmp[1]
                        else:
                            data = tmp                  # following messages only have text data in the second field
                        if not self.gui.windowDataTransfer.isVisible():
                            self.gui.windowDataTransfer.displayWindow()
                        self.gui.windowDataTransfer.dataRespTextReceived.setText(data)
                        if self.msgNum > self.lastMsgExpected:
                            print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                            self.rxAbort()
                        return True
                    if msgType == "d":
                        msg = tmp[1]                    # grab the second field. It's either all data or it breaks out info in msg 1
                        if self.msgNum == 1:
                            msg = msg.split(",", 3)
                            self.lastMsgExpected = int(msg[0])    # Second field of message 1, field 1 = messages coming
                            self.rxPacketTotal = self.lastMsgExpected
                            self.rxResendCount = 0
                            if self.msgNum > self.lastMsgExpected:
                                print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                                self.rxAbort()
                            if str(msg[1]) == "T":      # Second field of message 1, field 2 = messagee type
                                self.fileType = "Text"
                            else:
                                self.fileType = "Binary"
                            self.fileName = str(msg[2]) # Second field of message 1, field 2 = filename
                            msg = msg[3]                # Second field of message 1, field 2 = data
                            tmp = "\n===\nReceiving " + self.fileType + " File: " + self.fileName + "\n"
                            print(tmp)
                            text = tmp
                            self.gui.updateConsole(text)
                            self.rxMsgList = list()
                            for k in range(self.lastMsgExpected):
                                self.rxMsgList.append("")  # create array to hold each message packet
                            self.rxMsgList[0] = msg
                            self.msgsReceived = self.msgsReceived + 1
                        try:
                            self.rxMsgList[self.msgNum - 1] = msg
                            self.msgsReceived = self.msgsReceived + 1
                        except:
                            print("rxMsgList Length:", len(self.rxMsgList))
                            print("Invalid Message ID", self.msgNum, "out of", self.lastMsgExpected)
                            self.rxAbort()
                        if (self.msgsReceived % 250) == 0 and self.msgsReceived > 1:
                            text = "Received " + str(self.msgsReceived) + " of " + str(self.lastMsgExpected) + " packets.\n"
                            self.gui.updateConsole(text)
                        # If not at last expected msg, keep looking. Else look for misses or call it complete.
                        if int(self.msgNum) != int(self.lastMsgExpected):
                            self.rxAbortTimer.start()
                        # got to last expected message, did we miss any or are we done?
                        else:
                            # check for missed packets
                            self.rxMissingList = list()
                            self.lastMsgExpected = 0
                            for k in range(len(self.rxMsgList)):
                                if self.rxMsgList[k] == "":
                                    self.rxMissingList.append(k + 1)   # store the array index + 1
                                    self.lastMsgExpected = k + 1        # set to message number
                                    if len(self.rxMissingList) == 75:
                                        print("Grabbed first 75 missing packets")
                                        break
                            if len(self.rxMissingList) < 75:
                                print(f"Grabbed final {str(len(self.rxMissingList))} missing packets")
                                if len(self.rxMissingList) > 0:
                                    self.lastMsgExpected = self.rxMissingList[len(self.rxMissingList)-1]
                                    print("New Last should be:", self.lastMsgExpected)
                                else:
                                    self.lastMsgExpected = 0
                            self.rxResendCount = self.rxResendCount + len(self.rxMissingList)
                            # if we found misses, then ask for a resend of all of them
                            slot = self.gui.windowDataTransfer.dataDestinationSlot
                            dest = self.gui.windowDataTransfer.dataDestination
                            src = self.gui.appSettings['reqRadio']
                            order = "queue"
                            if self.lastMsgExpected != 0:
                                print("Requesting following missed packets:", self.rxMissingList)
                                tmp = "c1," + str(self.rxMissingList)
                                tmp = tmp.encode()
                                tmp = b64encode(tmp)
                                tmp = tmp.decode('utf-8')
                                slot = self.gui.windowDataTransfer.dataDestinationSlot
                                self.rxAbortTimer.start()
                                try:
                                    status = self.gui.radioReq.API.dataSend_B64_Request(src, dest, slot, order, tmp)
                                except:
                                    pass
                            # if we didn't find any misses, then save the file.
                            else:
                                tmp = "c1," + str(self.rxMissingList)
                                tmp = tmp.encode()
                                tmp = b64encode(tmp)
                                tmp = tmp.decode('utf-8')
                                try:
                                    status = self.gui.radioReq.API.dataSend_B64_Request(src, dest, slot, order, tmp)
                                except:
                                    pass
                                self.startBuild = time()
                                if len(self.rxMissingList) == 0:
                                    self.packetBuffer = ""
                                    tmp = "Building file from packet array\n"
                                    self.gui.updateConsole(tmp)
                                    self.threadRunningRx = 1
                                    rxPacketBuild = Thread(target=self.threadRxPacketBuild, daemon=True)
                                    self.rxThreadCheckTimer.start()
                                    rxPacketBuild.start()
                        return True
                else:
                    text = "==  Invalid Message, Aborting Transfer  ==\n"
                    self.gui.updateConsole(text)
                    self.packetBuffer = ""
                    self.rxMsgList = list()
                    self.lastMsgExpected = 0
                    self.msgsReceived = 0
                    return True

    # This is called by a packet timer that sends out all of the packets in self.packetArray
    def dataPacketSend(self):
        # self.packetTimer.stop()
        if not self.gui.rangingActive:
            # while self.sendCount != (len(self.packetList)):
            dataPacket = self.getDataPacket()
            order = "queue"
            dest = self.gui.windowDataTransfer.dataDestination
            msgNum = self.sendCount
            slot = 0
            try:
                status = self.gui.radioReq.API.dataSend_B64_Request(self.gui.appSettings['reqRadio'],dest, slot, order, dataPacket)
            except:
                pass

    def getDataPacket(self):
        dataPacket = self.packetList[self.sendCount]
        if self.sendCount != (len(self.packetList)-1):
            if (self.sendCount % 250) == 0 and self.sendCount > 1:
                text = "Sent " + str(self.sendCount) + " of " + str(len(self.packetList)) + " packets.\n"
                self.gui.updateConsole(text)
        else:
            self.dataReadyStatus = 1 # hold for checks
            self.dataTimeoutTimer.start()
            self.sendFinish = time()
            self.gui.windowDataTransfer.but_fileSend.setText("Send")
            self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: SteelBlue; color: GhostWhite;}")
            print(f"Transmission Time: {(self.sendFinish - self.sendStart):.1f} seconds")
            tmp = int((self.fileLength * 8) / (self.sendFinish - self.sendStart))
            print("Transfer Bits / Sec:", tmp)
            self.packetTimer.stop()
            tmp = f"Bits / Sec: {tmp:,}\n  Complete\n"
            self.gui.updateConsole(tmp)
        self.sendCount = self.sendCount + 1
        return dataPacket

    def dataAbort(self):
        self.dataReadyStatus = -1
        self.packetList = []
        self.sendCount = 0
        self.txResendCount = 0
        self.packetListComplete = []
        self.packetTimer.stop()
        self.dataTimeoutTimer.stop()
        print("Aborting Transfer, resuming ranging")
        tmp = f"====\nDid not receive final acknowledge\nAborting Transfer, resuming ranging\n====\n"
        self.gui.updateConsole(tmp)

    def transmissionConfirm(self, missedPackets):
        self.dataTimeoutTimer.stop()
        print("Retransmit Packet Requests:", missedPackets)
        if missedPackets != [] and missedPackets != "[]":
            missedPackets = missedPackets[1:len(missedPackets)-1]
            missedPackets = missedPackets.split(",")
            tmp = list()
            for k in range(len(missedPackets)):  # missed packets are message numbers, which are array indexes + 1
                tmp.append(self.packetListComplete[int(missedPackets[k])-1]) # message location in array is message number - 1
            print("New Packet Array to Send")
            # print("Resend tmp len", tmp[0])
            self.txResendCount = self.txResendCount + len(tmp)
            text = "Retransmitting Missing Packets\n"
            self.gui.updateConsole(text)
            self.packetList = list()
            self.packetList = tmp
            # print("Resend PacketList Length:", self.packetList[0])
            self.dataReadyStatus = 2 #resume transmission for resend array
            self.sendCount = 0
            self.packetTimer.start()
            self.dataTimeoutTimer.start()
        else:
            tmp = f"\n{self.txResendCount} packets resent out of {str(len(self.packetListComplete))}\n"
            success = "%0.2f" % (((len(self.packetListComplete) - self.txResendCount) / len(self.packetListComplete)) * 100)
            tmp = tmp = tmp + "Data Packet Success = " + success + "%\n"
            tmp = tmp + "File Send Complete\n"
            self.gui.updateConsole(tmp)
            self.packetList = []
            self.sendCount = 0
            self.txResendCount = 0
            self.packetListComplete = []
            self.dataReadyStatus = -1 # Signified Transfer Complete
        return True

    def sendDataAbort(self):
        text = "\n== Transfer aborted by sender ==\n"
        print(text)
        self.gui.updateConsole(text)
        self.dataReadyStatus = -1
        self.packetList = []
        self.sendCount = 0
        self.txResendCount = 0
        self.packetListComplete = []
        self.packetTimer.stop()
        self.dataTimeoutTimer.stop()
        msgNum = 0
        msgType = "a"
        msgID = 1
        msg = f"a1,{str(msgID)},{str(msgType)},{str(msgNum)}"
        msg = self.toBase64(msg)
        self.gui.windowDataTransfer.updateDropMenuDest()
        dest = self.gui.windowDataTransfer.dataDestination
        slot = 0
        order = "front"
        localIP = self.gui.appSettings['reqRadio']
        try:
            status = self.gui.radioReq.API.dataSend_B64_Request(localIP, dest, slot, order, msg)
        except:
            pass

    def processDataAbort(self):
        self.rxAbortTimer.stop()
        text = "\n== Transfer aborted by sender ==\n"
        print(text)
        self.gui.updateConsole(text)
        self.packetBuffer = ""
        self.rxMsgArray = []
        self.lastMsgExpected = 0
        self.msgsReceived = 0

    def rxAbort(self):
        self.rxAbortTimer.stop()
        text = "== Last Received: " + str(self.msgNum) + " of " + str(self.lastMsgExpected) + "==\n"
        text = text + "== Transfer Timeout, Aborting ==\n"
        self.gui.updateConsole(text)
        self.packetBuffer = ""
        self.rxMsgArray = []
        self.lastMsgExpected = 0
        self.msgsReceived = 0

    ####################
    # TX Packet Prep for sending
    ####################
    # This gets a send started by figuring out what to send, what type of data it is, and then makes
    #   a packet array that contains all the packets. It then starts a transmission timer for the
    #   dataPacketSend module to send them out.
    def reqSendBase64File(self):
        if self.sendCount != 0:
            self.gui.windowDataTransfer.but_fileSend.setText("Send")
            self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: SteelBlue; color: GhostWhite;}")
            if self.gui.radioMode == "networking":
                self.sendNetworkDataAbort()
            else:
                self.sendDataAbort()
        else:
            self.gui.windowDataTransfer.updateDropMenuDest()
            if self.gui.windowDataTransfer.dataBackSlot >= 0 or self.gui.radioMode != "networking":
                if self.gui.windowDataTransfer.dispfileSelect.text() != "":
                    test = Path(str(self.gui.windowDataTransfer.dispfileSelect.text()))
                    if test.is_file() == True:
                        tmp = str(self.gui.windowDataTransfer.dispfileSelect.text())
                        tmp = tmp.split("/")
                        tmp = tmp[len(tmp) - 1]
                        self.fileName = tmp
                        tmp = "\n===\nSending: " + str(self.gui.windowDataTransfer.dispfileSelect.text()) + "\n"
                        self.gui.updateConsole(tmp)
                        file = open(self.gui.windowDataTransfer.dispfileSelect.text(), "rb")
                        text = file.read()
                        self.fileLength = len(text)
                        print("Initial Len", len(text))
                        try:
                            procFileData = text.decode()
                            print("ACSII Detected")
                            self.fileType = "T"
                        except:
                            print("Binary Detected")
                            self.fileType = "B"
                            procFileData = b64encode(text)
                            procFileData = procFileData.decode('utf-8')
                        print(f"Sending File: {self.fileName}")
                        tmp = "Preparing Packet Array\n"
                        self.gui.updateConsole(tmp)
                        self.gui.windowDataTransfer.but_fileSend.setText("Abort")
                        self.gui.windowDataTransfer.but_fileSend.setStyleSheet("QPushButton {background-color: coral; color: GhostWhite;}")
                        self.threadRunningTx = 1
                        txPacketBuild = Thread(target=self.threadTxPacketBuild(procFileData), daemon=True)
                        self.startBuild = time()
                        self.txThreadCheckTimer.start()
                        txPacketBuild.start()
                    else:
                        tmp = "== Invalid Filename Selected ==\n"
                        self.gui.updateConsole(tmp)
                else:
                    tmp = "== No File Selected ==\n"
                    self.gui.updateConsole(tmp)
            else:
                tmp = "== No confirm channel in slotmap! ==\n"
                self.gui.updateConsole(tmp)
                self.dataReadyStatus = -1
                self.packetList = []
                self.sendCount = 0
                self.txResendCount = 0
                self.packetListComplete = []
                self.networkDataTXAbortTimer.stop()
                self.networkDataRXAbortTimer.stop()

    def threadTxPacketBuild(self, fileData):
        self.threadRunningTx = 1
        if self.gui.radioMode == "networking":
            maxDataLength = self.gui.windowNetwork.destSlotDataMax
        else:
            maxDataLength = self.packetLength
        firstHeader = f"d1,{str(self.sendCount)},{self.fileType},{self.fileName},"  # 3 + 6(max) + 1 + 1 + 1 + 50 + 1 = 63, round to 80
        payloadSize = len(fileData)
        maxHeaderLen = 8  # "d999999," supports up to a million packets.
        maxFirstHeaderLen = 80
        dataSizeFirst = maxDataLength - maxFirstHeaderLen
        dataSize = maxDataLength - maxHeaderLen
        self.packetListComplete = list()
        if payloadSize < dataSizeFirst:  # all fits in one packet
            # print("Single Packet")
            firstHeader = f"d1,1,{self.fileType},{self.fileName},"  # 3 + 6(max) + 1 + 1 + 1 + 50 + 1 = 63, round to 80
            firstPacket = (firstHeader + fileData).encode()
            firstPacket = (b64encode(firstPacket)).decode('utf-8')
            self.packetListComplete.append(firstPacket)
        else:
            # print("Multiple Packets")
            firstData, mainData = fileData[:dataSizeFirst], fileData[dataSizeFirst:]
                # +2 below adds 0 count and fist packet
            self.packetListComplete = list((f"d{int(i/dataSize) + 2},{mainData[i:i+dataSize]}").encode() for i in range(0, payloadSize, dataSize))
            throwAway = self.packetListComplete.pop()  # last element is empty, so remove it
            for i in range(len(self.packetListComplete)):
                self.packetListComplete[i] = (b64encode(self.packetListComplete[i])).decode('utf-8')
            totalCount = len(self.packetListComplete) + 1 # +1 accounts for first packet
            firstHeader = f"d1,{totalCount},{self.fileType},{self.fileName},"
            firstPacket = (firstHeader + firstData).encode()
            firstPacket = (b64encode(firstPacket)).decode('utf-8')
            self.packetListComplete.insert(0,firstPacket)
        self.packetList = self.packetListComplete
        # print(f"TX Packet Length(first, rest): {len(self.packetListComplete[0])}, {len(self.packetListComplete[1])}")
        self.threadRunningTx = 0

    def txStartSend(self):
        if self.threadRunningTx == 0:
            self.txThreadCheckTimer.stop()
            self.stopBuild = time()
            self.dataReadyStatus = 2 #packets ready
            print(f"Packet buffer build time: {(self.stopBuild - self.startBuild):.3f} seconds")
            self.sendCount = 0
            self.txResendCount = 0
            print(f"Sending {str(len(self.packetList))} packets")
            self.sendStart = time()
            self.gui.windowDataTransfer.updateDropMenuDest()
            if self.gui.radioMode == 'networking':
                tmp = 0
                for i in range(len(self.gui.windowNetwork.slotMap)):
                    tmp = tmp + int(self.gui.windowNetwork.slotMap[i]["period"])
                self.slotMapTime = tmp * 2
                # print("time", self.slotMapTime)
                self.networkDataTXAbortTimer.setInterval(self.slotMapTime)
                self.networkFileSend()
            else:
                self.packetTimer.start()

    ####################
    # RX Packet to file
    ####################

    def threadRxPacketBuild(self):
        self.threadRunningRx = 1
        self.packetBuffer = "".join(self.rxMsgList)
        self.threadRunningRx = 0

    def rxFinish(self):
        if self.threadRunningRx == 0:
            self.stopBuild = time()
            print(f"File from packets build time: {(self.stopBuild - self.startBuild):.3f} seconds")
            self.rxThreadCheckTimer.stop()
            fullName = self.gui.appSettings['downloadDirectory'] + self.fileName
            if self.fileType == "Text":
                asciiBuffer = self.packetBuffer
                file = open(fullName, "w")
                file.write(asciiBuffer)
                file.close()
                print("Saving Text File:", self.fileName)
            if self.fileType == "Binary":
                self.packetBuffer = self.packetBuffer.encode()
                tmp = b64decode(self.packetBuffer)
                file = open(fullName, "wb")
                file.write(tmp)
                file.close()
                print("Saving Binary File:", self.fileName)
            tmp = f"\n{self.rxResendCount} packets resent out of {str(self.rxPacketTotal)}\n"
            success = "%0.2f" % (((self.rxPacketTotal - self.rxResendCount) / self.rxPacketTotal) * 100)
            tmp = tmp = tmp + "Data Packet Success = " + success + "%\n"
            tmp = tmp + "File Send Complete\n"
            text = tmp + "Transfer Complete\n"
            self.gui.updateConsole(text)
            self.packetBuffer = ""
            self.rxMsgArray = []
            self.lastMsgExpected = 0
            self.msgsReceived = 0

# >>> import base64
# >>> file = open('a.out', 'rb')
# >>> data = file.read()
# >>> file.close()
# >>> data2 = base64.b64encode(data)
# >>> file2 = open('hello', 'wb')
# >>> file2.write(base64.b64decode(data2))
# 15960
# >>> file2.close()


    def toBase64(self, data):
        data = str(data)
        data = data.encode("ascii")
        data = b64encode(data)
        data = data.decode("ascii")
        return data

    def fromBase64(self, data):
        data = data.encode("ascii")
        data = b64decode(data)
        data = data.decode("ascii")
        return data
