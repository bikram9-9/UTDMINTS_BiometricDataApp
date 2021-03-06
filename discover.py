"""
    Modified discover_glasses_on_network.py example provided by Tobii.
    Module handles sending and receiving discovery info from glasses on network.

    Tested with Python 3.7 on Windows 10 and MSYS2 64-bit
    Uses gsocket and not python sockets.
    For ethernet connection only.
"""

import socket
import struct
import json

MULTICAST_ADDR = 'ff02::1'  # all ipv6 devices with link-local scope
#ETH_ADPT = 'fe80::39ee:1ac:d51d:2e80'  #ipv6 of ethernet adapter
ETH_IF = 'fe80::f430:a788:aae4:132c%7'  #ipv6 of ethernet interface
PORT = 13007  # Port used by RU


def discover():
    """ Sends discovery info to glasses on WLAN.
        Returns the IPv6 of the glasses that recived the discovery-message.
    """
    # Create udp socket
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    # Avoid error 'Adress already in use'
    s6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Associate the socket with a specific network interface & port number
    s6.bind((ETH_IF, PORT))  # for ethernet connection
    #s6.bind((ETH_ADPT, PORT)) # for connection with ethernet adapter
    #s6.bind(('::', PORT))  # for wifi connection
    # send data/msg to socket
    s6.sendto('{"type":"discover"}'.encode(), (MULTICAST_ADDR, 13006))

    print("Press Ctrl-C to abort...")
    while True:
        data, address = s6.recvfrom(1024)
        # covert data to str
        print(" From: " + address[0] + " " + data.decode())
        break
    s6.close()
    return address[0]

    #for wifi only
    #turn JSON encoded data into Python obj
    #data = json.loads(data)
    # get ip address from data, only wifi returns an ipv4 address
    #glasses_IP = data['ipv4']
    #break
    #return glasses_IP
