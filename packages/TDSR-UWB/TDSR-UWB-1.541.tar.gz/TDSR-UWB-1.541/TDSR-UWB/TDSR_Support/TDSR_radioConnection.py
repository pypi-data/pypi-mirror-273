import os
import socket
import struct
import queue
import threading
from json import loads
from time import sleep
import serial
import serial.tools.list_ports
import ipaddress
import netifaces

from TDSR_Support import TDSR_radioAPI

__version__ = "1.541"

# Use netifaces to find local IP addresses.
netifaces_available = False
try:
    import netifaces
    netifaces_available = True

except ImportError as e:
    netifaces_available = False

class Radio:
    def __init__(self, gui, messageTypes, interfaceType, interfaceAddr, interfacePort):
        # def __init__(self, gui, messageTypes, interface, interfaceAddr, interfacePort):
        self.TxQueue = queue.Queue()
        # print(interfaceAddr, self.TxQueue)
        self.gui = gui
        self.shutDownThreads = False
        self.RxThread = None
        self.TxThread = None
        self.radioIf = None
        self.messageTypes = messageTypes
        self.messageQueues = {}
        self.interfaceType = interfaceType
        self.interfaceAddr = interfaceAddr
        self.interfacePort = interfacePort
        self.status = ""
        if self.interfaceType == 'ip':
            self.status = self.connectIP()
        if self.interfaceType == 'usb' and self.interfacePort == 'connect':
            # print("Connecting")
            self.status = self.connectUSB()
        if self.interfaceType == 'None':
            self.status = False


    # Transmits any packets in the TXQueue for radio
    def TxQueueThread(self):
        #If thread is active
        while not self.shutDownThreads:
            # print("TXsize", self.TxQueue.qsize())
            # print(f"size {self.TxQueue.qsize()} for TxThread Queue {self.TxQueue}")
            packet = None
            try:
                packet = self.TxQueue.get(timeout = 0.1)    # if packet in the transmit queue then send it.
                if packet != None:
                    # print("  TXQueueThread Sending:", packet)
                    # if self.gui.appSettings['enableLogging'] == 1:
                    #     self.gui.logFile.logToFile(packet, self.gui.appSettings['reqIP'])
                    self.radioIf.sendPacket(packet)
            except:
                pass

    # Thread to handle messages that are in the input fifo from radio to host
    def RxQueueThread(self):
        while not self.shutDownThreads:
            packet = None
            try:
                packet = self.radioIf.inputFIFO.get(timeout = 0.5)
                if packet != None:
                    packet = packet.decode("utf-8")
                    packet = loads(packet)
                    # print("  RxQueueThread Saw:", packet)
                    msgType = list(packet.keys())[0]
                    msgId = packet[msgType]['msgId']
                    # if msgType == "DATA_INFO":
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    # if msgType == "RANGE_INFO":
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    # if "CONFIRM" in msgType:
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    #     print()
                    #If msgType exists in API message handler (PythonAPI.py), and msgType has a queue registered.
                    if msgType in self.API.messageList.keys():
                        if msgType in self.messageQueues.keys():
                            # print("In Keys")
                            # print("Pre length", self.messageQueues[msgType].qsize())
                            # print(packet)
                            self.messageQueues[msgType].put(packet)
                            # print("inner", self.messageQueues['RADIO_GET_INFO_CONFIRM'])
                            # print("Post length", self.messageQueues[msgType].qsize())
                            # print(f"Adding to {msgType} Queue")
                            # print("RX Pack:", packet)
                        else:
                            if "CONFIRM" in msgType:
                                # print(packet)
                                # print("Confirm")
                                # print(packet)
                                self.messageQueues['General_Confirm'].put(packet)
                                # print(time.time())
                                # print(f"RXThread: Adding {msgType} to General_Confirm Queue")
                            else:
                                if "REQUEST" not in msgType:
                                    # print("General")
                                    self.messageQueues['General_Msg'].put(packet)
                                    # print(f"RX Thread: Adding {msgType} to General Message Queue")
                                else:
                                    ...
                                    # print("Dumping Request")
                    else:
                        print("RX Thread: MessageType not in API keys")
                        print(f"   Type: {msgType}")
                        print(f"   Keys: {self.API.messageList.keys()}")
                        print(f"   Type: {packet}")
                    if self.gui.appSettings['enableLogging'] == 1 and (self.gui.radioMode != "idle" or self.gui.appSettings['logWhileIdle'] == 1):
                        self.gui.logFile.logToFile(packet, self.gui.appSettings['reqRadio'])
            except:
                pass

    def findUsbRadios(self):
        radios = []
        ports = [port for port in serial.tools.list_ports.comports() if port != "n/a" and port.vid == 0x1027 and port.pid == 0x1234]
        # print(ports)
        for radio in ports:
            radios.append(radio)
            # print(radio)
        return radios

    def getMulticast(self):
        timeout = 0.1
        local_ipv4_interfaces = []
        ifaces = netifaces.interfaces()
        for iface in ifaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs.keys():
                for local_addr_info in addrs[netifaces.AF_INET]:
                    # Confirm it has an "addr" key for the IP address (should always)
                    # Also use the "peer" to avoid certain loopback addresses on some OSes
                    if "addr" in local_addr_info.keys() and "peer" not in local_addr_info.keys():
                        local_addr = local_addr_info['addr']
                        # Attempt to avoid loopback addresses on multiple platforms
                        if local_addr[0:4] != "127.":
                            local_ipv4_interfaces.append(local_addr)        # Create and bind list of sockets
        sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for i in range(len(local_ipv4_interfaces))]
        [sockets[i].bind((local_ipv4_interfaces[i], 0)) for i in range(len(local_ipv4_interfaces))]
        # Basic RADIO_GET_INFO_REQUEST to send out
        req_str = '{"RADIO_GET_NODE_CONFIG_REQUEST":{"msgId":100}}'
        # Send to the multicast address and port 8890, on each provided IP interface.
        for s in sockets:
            try:
                s.sendto(req_str.encode(), ("239.255.92.43", 8890))
            except OSError:
                print("Error multicasting from %s" % str(s.getsockname()))
                # Most likely, a virtual interface was tried that the OS didn't have set up for multicast.
                # Since we can't use that interface anyway, just proceed as normal (we won't get any responses obviously, but it's also harmless in the socket list).
                pass
        # Now receive RADIO_GET_INFO_CONFIRMs and store in a dict.
        # Dict will be {key, value} of {IPv4 address string, RADIO_GET_INFO_CONFIRM object}
        found_radios = {}
        # Receive messages up to the timeout. Any that match expected parameters will add a radio to our list.
        sleep(timeout)
        # Check all interfaces and receive data.
        for s in sockets:
            # Read packets in a loop until there are none left
            while True:
                rx_data = None
                rx_source = None
                try:
                    # Receive a message (if any)
                    s.setblocking(False)
                    rx = s.recvfrom(1600)
                    if rx is None:
                        # No data to receive
                        break
                    rx_data, rx_source = rx
                except (TimeoutError, BlockingIOError):
                    # No data to receive
                    break
                if rx_data is None or rx_source is None:
                    break
                # Try converting it to a RADIO_GET_INFO_CONFIRM
                try:
                    rx_obj = loads(rx_data)
                    if len(rx_obj.keys()) != 1:
                        # Not a valid API message
                        continue
                    if "RADIO_GET_NODE_CONFIG_CONFIRM" not in rx_obj.keys():
                        # May or may not be an API message, but it's not the API message type we're looking for
                        continue
                    if rx_obj["RADIO_GET_NODE_CONFIG_CONFIRM"]["msgId"] != 100:
                        # Wrong msgId. Really not likely to happen at this point, but msgId should have matched, so reject it.
                        continue
                    # Add it to the list!
                    found_radios[rx_source[0]] = rx_obj
                except ValueError:
                    continue
        return found_radios

    def connectIP(self):
        if self.radioIf != None:
            print("Radio is already connected")
        self.radioIf = radioIfIp(self.interfaceAddr, self.interfacePort)             #  Radio Interface Socket
        status = self.radioIf.connect()   # opens socket and starts read thread for radio to host input FIFO.
        if status == True:
            if self.interfacePort == 8888:
                print("Connected to radio IP address:", self.interfaceAddr)
            self.API = TDSR_radioAPI.RadioAPI(self.messageQueues, self.messageTypes, self.TxQueue)
            self.connectCommon()
        return status

    def connectUSB(self):
        if self.radioIf != None:
            print("Radio is already connected")
        self.radioIf = radioIfUsb(self.interfaceAddr)
        status = self.radioIf.connect()
        if status == True:
            print("Connected to radio USB Port:", self.interfaceAddr)
            self.API = TDSR_radioAPI.RadioAPI(self.messageQueues, self.messageTypes, self.TxQueue)
            self.connectCommon()
        return status

    # Finishes connection after interface-specific _radioIfObj has been created and connected
    def connectCommon(self):
        # Clear TX queue
        self.TxQueue.queue.clear()
        if self.interfacePort == 8888:
            print(f'Configuring message queues for radio {self.interfaceAddr}')
        self.getStatsConfirm_Queue = queue.Queue()
        self.getInfoConfirm_Queue = queue.Queue()
        self.dataSendConfirm_Queue = queue.Queue()
        self.sendRangeConfirm_Queue = queue.Queue()
        self.getNetworkStatsConfirm_Queue = queue.Queue()
        self.dataInfo_Queue = queue.Queue()
        self.rangeInfo_Queue = queue.Queue()
        self.generalConfirm_Queue = queue.Queue()
        self.generalMsg_Queue = queue.Queue()
        self.messageQueues['RADIO_GET_STATS_CONFIRM'] = self.getStatsConfirm_Queue
        self.messageQueues['RADIO_GET_INFO_CONFIRM'] = self.getInfoConfirm_Queue
        self.messageQueues['RANGE_SEND_RANGE_CONFIRM'] = self.sendRangeConfirm_Queue
        self.messageQueues['DATA_CONFIRM']= self.dataSendConfirm_Queue
        self.messageQueues['NETWORKING_GET_STATS_CONFIRM'] = self.getNetworkStatsConfirm_Queue
        self.messageQueues['DATA_INFO'] = self.dataInfo_Queue
        self.messageQueues['RANGE_INFO'] = self.rangeInfo_Queue
        self.messageQueues['General_Confirm'] = self.generalConfirm_Queue
        self.messageQueues['General_Msg'] = self.generalMsg_Queue
        # Start threads
        self.shutDownThreads = False
        self.TxThread = threading.Thread(target = self.TxQueueThread, name = "TX Thread for %s" % self.interfaceAddr)
        self.RxThread = threading.Thread(target = self.RxQueueThread, name = "RX Thread for %s" % self.interfaceAddr)
        self.TxThread.start()
        self.RxThread.start()

    # Shut down threads and disconnect radio
    def disconnect(self):
        if self.radioIf == None:
            print("Radio is not connected")
            return
        else:
            if self.interfacePort == 8888:
                print(f"Disconnecting Handler for ip {self.interfaceAddr}")
            self.shutDownThreads = True
            self.RxThread.join()
            self.TxThread.join()
            self.RxThread = None
            self.TxThread = None
            self.radioIf.disconnect()
            self.radioIf = None

class RadioError(Exception):
    pass

class radioInterface():
    def __init__(self):
        self.discardInfoMsgs = False
        self.readThread = None
        self.inputFIFO = queue.Queue(maxsize = 100)
        self.shutDown = False

    def __del__(self):
        self.shutDown = True

    def sendPacket(self, payload):
        pass

    def flushInput(self):
        with self.inputFIFO.mutex:
            self.inputFIFO.queue.clear()

    def readThreadFunc(self):  # timeout for thread set lower in this module
        while not self.shutDown:
            # Read packets and add to the FIFO.
            packet = self.readPacketInternal()
            if packet != None and packet != False:
                # print(packet)
                if len(packet) >= 4:
                    if self.discardInfoMsgs:
                        if packet[0] & 0x03 == 0x02:
                            continue
                    try:
                        if self.inputFIFO.full():
                            # Discard oldest message
                            self.inputFIFO.get_nowait()
                    except:
                        pass
                    try:
                        self.inputFIFO.put(packet, block=False)
                        # print(f"   Stuffing incoming packet for {self.interfacePort} into input FIFO")
                    except:
                        pass

    def readPacketInternal(self):
        pass

    def readPacket(self, msgType=0, timeout=1.0):
        pass

    def setTimeout(self, timeout):
        pass


class radioIfIp(radioInterface):
    def __init__(self, ip, interfacePort):
        super().__init__()
        self.sock = None
        self.ip = ip
        self.interfacePort = interfacePort
        # self.sendBuffer = []
        # self.packetBuffer = []

    def connect(self):
        self.disconnect()
        self.shutDown = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.settimeout(0.1)
        payload = '{"RADIO_GET_CONFIG_REQUEST": {"msgId": 1, "configId": 0}}'
        self.sendPacket(payload)
        try:
            packet, addr = self.sock.recvfrom(1500)
                # reaad Thread it to fill input FIFO with incoming traffic
            self.readThread = threading.Thread(target=self.readThreadFunc, name="Radio %s Read Thread" % self.ip)
            self.readThread.start()
            return True
        except socket.timeout:
            return False

    def disconnect(self):
        self.shutDown = True
        if self.readThread != None:
            self.readThread.join()
            self.readThread = None
        if self.sock != None:
            self.sock.close()
            self.sock = None

    def sendPacket(self, payload):
        payload = payload.encode()
        # print(f'radioConnection: sendPacket sending to {self.ip} \n  Payload: {payload}')
        self.sock.sendto(payload, (self.ip, self.interfacePort))

    def readPacketInternal(self):
        try:
            packet, addr = self.sock.recvfrom(1500)
            # print(f"RadioIF readPacketInternal from: {addr} received: {packet}")
        except socket.timeout:
            # print("readPacketInternal: IP Timeout")
            return None
        return packet

    def setTimeout(self, timeout):
        old = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        return old

class radioIfUsb(radioInterface):
    def __init__(self, interfaceAddr):
        super().__init__()
        self.interfaceAddr = interfaceAddr
        self.USBRadio = None

    def connect(self):
        # print ("Using USB Port:", self.interfaceAddr)
        self.USBRadio = serial.Serial(self.interfaceAddr, baudrate=4000000,timeout=.05)
        payload = '{"RADIO_GET_CONFIG_REQUEST": {"msgId": 1, "configId": 0}}'
        self.sendPacket(payload)
        sleep(.25)
        try:
            packet = self.readPacketInternal()
            packet = self.readPacketInternal()
            if packet == None:
                print("Could not open USB port:", self.interfaceAddr)
                return False
            else:
                self.readThread = threading.Thread(target=self.readThreadFunc, name="Radio %s Read Thread" % self.interfaceAddr)
                self.readThread.start()
                return True
        except:
            print("Could not open USB port:", self.interfaceAddr)
            return False

    def disconnect(self):
        self.shutDown = True
        if self.readThread != None:
            self.readThread.join()
            self.readThread = None
        if self.USBRadio != None:
            self.USBRadio.close()
            self.USBRadio = None

    def sendPacket(self, payload):
        payload = payload + "\n"
        # print()
        # print("payload Msg:", payload)
        packet = payload.encode()
        # print("radioIfUsb: Sending packet:", packet)
        self.USBRadio.write(packet)

    def readPacketInternal(self):
        # print("radioIfUsb: readPacketInternal")
        try:
            if self.USBRadio.inWaiting() > 0:
                packet = self.USBRadio.readline(self.USBRadio.inWaiting())
                # print("radioIfUsb: Receiving packet:", packet)
                # msg = packet.decode("utf-8")
                # msgJson = loads(msg)
                # print(msgJson)
                return packet
            else:
                return None
        except:
            # print("Error communicating with radio on USB")
            return False

    def threadRead(self, exitEvent, readQueue):
        while not exitEvent.isSet():
            packet =  self.readPacketNoError()
            if (len(packet) > 0):
                readQueue.put(packet)
