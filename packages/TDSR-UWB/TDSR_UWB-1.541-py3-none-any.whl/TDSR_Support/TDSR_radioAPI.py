from json import dumps
from time import sleep

__version__ = "1.541"

class RadioAPI:
    _msgId = 0

    def __init__(self, messageQueues, messageList, TxQueue):
        self.TxQueue = TxQueue
        self.messageList = messageList
        self.messageQueues = messageQueues

# Data commands. Does not request a confirm. When data comes in it uses a DATA_INFO message, which is decoded
#   in the readPacketRequesConfirm and readPacketAPI commands
    def dataSend_UInt8_Request(self,ip, responderId, data):
        message = self.getMessageFromList('DATA_REQUEST')
        message[list(message.keys())[0]]['destinationId'] = responderId
        message[list(message.keys())[0]]['data'] = data
        message[list(message.keys())[0]]['encoding'] = "ENCODING_UINT8"
        self.sendMessage(message,ip)

    def dataSend_B64_Request(self,destIP, destID, slot, order, data):
        # print("Send")
        message = self.getMessageFromList('DATA_REQUEST')
        if order == "front":
            message[list(message.keys())[0]]['packetType'] = "PACKET_TYPE_FRONT"
        else:
            message[list(message.keys())[0]]['packetType'] = "PACKET_TYPE_QUEUE"
        message[list(message.keys())[0]]['destinationId'] = destID
        message[list(message.keys())[0]]['slot'] = slot
        message[list(message.keys())[0]]['data'] = data
        message[list(message.keys())[0]]['encoding'] = "ENCODING_BASE64"
        # print(message)
        status, packet, addr = self.readPacketRequestConfirm(message,'DATA_CONFIRM',destIP,retryCount = 2)
        return status

    def dataSend_UInt32_Request(self,ip, responderId, data):
        message = self.getMessageFromList('DATA_REQUEST')
        message[list(message.keys())[0]]['destinationId'] = responderId
        message[list(message.keys())[0]]['data'] = data
        message[list(message.keys())[0]]['encoding'] = "ENCODING_UINT32"
        self.sendMessage(message,ip)

    def dataSend_String_Request(self,ip, responderId, data):
        message = self.getMessageFromList('DATA_REQUEST')
        message[list(message.keys())[0]]['destinationId'] = responderId
        message[list(message.keys())[0]]['data'] = data
        message[list(message.keys())[0]]['encoding'] = "ENCODING_STRING"
        self.sendMessage(message,ip)

# Networking section
    def network_GetSlotMap_Request(self,ip):
        message = self.getMessageFromList('NETWORKING_GET_SLOT_MAP_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'NETWORKING_GET_SLOT_MAP_CONFIRM',ip,retryCount  = 1 )
        return status,packet,addr

    def network_Stats_Request(self,ip):
        message = self.getMessageFromList('NETWORKING_GET_STATS_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'NETWORKING_GET_STATS_CONFIRM',ip,retryCount  = 1 )
        return status,packet,addr

    def network_SetSlotMap_Request(self, ip, slotMap, persist):
        message = self.getMessageFromList('NETWORKING_SET_SLOT_MAP_REQUEST')
        message[list(message.keys())[0]]['slotMap'] = slotMap
        message[list(message.keys())[0]]['persistFlag'] = persist
        status, packet, addr = self.readPacketRequestConfirm(message,'NETWORKING_SET_SLOT_MAP_CONFIRM',ip,retryCount  = 1 )
        return status,packet,addr

# Radio Command section
    def radio_GetConfig_Request(self,ip, configId):
        message = self.getMessageFromList('RADIO_GET_CONFIG_REQUEST')
        message[list(message.keys())[0]]['configId'] = configId
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_CONFIG_CONFIRM',ip )
        return packet,addr

    def radio_SetConfig_Request(self, ip, message, persist):
        message['RADIO_SET_CONFIG_REQUEST'] = message.pop(list(message.keys())[0])
        message[list(message.keys())[0]]['persistFlag'] = persist
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_CONFIG_CONFIRM',ip )
        return packet,addr

    def radio_GetConnect_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_CONNECT_REQUEST')
        message[list(message.keys())[0]]['connectType'] = 0
        status,packet,addr = self.readPacketRequestConfirm(message,'RADIO_GET_CONNECT_CONFIRM',ip,retryCount  = 1 )

        return status,packet,addr

    def radio_SetConnect_Request(self,ip):
        message = self.getMessageFromList('RADIO_SET_CONNECT_REQUEST')
        message[list(message.keys())[0]]['connectType'] = 0
        try:
            status,packet,addr = self.readPacketRequestConfirm(message,'RADIO_SET_CONNECT_CONFIRM',ip,retryCount  = 1 )
        except:
            status = False
            packet = None
            addr = ip
            print("-- Could not reach network --")
        return status,packet,addr

    def radio_GetInfo_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_INFO_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_INFO_CONFIRM',ip )
        return status,packet,addr

    def radio_GetTuning_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_TUNING_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_TUNING_CONFIRM',ip )
        return status,packet,addr

    def radio_SetTuning_Request(self,ip, message):
        message['RADIO_SET_TUNING_REQUEST'] = message.pop(list(message.keys())[0])
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_TUNING_CONFIRM',ip )
        return packet,addr

    def radio_GetNodeID_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_NODE_CONFIG_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_NODE_CONFIG_CONFIRM',ip )
        return packet,addr

    def radio_SetNodeID_Request(self,ip, nodeID, persist):
        message = self.getMessageFromList('RADIO_SET_NODE_CONFIG_REQUEST')
        message[list(message.keys())[0]]['nodeId'] = nodeID
        message[list(message.keys())[0]]['persistFlag'] = persist
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_NODE_CONFIG_CONFIRM',ip )
        return packet,addr

    def radio_GetState_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_STATE_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_STATE_CONFIRM',ip )
        return packet,addr

    def radio_SetState_Request(self,ip, message):
        message['RADIO_SET_STATE_REQUEST'] = message.pop(list(message.keys())[0])
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_STATE_CONFIRM',ip )
        return packet,addr

    def radio_GetStats_Request(self,ip):
        message = self.getMessageFromList('RADIO_GET_STATS_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_STATS_CONFIRM',ip )
        return status,packet,addr

    def radio_ClearStats_Request(self,ip):
        message = self.getMessageFromList('RADIO_SET_STATS_CLEAR_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_STATS_CLEAR_CONFIRM',ip )
        return status,packet,addr

    def radio_Reboot_Request(self,ip):
        message = self.getMessageFromList('RADIO_REBOOT_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_REBOOT_CONFIRM',ip )
        return status,packet,addr

    def radio_FactoryReset_Request(self,ip):
        message = self.getMessageFromList('RADIO_RESET_FACTORY_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_RESET_FACTORY_CONFIRM',ip )
        return status,packet,addr

    def radio_GetIP_Request(self, ip):
        message = self.getMessageFromList('RADIO_GET_IP_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_IP_CONFIRM',ip )
        return status,packet,addr

    def radio_SetIP_Request(self, ip, ipNew, netmask, gateway):
        message = self.getMessageFromList('RADIO_SET_IP_REQUEST')
        message[list(message.keys())[0]]['ipv4'] = ipNew
        message[list(message.keys())[0]]['netmask'] = netmask
        message[list(message.keys())[0]]['gateway'] = gateway
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SET_IP_CONFIRM',ip )
        return packet,addr

    def radio_ApplyPreset_Request(self, ip, presetName, persist):
        message = self.getMessageFromList('RADIO_APPLY_PRESET_REQUEST')
        message[list(message.keys())[0]]['presetName'] = presetName
        message[list(message.keys())[0]]['persistFlag'] = persist
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_APPLY_PRESET_CONFIRM',ip )
        return packet,addr

    def radio_ListPresets_Request(self, ip):
        message = self.getMessageFromList('RADIO_LIST_PRESETS_REQUEST')
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_APPLY_PRESET_CONFIRM',ip )
        return packet,addr

    def radio_SavePreset_Request(self, ip, presetName, lock):
        message = self.getMessageFromList('RADIO_SAVE_PRESET_REQUEST')
        message[list(message.keys())[0]]['presetName'] = presetName
        message[list(message.keys())[0]]['lock'] = lock
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_SAVE_PRESET_CONFIRM',ip )
        return packet,addr

    def radio_DeletePreset_Request(self, ip, presetName):
        message = self.getMessageFromList('RADIO_DELETE_PRESET_REQUEST')
        message[list(message.keys())[0]]['presetName'] = presetName
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_DELETE_PRESET_CONFIRM',ip )
        return packet,addr

    # This gets the current config and tuning data from a given preset without actually updating the radio to that preset.
    def radio_GetPreset_Request(self, ip, presetName):
        message = self.getMessageFromList('RADIO_GET_PRESET_REQUEST')
        message[list(message.keys())[0]]['presetName'] = presetName
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_PRESET_CONFIRM',ip )
        return packet,addr

    # This finds out if there is an active preset on the radio, and if so, which one.
    def radio_Get_Active_Preset_Request(self, ip):
        message = self.getMessageFromList('RADIO_GET_ACTIVE_PRESET_REQUEST')
        # print(message)
        status, packet, addr = self.readPacketRequestConfirm(message,'RADIO_GET_ACTIVE_PRESET_CONFIRM',ip )
        return packet,addr

# Ranging Command section
    def range_Send_Request(self,ip, responderId, rangeMethod, encoding, data):
        message = self.getMessageFromList('RANGE_SEND_RANGE_REQUEST')
        message[list(message.keys())[0]]['responderId'] = responderId
        message[list(message.keys())[0]]['encoding'] = "ENCODING_BASE64"
        message[list(message.keys())[0]]['data'] = data
        message[list(message.keys())[0]]['rangeMethod'] = rangeMethod
        status, packet, addr = self.readPacketRequestConfirm(message,'RANGE_SEND_RANGE_CONFIRM',ip,retryCount  = 1 )
        return status,packet,addr

    def getMessageFromList(self,messageName):
        messages = [value for key, value in self.messageList.items() if messageName.upper() in key.upper()]
        #for key, value in self.messageList.items():
            #print(key.upper())
        # print(messages)
        if (messages):
            return messages[0]
        else:
            return None

    # this is used to send get request and let the response get handles with info message
    def sendMessage(self, txMessageObj, ip ):
        txMessageObj[list(txMessageObj.keys())[0]]['msgId'] = self._msgId&0xffff
        self._msgId += 1
        payload = dumps(txMessageObj)
        # print(f"API: Send message adding to TXQueue for IP {ip}")
        # print(txMessageObj)
        # print(f"size {self.TxQueue.qsize()} for SendMessage Queue {self.TxQueue}")
        self.TxQueue.put(payload)
        # print(f"size {self.TxQueue.qsize()} for SendMessage Queue {self.TxQueue}")
        # self.radioIf.sendPacket(payload.encode('utf-8'),ip)

    def readPacketRequestConfirm(self, txMessageObj, rxMessageName,txIp, retryCount  = 0):
        fields = None
        addr = None
        packet = None
        status = True
        self.sendMessage(txMessageObj,txIp)
            # if there is a dedicated queue then draw from it.
        if rxMessageName in self.messageQueues.keys():
            # print(f"Found: {rxMessageName}")
            try:
                packet = self.messageQueues[rxMessageName].get(timeout = 0.1)
                # print("Got: ", rxMessageName)
                # print(f'{packet}\n')
            except:
                print("failed queue")
                print(f"Missed a {rxMessageName} packet")
                status = False
                pass
        else:
            # otherwise, if it's a comfirm message, draw from the general confirm.
            if "CONFIRM" in rxMessageName:
                # print(f"General Confirm: {rxMessageName}")
                try:
                    # print(time.time())
                    packet = self.messageQueues['General_Confirm'].get(timeout = 0.4)
                    # print(f'{packet}\n')
                except:
                    print(f"Missed a {rxMessageName} message")
                    # print("I'm here")
                    print(packet)
                    # print(time.time())
                    status = False
                    pass
            else:
                # should never really land here since message wasn't a confirm request.
                print(f"Looking For: {rxMessageName}")
                while not self.messageQueues['General_Msg'].empty():
                    try:
                        tmp = self.messageQueues['General_Msg'].get(timeout = 0.05)
                        print(tmp)
                    except:
                        status = False
                        pass
        return status,packet,[]

    #
    def sendStatusRequest(self,ip):
        pass
    #
    def sendRangeDataRequest(self,ip):
        pass
