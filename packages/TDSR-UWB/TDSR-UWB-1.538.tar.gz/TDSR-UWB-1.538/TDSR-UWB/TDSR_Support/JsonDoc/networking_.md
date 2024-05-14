#  Networking in PW
  
  
Simple networking is supported:
1. TDMA only, no aloha 
2. First slot setting timing for the network, no auto-selection of node setting timing, no changing masters if master is not available
3. Nodes can be in one of two states, acquire Timing (waiting to receive a messages from a node that has timing) or Have_timing. The master is assumed to have_timing as soon as it starts. 
4. Three types of slots: Idle, Data, Ranging
5. Multiple radios can "own" different slots, which means multiple radios operating in different slots can initiate range transaction. 
6. Slot period is set in milliseconds and is limited to a maximum of 100 ms. This limit is mostly a testing limit, this limit is what we will test to. Otherwise, what slot period do we check, 20 seconds. A user can add idle slots to make for a long cycle time if they need to. 
7. Use DW send delay to set the timing of the transmit packet to implement networking, use the DW system clock as source of timing.
8. Two types of user data, one type is sent in as a data message in a data slot and the other is sent in range request messages. No support for responders to reply with user data. 
9. Still deciding if Range_info needs to change,  either add fields for networking timing or define a new message "network_range_info" with contains fields for network timing (slot index and time offset).
10. Currently not planning to support user data in range response messages. Assume radios will be given requestor slots at some point or a data slot. Can revisit this later if we need to. At this stage just trying to keep the feature list a small as possible. 
11. The radio software will validate the slot map when a "SET_STATE_REQUEST (NETWORKING)" is received. And if any slot is too small, the radio software will reject the "SET_STATE_REQUEST". One thing that is also validated is making sure all config ids are valid, that a slot does not contain a config_id that has not been setup on the radio. 
  
<div style="page-break-after: always;"></div>
  
##  Range Slot Timing
  
In a range slot, there is buffer period at the beginning to allow radios to change config if needed. In some deployments, some radios may need to change config, the buffer period allow all radios to complete configuration before the transmitting radio starts sending. 
  
The minimum slot time for a range slot is the sum of:
1. Config buffer time to reconfigure DW at the start of a slot (1 millisecond)
2. Range transaction is 4 packets, time to send 4 packets (set by radio parameters)
3. Turnaround time, there are three turn around times of 2ms (may change)
4. Jitter buffer of 2 ms (subject to change when we get into testing)
  
The minimum slot time for ranging, is the time for a ranging transaction plus config buffer time and Jitter buffer time (3ms currently)
  
  
  
To time the first packet the requesting packet, the sendDelay function will be used. This is the same function that is used in normal ranging on the other packets. 
The time between "StartTxPacket" and TX_RMARKER is the packet preamble. 
  

```
Error: mermaid CLI is required to be installed.
Check https://github.com/mermaid-js/mermaid-cli for more information.

Error: Command failed: npx -p @mermaid-js/mermaid-cli mmdc --theme default --input /tmp/mume-mermaid202324-6867-1hvnpfp.epuui.mmd --output /home/tdsr/DWRadio/driver/DWApp/assets/f561a524d6e198220788a7a13ac8177a0.png
/bin/sh: 1: npx: not found

```  

  
  
<div style="page-break-after: always;"></div>
  
##  Data Slot Timing
  
  
  
In a data slot, there is buffer period at the beginning also to allow radios to change config if needed. In some deployments, some radios may need to change config, the buffer period allow all radios to complete configuration before the transmitting radio starts sending. 
  
Then a sendDelay is used to align the transmitting time of the packet to be aligned in the slot. 
  

```
Error: mermaid CLI is required to be installed.
Check https://github.com/mermaid-js/mermaid-cli for more information.

Error: Command failed: npx -p @mermaid-js/mermaid-cli mmdc --theme default --input /tmp/mume-mermaid202324-6867-1tw4cdg.lmka.mmd --output /home/tdsr/DWRadio/driver/DWApp/assets/f561a524d6e198220788a7a13ac8177a1.png
/bin/sh: 1: npx: not found

```  

{
    "RADIO_SET_NODE_CONFIG_REQUEST": {
        "msgId": 100,
        "nodeId": 140,
        "persistFlag": 1
    }
}
```
  
<div style="page-break-after: always;"></div>
  
## SET STATE Messages
First renamed from Range_State to Radio_State. The three states are IDLE, RANGING and NETWORKING
  
```
{
    "RADIO_SET_STATE_REQUEST": {
        "msgId": 0,
        "state": "RADIO_STATE_NETWORKING",
        "configId": 0,
        "flags": "RADIO_STATE_FLAGS_REPORT_DEBUG_INFO+RADIO_STATE_FLAGS_REPORT_SNIFF_INFO",
        "persistFlag": 0
    }
}
```
  
<div style="page-break-after: always;"></div>
  
## NETWORKING SLOT MAPS Messages
The slot map is an array of slot descriptors. 
Three types of slots, IDLE, RANGE and Data. The idle slot is to put a delay in the slot map, I am not sure I ever seen that used.  
Each slot has a set of parameters.
The period is in milliseconds. 
  
  
```
{
    "NETWORKING_SET_SLOT_MAP_REQUEST": {
        "msgId": 100,
        "slotMap": [
            {
                "slotIdx": 0,
                "slotType": "SLOT_RANGE",
                "configId": 0,
                "ownerId": 140,
                "targetId": 150,
                "period": 20,
                "maxUserData": 10
            },
            {
                "slotIdx": 1,
                "slotType": "SLOT_RANGE",
                "configId": 0,
                "ownerId": 140,
                "targetId": 150,
                "period": 20,
                "maxUserData": 10
            },
            {
                "slotIdx": 2,
                "slotType": "SLOT_RANGE",
                "configId": 0,
                "ownerId": 140,
                "targetId": 150,
                "period": 20,
                "maxUserData": 10
            }
        ],
        "persistFlag": 1
    }
}
```
  
<div style="page-break-after: always;"></div>
  
## SET CONFIG Messages
The config messages change, renamed to radio_ from range. This is because config message is used for both ranging and networking. 
Also, as discussed either node id is moved to a different message.
  
  
```
{
    "RADIO_SET_CONFIG_REQUEST": {
        "msgId": 21,
        "configId": 0,
        "channel": 2,
        "prf": "DWT_PRF_64M",
        "txPreambleLength": "DWT_PLEN_1024",
        "txRxPreambleCode": 9,
        "power": 0,
        "dataRate": "DWT_BR_110K",
        "configFlags": "",
        "antennaDelay": 0,
        "persistFlag": 0
    }
}
```
  
  