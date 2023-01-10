
import binascii
import json

udp_data = b'\xf8gxpP@2\x15\x00~\x0e\x19\x11\x01\xff\xff\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00' #  NBSN959A
#udp_data = b'A\x10Vu\x04\x90\x00\x82\r5\x12\x01\x00\x00\x08>\x00\x00\x00c\xbc\x1aC' # NSE01
udp_data = binascii.hexlify(udp_data).decode('ascii')


def hex_json_NBSN95A (data) :

    # NBSN95A_firmware version 1.2.6
    # configuration mode =1
    data = udp_data
    a95_device_id = udp_data[1:16]
    a95_version = udp_data[16:20]
    a95_battery = udp_data[20:24]
    a95_signal_strength = udp_data[24:26]
    a95_mod = udp_data[26:28]
    a95_ds18b20_temperature = udp_data[28:32]
    a95_digital_interrupt = udp_data[32:34]
    a95_adc = udp_data[34:38]
    a95_sht2031_temperature = udp_data[38:42]
    a95_sht2031_humidity = udp_data[42:46]
    a95_timestamp = udp_data[46:54]


    # dictionary for the payload message
    payload_dict = {"device_id": a95_device_id, "version": int(a95_version, 16), "battery_V" : (int(a95_battery, 16)/1000) ,"device_signal": int(a95_signal_strength, 16),\
    "mod": int(data[22:24], 16), "device_signal": int(data[20:22], 16), #"temperature" : int(data[24:28], 16), \
    "Bodenfeuchtigkeit (%)": round((int(a95_adc, 16) / 3000 * 100),2),"timestamp": int(a95_timestamp, 16) }


    # convert to payload message to json
    payload_json = json.dumps(payload_dict)
    return payload_json


# This function converts hex data to json formatted data
def hex_json_NSE01 (data) :

    # NSE01_firmware version 1.3.2
    # configuration mode = 1
    data = udp_data
    ns01_device_id = udp_data[1:16]
    ns01_version = udp_data[16:20]
    ns01_battery = udp_data[20:24]
    ns01_signal_strength = udp_data[24:26]
    ns01_mod = udp_data[26:28]
    ns01_interrupt = udp_data[28:30]
    ns01_soilMoisture = udp_data[30:34]
    ns01_soilTemperature = udp_data[34:38]
    ns01_soilConductivity = udp_data[38:42]
    ns01_soilDielectric = udp_data[42:46]
    ns01_timestamp = udp_data[46:54]

    # dictionary for the payload message
    payload_dict_NSE01 = {"device_id": int(ns01_device_id, 16), "version": int(ns01_version, 16), 
    "battery_V": (int(ns01_battery, 16))/int(1000), "device_signal": int(ns01_signal_strength, 16), "mod":int(data[22:24]),"temperature" :(int(ns01_soilTemperature, 16))/100,\
    "Bodenfeuchtigkeit": (int(ns01_soilMoisture, 16))/100,"conductivityEC":int(ns01_soilConductivity, 16),"timestamp":int(ns01_timestamp,16)}

    # convert to payload message to json
    payload_json = json.dumps(payload_dict_NSE01)
    return payload_json


print("===============================================================")
print('udp_data_hexstring : {udp_data}')
print(hex_json_NBSN95A(udp_data))