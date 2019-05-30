#! /usr/bin/env python

# Club Ignition

import sys
import struct
import socket
import time
from gpiozero import Button
from signal import pause

# Configuration Variables
broadcast_address = '192.168.1.255'
wol_port = 9
projector_port = 4352
power_on = "%1POWR 1"
power_off = "%1POWR 0"
power_query = "%1POWR ?"
pj_response_buffer_size = 160

computers = {
    'Computer-Name': '00:11:22:33:44:55',
}

projectors = {
    'Projector Name': '192.168.1.2',
}


def WakeOnLan(ethernet_mac):
    ethernet_mac = ethernet_mac.replace(':', '')
    print(ethernet_mac)

    if len(ethernet_mac) != 12:
        # Illegal MAC Address
        return

    data = ''.join(['FFFFFFFFFFFF', ethernet_mac * 20])
    send_data = b''

    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    soc.sendto(send_data, (broadcast_address, wol_port))
    soc.close()


def CommandProjector(projector, action):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((projector, projector_port))
    soc.send(action + "\r")
    response = soc.recv(pj_response_buffer_size)
    if "PJLINK 0" == response:
        soc.send(action + "\r")
        response = soc.recv(pj_response_buffer_size)
    soc.close()
    print(response)


def ProjectorsOn():
    for projector in projectors:
        CommandProjector(projectors[projector], power_on)


def ProjectorsOff():
    for projector in projectors:
        CommandProjector(projectors[projector], power_off)


def ProjectorsStatus():
    for projector in projectors:
        print(projector)
        CommandProjector(projectors[projector], power_query)


def ComputersOn():
    for computer in computers:
        WakeOnLan(computers[computer])

def ClubOn():
    ComputersOn()
    ProjectorsOn()

def ClubOff():
    ProjectorsOff()

def TurnClubOn():
    print("Club On")
    ClubOn()

def TurnClubOff():
    print("Club Off")
    ClubOff()

#ComputersOn()
#ProjectorsOn()
onButton = Button(17, hold_time=3)
offButton = Button(27, hold_time=3)
onButton.when_held = TurnClubOn
offButton.when_held = TurnClubOff

pause()
