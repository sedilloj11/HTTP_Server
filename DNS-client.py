# Name: John Sedillo
# UCID: jcs89
# Class section: 008

# File name: client.py
# ======================================================================

# ! /usr/bin/env python3
# Echo Client
import sys
import socket
import time
import random
from struct import *

# Get the server host ip, port and hostname request as command line arguments

host = sys.argv[1]
port = int(sys.argv[2])
hostname = (sys.argv[3])
#
typeR = 'A'
classR = 'IN'

attempts = 1

questS = (hostname + " " + typeR + " " + classR)

Mtype = 1
Rcode = -1
ID = random.randint(1, 101)

quest = hostname.encode('utf-8')

answer = ''
count = 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while attempts < 4:

    try:

        print("Sending Request to " + host + ", " + str(port) + ':')
        print("Message ID: %d " % ID)
        print("Question Length:  %d bytes" % len(questS))
        print("Answer Length: %d bytes" % len(answer))
        print("Question: " + questS)
        # https://docs.python.org/3/library/struct.html
        # encapsulating package string/int to bits
        Clientdata = pack('!hhh{}s'.format(len(quest)),  ID, Mtype, Rcode, quest)


        # https://docs.python.org/2/library/time.html#module-time
        # buffer time for Server
        time.sleep(.5)

        #RTT
        starttime = time.time()
        # https: // docs.python.org / 3 / library / socket.html
        clientsocket.settimeout(1.0)

        # sending packet to Server
        clientsocket.sendto(Clientdata, (host, port))

        # Receive the server response
        Serverdata, address = clientsocket.recvfrom(1024)

        # https://docs.python.org/2/library/time.html#module-time
        endtime = time.time()

        RTT = endtime - starttime

        size = len(Serverdata) - 6
        # https://docs.python.org/3/library/struct.html
        ID, Mtype, Rcode,answer = unpack('!hhh{}s'.format(size), Serverdata)
        answer0 = answer.decode('utf-8')

        if Rcode != -1:
            break

    # https://docs.python.org/3/library/socket.html
    # no connection est. due to timeout
    except OSError as msg:
        attempts += 1
        print()
        print ("Timed out")
        print()


print()
print()


if Rcode == 0:

    print("Received Response to " + host + ", " + str(port) + ':')
    print("Return Code: %d"  %Rcode)
    print("Message ID: %d " % ID)
    print("Question Length:  %d bytes" % len(questS))
    print("Answer Length: %d bytes" % len(answer0))
    print("Question: ", questS)
    print("Answer: " + answer0)
elif Rcode == 1:
    print("Received Response to " + host + ", " + str(port) + ':')
    print("Return Code: %d" % Rcode)
    print("Message ID: %d " % ID)
    print("Question Length:  %d bytes" % len(questS))
    print("Answer Length: 0 bytes" )
    print("Question: ", questS)


# Close the client socket
clientsocket.close()