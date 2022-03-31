import paho.mqtt.client as mqtt
import pymysql.cursors
import sys
import json


#User variable for database name
dbName = "weatherstation"

# it is expected that this Database will already contain one table called mosensor.  Create that table inside the Database with this command:
'''
create table mosensor(
    device_id VARCHAR(150) NOT NULL, 
    version VARCHAR(150) NOT NULL, 
    model VARCHAR(150) NOT NULL, 
    battrey VARCHAR(150) NOT NULL, 
    device_signal VARCHAR(150) NOT NULL, 
    moisture_mv VARCHAR(150) NOT NULL, 
    last_heard TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    ASCII messasge string = 72403155615900780c541901000000004200fc023260da7c4e
    device_id = int(data[:12], 16)
    version = int(data[12:16], 16)
    battrey_mV = int(data[16:20], 16)
    device_signal = int(data[20:22], 16)
    model = int(data[22:24], 16)
    temperature = int(data[24:28], 16)
    interrupt = int(data[28:30], 16)
    moisture_mV = int(data[30:34], 16)
    temperatureSH = int(data[34:38], 16)
    humiditySH = int(data[38:42], 16)
    timestamp = int(data[42:50], 16)
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
def hex_json (data) :

    # dictionary for the payload message
    payload_dict = {"device_id": int(data[:12], 16), "version": int(data[12:16], 16), "model": int(data[22:24], 16), 
    "battrey": int(data[16:20], 16), "device_signal": int(data[20:22], 16), "moisture_mV": int(data[30:34], 16), "Bodenfeuchtigkeit": (int(data[30:34], 16) / int(data[16:20], 16) * 100) }

    # convert to payload message to json

    payload_json = json.dumps(payload_dict)
    return payload_json



# This function updates the sensor's information in the sensor index table
def sensor_update(db, payload):

    cursor = db.cursor()
    insertRequest = "INSERT INTO mosensor(device_id, version, model, battrey, device_signal, moisture_mv, Bodenfeuchtigkeit, last_heard) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)" % (payload['device_id'], payload['version'], payload['model'], payload['battrey'], payload['device_signal'], payload['moisture_mV'], payload['Bodenfeuchtigkeit'])
    cursor.execute(insertRequest)
    db.commit()



# The callback for when a PUBLISH message is received from the MQTT Broker.
def on_message(client, userdata, msg):

    print("Transmission received")
    MQTTpayload = (msg.payload).decode("utf-8")
    payload_json = hex_json(MQTTpayload)
    payload = json.loads(payload_json)
    db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPassword, db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    sensor_update(db,payload)
    #log_telemetry(db,payload)
    print('data logged')
    db.close()


# Connect the MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=mqttUser, password=mqttPassword)

try:
    client.connect(mqttBroker, mqttBrokerPort)
except:
    sys.exit("Connection to MQTT Broker failed")



# Stay connected to the MQTT Broker indefinitely
client.loop_forever()
