# Name: John Sedillo
# UCID: jcs89
# Class section: 008

# File name: dnsserver.py
# ======================================================================
# ! /usr/bin/env python3
# Echo Server
import sys
import socket
import time
import random
from struct import *

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

answer = ''
DNS_init = {}
IP = []
counter = 0

file = open('dns-master.txt','r')
lines = file.readlines()




# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    Clientdata, address = serverSocket.recvfrom(1024)
    size = len(Clientdata) - 6
    ID, Mtype, Rcode, hostname = unpack('!hhh{}s'.format(size), Clientdata)

    question = hostname.decode('utf-8')

    # searching DNS list for hostname request
    for i in range(len(lines)):
        line = lines[i]
        answer = ''
        if question in line:
            answer = line
            Rcode = 0
            break

        else:
            Rcode = 1
            line = "not found"

    answ = line.encode('utf-8')

    # https://docs.python.org/2/library/random.html,
    # https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/

    # simulate delay
    delay = random.uniform(0.0, 1.5)
    time.sleep(delay)

    print(answer)
    if  delay < 1 :
        # echo back to client
        print("Responding to ping request")
        # sending packets to client
        Serverdata = pack('!hhh{}s'.format(len(answ)), ID,Mtype,Rcode,answ)
        serverSocket.sendto(Serverdata, address)

    else:
        print("Message timed out")
