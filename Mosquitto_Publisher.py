import paho.mqtt.client as mqtt
import sys
import json


# User variables for MQTT Broker connection
mqttBroker = "localhost"
mqttBrokerPort = 1883
mqttUser = "iqwatertestbed"
mqttPassword = "iqwater"


# Configuation command
config_cmd = "01000BB8"

def on_connect(client, userdata, flags, rc):
    print("Publisher MQTT Client Connected")

def on_publish(client, config_cmd, result):
    print("Configuration published \n")
    pass

# Publishing the configuration messasge
client1 = mqtt.Client("publisher")
client1.username_pw_set(username=mqttUser, password=mqttPassword)
client1.on_connect = on_connect
client1.on_publish = on_publish

try:
    client1.connect(mqttBroker, mqttBrokerPort)
    ret = client1.publish(topic = "configuration", payload = config_cmd)
except:
    sys.exit("Connection to MQTT Broker failed")

