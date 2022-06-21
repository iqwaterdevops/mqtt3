import paho.mqtt.client as mqtt
import pymysql.cursors
import sys
import json
import subprocess
import time

#User variable for database name
dbName = "weatherstation"

# it is expected that this Database will already contain one table called mosensor.  Create that table inside the Database with this command:
'''

    create table mosensor(
    device_id VARCHAR(150) NOT NULL, 
    version VARCHAR(150) NOT NULL,  
    battery VARCHAR(150) NOT NULL, 
    device_signal VARCHAR(150) NOT NULL, 
    Bodenfeuchtigkeit VARCHAR(150) NOT NULL,
    last_heard TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );


NBSN95 : CFGMOD = 1  : 25 bytes 
    ASCII messasge string = 72403155615900780c541901000000004200fc023260da7c4e
    device_id = int(data[:12], 16)
    version = int(data[12:16], 16)
    battery_mV = int(data[16:20], 16)
    device_signal = int(data[20:22], 16)
    model = int(data[22:24], 16)
    temperature = int(data[24:28], 16)
    interrupt = int(data[28:30], 16)
    moisture_mV = int(data[30:34], 16)
    temperatureSH = int(data[34:38], 16)
    humiditySH = int(data[38:42], 16)
    timestamp = int(data[42:50], 16)

NSE01 : 18 bytes
    ASCII messasge string = 41105675049000640d080e026f091e000700
    device_id = int(data[:12], 16)
    version = int(data[12:16], 16)
    battery_mV = int(data[16:20], 16)
    device_signal = int(data[20:22], 16)
    moisture = int(data[22:26], 16)
    temperatureSH = int(data[26:30], 16)
    conductivityEC = int(data[30:34], 16)

'''

# User variables for MQTT Broker connection
mqttBroker = "localhost"
mqttBrokerPort = 1883
mqttUser = "iqwatertestbed"
mqttPassword = "iqwater"


# MySQL variables
mysqlHost = "localhost"
mysqlUser = "python_logger"
mysqlPassword = "supersecure"


# This callback function fires when the MQTT Broker conneciton is established.  At this point a connection to MySQL server will be attempted.
# It subscribes to the topic te receive the message.
def on_connect(client, userdata, flags, rc):

    print("MQTT Client Connected")
    client.subscribe("payload")
    try:
        db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPassword, db=dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        db.close()
        print("MySQL Client Connected")
    except:
        sys.exit("Connection to MySQL failed")


# This function converts hex data to json formatted data
def hex_json_NBSN95A (data) :

    # dictionary for the payload message
    payload_dict = {"device_id": int(data[:12], 16), "version": int(data[12:16], 16), #"model": int(data[22:24], 16), 
    "battery": int(data[16:20], 16), "device_signal": int(data[20:22], 16), #"moisture_mV": int(data[30:34], 16), 
    "Bodenfeuchtigkeit": round((int(data[30:34], 16) / int(3000) * 100),2) }

    # convert to payload message to json

    payload_json = json.dumps(payload_dict)
    return payload_json


# This function converts hex data to json formatted data
def hex_json_NSE01 (data) :

    # dictionary for the payload message
    payload_dict_NSE01 = {"device_id": int(data[:12], 16), "version": int(data[12:16], 16), 
    "battery": int(data[16:20], 16), "device_signal": int(data[20:22], 16), "Bodenfeuchtigkeit": (int(data[22:26], 16))/100 }

    # convert to payload message to json

    payload_json = json.dumps(payload_dict_NSE01)
    return payload_json



# This function updates the sensor's information in the sensor index table
def sensor_update(db, payload):

    cursor = db.cursor()
    insertRequest = "INSERT INTO mosensor(device_id, version, battery, device_signal, Bodenfeuchtigkeit, last_heard) VALUES(%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)" % (payload['device_id'], payload['version'], payload['battery'], payload['device_signal'], payload['Bodenfeuchtigkeit'])
    cursor.execute(insertRequest)
    db.commit()



# The callback for when a PUBLISH message is received from the MQTT Broker.
def on_message(client, userdata, msg):

    print("Transmission received")
    MQTTpayload = (msg.payload).decode("utf-8")

    # messsage length for the NBSN95A is 25 bytes = 50 characters in the message string
    if (len(MQTTpayload) == 50):
        # MQTTpayload = (msg.payload).decode("utf-8")
        payload_json = hex_json_NBSN95A(MQTTpayload)
        payload = json.loads(payload_json)
        db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPassword, db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        sensor_update(db,payload)
        print('data logged')
        db.close()

    # messsage length for the NSE01 is 18 bytes = 36 characters in the message string
    elif(len(MQTTpayload) == 36):
        # MQTTpayload = (msg.payload).decode("utf-8")
        payload_json = hex_json_NSE01(MQTTpayload)
        payload = json.loads(payload_json)
        db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPassword, db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        sensor_update(db,payload)
        print('data logged')
        db.close() 

    else :
        print("Incorrect messsage format, Please check the CFGMOD")
    
    return 'subscribing completed'


# Connect the MQTT Client
def execute():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=mqttUser, password=mqttPassword)

    try:
        client.connect(mqttBroker, mqttBrokerPort)
    except:
        sys.exit("Connection to MQTT Broker failed")

    if on_message == 'subscribing completed':
        time.sleep(2)
        subprocess.call("Mosquitto_Publisher.py", shell=True)


    # Stay connected to the MQTT Broker indefinitely
    client.loop_forever()

if  __name__ == '__main__':
    execute()

