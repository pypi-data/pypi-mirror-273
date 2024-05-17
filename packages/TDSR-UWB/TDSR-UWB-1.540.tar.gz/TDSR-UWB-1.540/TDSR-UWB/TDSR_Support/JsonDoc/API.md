<p align="center"><img src = "Doc/TDSR_logo_250x134.png"
</p><br>


# TDSR Development  <br>PennyWhistle API<br />
<p>
<script> document.write(new Date().toLocaleDateString()); </script>
</p>


The API is json messages sent via UDP packets. The radio will open a UDP port (8888) and listen for messages. 
The radio will decode any messages received on that port and process the message accordingly. 

The API will have different sections. In the initial version of the API there will be two sections "Radio" and "Range".
The "Radio" section contains messages for general radio operation, these messages would apply to any node of operation. 
The "Range" section contains messages for ranging operations. 
Many of the messages are in pairs and operate as command and response, here called "Request" and "Confirm"


The radio can generate messages that are not matched with a request, these messages are "Info" messages and usually the results of the radio receiving messages from other radios. 


Each message will contain an MsgID field, MsgID from a request messages is copied to the matching confirm messages. Also, for ranging operation the MsgIS from the range request message added to the over the air ranging messages and responding radios will use the that MsgID in any Info messages generate as part of that that ranging transaction. 

One more note, the document shows the messages printed with pretty print (multi-line) form, the radio will normally report messages in single line mode (pretty print off).

<div style="page-break-after: always;"></div>

## Range Section

###  RANGE_REQUEST and RANGE_CONFIRM,  
A host sends a RANGE_REQUEST to the radio and it replies with a RANGE_CONFIRM. The RANGE_CONFIRM acknowledges the RANGE_REQUEST is received by the radio and not results of range transaction. After the range transaction the radio will send out info messages to report the results of the RANGE_REQUEST.
The range request message will contain the node ID of the responding radio. 

### RANGE_REQUEST
```
{
    "RANGE_SEND_RANGE_REQUEST": {
        "msgId": 0,
        "responderId": 0
    }
}
```
### RANGE_CONFIRM
The range request message will contain the node ID of the responding radio.  
```
{
    "RANGE_SEND_RANGE_CONFIRM": {
        "msgId": 0,
        "status": "ok"
    }
}
```

<div style="page-break-after: always;"></div>

##  RANGE_SET_CONFIG_REQUEST and RANGE_SET_CONFIG_CONFIRM
These messages allow a host to set the Decawave hardware parameters of the radio. 



### RANGE_SET_CONFIG_REQUEST
This message contains a "persistFlag"
```
{
    "RANGE_SET_CONFIG_REQUEST": {
        "msgId": 21,
        "nodeId": 100,
        "configId": 0,
        "channel": 2,
        "prf": "DWT_PRF_64M",
        "txPreambleLength": "DWT_PLEN_1024",
        "txRxPreambleCode": 9,
        "power": 0,
        "dataRate": "",
        "configFlags": "RangeConfigIPAsNodeId",
        "antennaDelay": 0,
        "persistFlag": 0
    }
}
```



### RANGE_SET_CONFIG_CONFIRM
The radio can reject hardware parameters or adjust hardware parameters
```
{
    "RANGE_SET_CONFIG_CONFIRM": {
        "msgId": 0,
        "status": "ok"
    }
}
```



<div style="page-break-after: always;"></div>

##  RANGE_SET_STATE_REQUEST and RANGE_SET_STATE_CONFIRM
These messages controls the state of the radio. Currenly, the allowable states are "Idle" or "Active". In the "Idle" the radio will not receive messages from othe radios or start a ranging transaction. At start up, the state of the radio is "Idle". In the future other states will be added for example "TDMA networking" or "Data only" (set and receive data messages). The request contains a config ID that matches the config ID in the set config messages (currently this feature is not fully implemented and only one config is supported). 
The radio will supports storing different hardware or radio configurations and allowing the host to select a configuration in the range request message. 


###  RANGE_SET_STATE_REQUEST
This message allows the host to select the hardware config the radio will use. The State request selects the config id for the radio. Currently, only config id 0 is supported.
The flags field controls extra debug info messages:
"RANGE_STATE_FLAGS_REPORT_DEBUG_INFO" generates RANGE_DEBUG_INFO messages for successful range transactions."RANGE_STATE_FLAGS_REPORT_SNIFF_INFO" generates RANGE_DEBUG_INFO messages for range transactions between other radios. 
```
{
    "RANGE_SET_STATE_REQUEST": {
        "msgId": 0,
        "state": "RangeStateActive",
        "configId": 0,
        "flags": "RANGE_STATE_FLAGS_REPORT_DEBUG_INFO+RANGE_STATE_FLAGS_REPORT_SNIFF_INFO",
        "persistFlag": 0
    }
}
```


###  RANGE_SET_STATE_CONFIRM
This message reports the that request message has reached the radio and this messages confirms that. 

```
{
    "RANGE_SET_STATE_CONFIRM": {
        "msgId": 0,
        "status": "ok"
    }
}
```

<div style="page-break-after: always;"></div>

## RANGE_INFO

This message remorts the results of a range transaction. Either range transaction was successful and the range is reported in this message.
```
{
    "RANGE_INFO": {
        "msgId": 0,
        "configId": 0,
        "requesterId": 0,
        "responderId": 0,
        "rangeStatus": 0,
        "stopwatchTime": 0,
        "precisionRangeMm": 0,
        "precisionRangeErrEst": 0,
        "responderFpp": 0,
        "firstPathPower": 0.0,
        "rxPower": 0.0,
        "maxNoise": 0,
        "stdNoise": 0,
        "firstPathAmp1": 0,
        "firstPathAmp2": 0,
        "firstPathAmp3": 0,
        "maxGrowthCIR": 0,
        "rxPreamCount": 0,
        "firstPath": 0,
        "timestamp": "0"
    }
}
```


<div style="page-break-after: always;"></div>

## RANGE_DEBUG_INFO

```
{
    "RANGE_DEBUG_INFO": {
        "msgId": 0,
        "configId": 0,
        "requesterId": 0,
        "responderId": 0,
        "rangeDebugType": "",
        "rcmUWBRangeReqOut": {
            "pktType": 0,
            "msgId": 0,
            "srcNodeId": 0,
            "destNodeId": 0,
            "rxTimestamp": 0,
            "status": 0,
            "phyHdrOut": []
        },
        "rcmUWBRangeReq2Out": {
            "pktType": 0,
            "msgId": 0,
            "srcNodeId": 0,
            "destNodeId": 0,
            "rxTimestamp": 0,
            "status": 0,
            "phyHdrOut": []
        },
        "rcmUWBRangeReq3Out": {
            "pktType": 0,
            "msgId": 0,
            "srcNodeId": 0,
            "destNodeId": 0,
            "rxTimestamp": 0,
            "status": 0,
            "phyHdrOut": []
        },
        "rcmUWBRangeRespOut": {
            "pktType": 0,
            "antennaMode": 0,
            "msgId": 0,
            "srcNodeId": 0,
            "destNodeId": 0,
            "LEDFlags": 0,
            "tagPollTxTimeOut": 0,
            "anchorRespRxTimeOut": 0,
            "tagFinalTxTimeOut": 0,
            "rxTimestamp": 0,
            "status": 0,
            "phyHdrOut": []
        }
    }
}
```



<div style="page-break-after: always;"></div>

## Radio Section

### RADIO_GET_INFO_REQUEST

```
{
    "RADIO_GET_INFO_REQUEST": {
        "msgId": 0
    }
}
```

### RADIO_GET_INFO_CONFIRM
This messages reports 


```
{
    "RADIO_GET_INFO_CONFIRM": {
        "msgId": 0,
        "serialNo": 0,
        "barCodeString": "",
        "boardType": "",
        "kernelVersion": "",
        "appVersion": "",
        "chipInfo": "PART: 1000173A LOT: 10205EFA"
    }
}
```



<div style="page-break-after: always;"></div>

### RADIO_GET_STATS_REQUEST


```
{
    "RADIO_GET_STATS_REQUEST": {
        "msgId": 0
    }
}
```



### RADIO_GET_STATS_CONFIRM

```
{
    "RADIO_GET_STATS_CONFIRM": {
        "msgId": 0,
        "numPacketsTransmitted": "0",
        "numPacketsReceived": "0",
        "numRangeRequests": "0",
        "numRangeRequestsComplete": "0",
        "numRangeResponses": "0",
        "PHE": 0,
        "RSL": 0,
        "CRCG": 0,
        "CRCB": 0,
        "ARFE": 0,
        "OVER": 0,
        "SFDTO": 0,
        "PTO": 0,
        "RTO": 0,
        "TXF": 0,
        "HPW": 0,
        "TXW": 0,
        "txErrors": "0",
        "receiverIdleError": "0"
    }
}
```


<div style="page-break-after: always;"></div>

## CAT mode
CAT mode send data packets between radios. The packets contain a BER pattern and CAT mode can be used to test link quality. 

### CAT_SET_CONFIG_REQUEST


```
{
    "CAT_SET_CONFIG_REQUEST": {
        "msgId": 0,
        "nodeId": 33752069,
        "opMode": "idle",
        "channel": 2,
        "prf": "DWT_PRF_64M",
        "txPreambleLength": "DWT_PLEN_1024",
        "txRxPreambleCode": 9,
        "power": 10,
        "configFlags": 0,
        "dataRate": "DWT_BR_110K",
        "dataType": "BER",
        "txNumPackets": 100,
        "txPacketLenWords": 100,
        "txPacketDelayMs": 100,
        "rxFilter": 0,
        "persistFlag": 0
    }
}
```

### CAT_SET_CONFIG_CONFIRM

{
    "CAT_SET_CONFIG_CONFIRM": {
        "msgId": 0,
        "status": "ok"
    }
}
'''

### CAT_GET_STATS_CONFIRM
```
{
    "CAT_GET_STATS_CONFIRM": {
        "msgId": 0,
        "opMode": 0,
        "tempDegC": 0,
        "numBitErrors": "0",
        "numBits": "0",
        "numPackets": "0",
        "numDroppedPackets": "0",
        "numErrorPackets": "0",
        "runTimeSecs": "0"
    }
}
```


### CAT_SET_STATE_REQUEST
```
{
    "CAT_SET_STATE_REQUEST": {
        "msgId": 0,
        "stopStart": ""
    }
}
```