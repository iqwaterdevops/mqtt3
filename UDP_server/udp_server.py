#!/usr/bin/python3
 
import socket
import sys
from paho.mqtt import publish
 
UDP_IP = "0.0.0.0"  # listen on all the available ip address of the linux
UDP_PORT = 20001
creds = {'username': 'iqwatertestbed', 'password': '!Qwassert3stbed'}
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("UDP server up and listening")
 
while True:
    try:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        clientMsg = data #.decode('ascii') # need to the udp messages. they have different payload compared to the mqtt payload
        #clientMsg = "Message from Client:{}".format(data)
        print(clientMsg)
        topic = 'test'        
        publish.single("%s" %topic, clientMsg, hostname= UDP_IP, auth=creds)
    except KeyboardInterrupt:
        sock.close()
        sys.exit()
    except:
        continue
