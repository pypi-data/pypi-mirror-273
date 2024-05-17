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
<$#insert_here="RANGE_SEND_RANGE_REQUEST.txt"
```
### RANGE_CONFIRM
The range request message will contain the node ID of the responding radio.  
```
<$#insert_here="RANGE_SEND_RANGE_CONFIRM.txt"
```

<div style="page-break-after: always;"></div>

##  RANGE_SET_CONFIG_REQUEST and RANGE_SET_CONFIG_CONFIRM
These messages allow a host to set the Decawave hardware parameters of the radio. 

```
DWT_PLEN_64
DWT_PLEN_128
DWT_PLEN_256
DWT_PLEN_512
DWT_PLEN_1024
DWT_PLEN_1536
DWT_PLEN_2048
DWT_PLEN_4096
```


```
DWT_PRF_16M
DWT_PRF_64M
```
```
DWT_BR_110K
DWT_BR_850K
DWT_BR_6M8
```


```
DWT_PAC8
DWT_PAC16
DWT_PAC32
DWT_PAC64
```





### RANGE_SET_CONFIG_REQUEST
This message contains a "persistFlag"
```
<$#insert_here="RANGE_SET_CONFIG_REQUEST.txt" 
```



### RANGE_SET_CONFIG_CONFIRM
The radio can reject hardware parameters or adjust hardware parameters
```
<$#insert_here="RANGE_SET_CONFIG_CONFIRM.txt" 
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
<$#insert_here="RANGE_SET_STATE_REQUEST.txt" 
```


###  RANGE_SET_STATE_CONFIRM
This message reports the that request message has reached the radio and this messages confirms that. 

```
<$#insert_here="RANGE_SET_STATE_CONFIRM.txt" 
```

<div style="page-break-after: always;"></div>

## RANGE_INFO

This message remorts the results of a range transaction. Either range transaction was successful and the range is reported in this message.
```
<$#insert_here="RANGE_INFO.txt" 
```


<div style="page-break-after: always;"></div>

## RANGE_DEBUG_INFO

```
<$#insert_here="RANGE_DEBUG_INFO.txt" 
```



<div style="page-break-after: always;"></div>

## Radio Section

### RADIO_GET_INFO_REQUEST

```
<$#insert_here="RADIO_GET_INFO_REQUEST.txt"
```

### RADIO_GET_INFO_CONFIRM
This messages reports 


```
<$#insert_here="RADIO_GET_INFO_CONFIRM.txt" a
```



<div style="page-break-after: always;"></div>

### RADIO_GET_STATS_REQUEST


```
<$#insert_here="RADIO_GET_STATS_REQUEST.txt" 
```



### RADIO_GET_STATS_CONFIRM

```
<$#insert_here="RADIO_GET_STATS_CONFIRM.txt"
```




### RADIO_MESSAGE_ERROR

This message is returned by the radio when the it can not parse a received messages. 
```
<$#insert_here="RADIO_MESSAGE_ERROR.txt"
```


<div style="page-break-after: always;"></div>
