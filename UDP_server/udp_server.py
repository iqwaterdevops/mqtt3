#!/usr/bin/python3
 
import socket
import sys
from paho.mqtt import publish
from UDP_iQConnectIT_payload_decoder_NewFW import *
import mysql.connector

UDP_IP = "0.0.0.0"  # listen on all the available ip address of the linux
UDP_PORT = 20002
creds = {'username': 'iqwatertestbed', 'password': '!Qwassert3stbed'}
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("UDP server up and listening")

# MySQL settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'python_logger'
MYSQL_PASSWORD = 'supersecure'
MYSQL_DATABASE = 'weatherstation'


# Connect to the MySQL database
db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()


while True:
    try:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        clientMsg = data #.decode('ascii') # need to the udp messages. they have different payload compared to the mqtt payload
        #clientMsg = "Message from Client:{}".format(data)
        print(clientMsg)
        hex_json_NDDS75(data)
        # topic = 'test'
        # publish.single("%s" %topic, clientMsg, hostname= UDP_IP, auth=creds)

        sql = "INSERT INTO tank_level (device_id, version, battery, device_signal, Tank_Level, last_heard,) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP"  # Adjust column names
        values = (parsed_data['value1'], parsed_data['value2'], parsed_data['value3'])  # Adjust column values
        cursor.execute(sql, values)
        db.commit()

    except KeyboardInterrupt:
        sock.close()
        sys.exit()
    except:
        continue
