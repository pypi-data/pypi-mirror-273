import json

filename = '../logfiles/April_2024/Unit100_to_101_0000.json'
logfile = open(filename,"r")
data = json.loads(logfile.read())
logfile.close()
for k in range(len(data)):
    if "RANGE_INFO" in data[k]:
        print("Precision Range:", data[k]['RANGE_INFO']['precisionRangeM'])
print("\nExample JSON message:\n", data[100])
print("\nRecords in logfile:", len(data))
