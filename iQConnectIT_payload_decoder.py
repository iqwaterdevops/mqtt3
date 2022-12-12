
"""
NBSN95A : CFGMOD = 1  : 25 bytes 
    ASCII messasge string = 72403155615900780c541901000000004200fc023260da7c4e
    device_id = int(data[:12], 16)
    version = int(data[12:16], 16)
    battery_mV = int(data[16:20], 16)
    device_signal = int(data[20:22], 16)
    mod = int(data[22:24], 16)
    temperature = int(data[24:28], 16)
    interrupt = int(data[28:30], 16)
    moisture_mV = int(data[30:34], 16)
    temperatureSH = int(data[34:38], 16)
    humiditySH = int(data[38:42], 16)
    timestamp = int(data[42:50], 16)

NSE01 : 23 bytes
    ASCII messasge string = 41105675049000640d080e026f091e000700
    device_id = int(data[:12], 16)
    version = int(data[12:16], 16)
    battery_mV = int(data[16:20], 16)
    device_signal = int(data[20:22], 16)
    mod = int(data[22:24])
    moisture = int(data[24:28], 16)
    temperature = int(data[28:32], 16)
    conductivityEC = int(data[32:36], 16)
    interrupt = int(data[36:38],16)
    timestamp = int(data[38:46],16)

"""
import json

def hex_json_NBSN95A (data) :

    # dictionary for the payload message
    payload_dict = {"device_id": int(data[:12], 16), "version": int(data[12:16], 16), "battery_V" : (int(data[16:20], 16)/1000) ,"device_signal": int(data[20:22], 16),\
    "mod": int(data[22:24], 16), "device_signal": int(data[20:22], 16), #"temperature" : int(data[24:28], 16), \
    "Bodenfeuchtigkeit": round((int(data[30:34], 16) / 3000 * 100),2),"timestamp": int(data[42:50], 16) }

    # convert to payload message to json
    payload_json = json.dumps(payload_dict)
    return payload_json


# This function converts hex data to json formatted data
def hex_json_NSE01 (data) :

    # dictionary for the payload message
    payload_dict_NSE01 = {"device_id": int(data[:12], 16), "version": int(data[12:16], 16), 
    "battery_V": (int(data[16:20], 16))/int(1000), "device_signal": int(data[20:22], 16), "mod":int(data[22:24]),"temperature" :(int(data[28:32], 16))/100,\
    "Bodenfeuchtigkeit": (int(data[24:28], 16))/100,"conductivityEC":int(data[32:36], 16),"timestamp":int(data[38:46],16)  }

    # convert to payload message to json
    payload_json = json.dumps(payload_dict_NSE01)
    return payload_json


print("===============================================================")
print(hex_json_NBSN95A("411056759210007d0c970c01Ffff00028300000000639722c1"))
print(hex_json_NSE01("41105675957400820cbe0901076d013500120063971969"))