
import binascii
import json

# Sample UDP NBSN95A (advanced)
#udp_data = b'\xf8gxpP@2\x15\x00~\x0e\x19\x11\x01\xff\xff\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00'

# Sample UDP NSE01 (basic)
#udp_data = b'A\x10Vu\x04\x90\x00\x82\r;\x11\x01\x00\x00\x08\xfd\x00\x00\x00d\x11\xa22' 

# Sample UDP Tank Level message
udp_data = b'\xf8gxpRg\x96\x14\x00\x98\r3\x0e\x01\x00\x00\xfad\x90\x80@\x00\xfad\x89\xd5i\x00\xfad\x89\xd1\xe5\x00\xfad\x89\xcea\x00\xfad\x89\xca\xdd\x00\xfad\x89\xc7Y\x00\xfad\x89\xc2\x05\x00\xfad\x89\xbe\x81\x00\xfad\x89\xb6:'
udp_data = binascii.hexlify(udp_data).decode('ascii')

# This function converts hex data to json formatted data ------------------------------------NBSN95A (1.2.6)-----------------------------------------------------
def hex_json_NBSN95A (data) :

    # UDP Port 20001
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


# This function converts hex data to json formatted data ----------------------------------------- NS01 (1.3.2) ----------------------------------------------------
def hex_json_NSE01 (data) :

    # UDP Port 20001
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
    payload_dict_NSE01 = {"device_id": ns01_device_id, "version": int(ns01_version, 16),"battery_V": (int(ns01_battery, 16))/int(1000), \
                          "device_signal": int(ns01_signal_strength, 16),"mod":int(data[22:24]),"temperature" :(int(ns01_soilTemperature, 16))/100,\
                            "Bodenfeuchtigkeit": (int(ns01_soilMoisture, 16))/100,"conductivityEC":int(ns01_soilConductivity, 16)}
    #,"timestamp":int(ns01_timestamp,16)
    # convert to payload message to json
    payload_json = json.dumps(payload_dict_NSE01)
    return payload_json


# This function converts hex data to json formatted data-----------------------------------NDDS75 (1.5.2)-----------------------------------------------------------
def hex_json_NDDS75 (data) :
    
    # UDP Port = 20002
    # NSE01_firmware version 1.5.2
    # configuration mode = 1
    
    data = udp_data
    nd75_device_id = udp_data[1:16]
    nd75_version = udp_data[16:20]                                                                                                                 
    nd75_battery = udp_data[20:24]
    nd75_signal_strength = udp_data[24:26]
    nd75_mod = udp_data[26:28]
    nd75_interrupt = udp_data[28:30]
    nd75_tankLevel = udp_data[30:34]
    nd75_timeStamp = udp_data[34:42]
    nd75_meas1 = udp_data[42:46]
    nd75_time1 = udp_data[46:54]
    nd75_meas2 = udp_data[54:58]
    nd75_time2 = udp_data[58:66]
    nd75_meas3 = udp_data[66:70]
    nd75_time3 = udp_data[70:78]
    nd75_meas4 = udp_data[78:82]
    nd75_time4 = udp_data[82:90]
    nd75_meas5 = udp_data[90:94]
    nd75_time5 = udp_data[94:102]
    nd75_meas6 = udp_data[102:106]
    nd75_time6 = udp_data[106:114]
    nd75_meas7 = udp_data[114:118]
    nd75_time7 = udp_data[118:126]
    nd75_meas8 = udp_data[126:130]
    nd75_time8 = udp_data[130:138]


    # dictionary for the payload message
    payload_dict_NDDS75 = {"device_id": nd75_device_id, "version": int(nd75_version, 16),"battery_V": (int(nd75_battery, 16))/int(1000), \
                           "device_signal": int(nd75_signal_strength, 16),"mod":int(nd75_mod, 16),"timestamp": (int(nd75_timeStamp, 16)),"TankLevel(mm)": (int(nd75_tankLevel, 16)),\
                            "time1" : (int(nd75_time1, 16)),"meas1" : (int(nd75_meas1, 16)),"time2" : (int(nd75_time2, 16)),"meas2" : (int(nd75_meas2, 16)),\
                                "time3" : (int(nd75_time3, 16)),"meas3" : (int(nd75_meas3, 16)),"time4" : (int(nd75_time4, 16)),"meas4" : (int(nd75_meas4, 16)),\
                                    "time5" : (int(nd75_time5, 16)),"meas5" : (int(nd75_meas5, 16)),"time6" : (int(nd75_time6, 16)),"meas6" : (int(nd75_meas6, 16)),\
                                        "time7" : (int(nd75_time7, 16)),"meas7" : (int(nd75_meas7, 16)),"time8" : (int(nd75_time8, 16)),"meas8" : (int(nd75_meas8, 16))}
    
    # convert to payload message to json
    payload_json = json.dumps(payload_dict_NDDS75)
    return payload_json


print("===============================================================")
print('udp_data_hexstring : {udp_data}')
print(udp_data)
#print(hex_json_NBSN95A(udp_data))
#print(hex_json_NSE01(udp_data))
print(hex_json_NDDS75(udp_data))