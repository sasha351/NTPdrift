"""
Supplies functions that connect to WiFi network and get the 
time from NTP server specified, taken and modified from aallan on GitHub

Attribution:

https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c
"""
import network
import socket
import time
import struct
import machine

NTP_DELTA = 2208988800

def connect_network(ssid, password):
    """
    Connects to a WiFi network using provided credentials
    
    Args:
        ssid (str): Network name
        password (str): Network password
    """

    # Initialize, activate, and connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait and check if connection has been established
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Raise an error upon failed connection or print IP
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

def get_time(host):
    """
    Retrieves current time from an NTP server
    
    Args:
        host (str): NTP server hostname
    
    Returns:
        tuple: First index is epoch time, second index is milliseconds timestamp
    """
    # NTP protocol constraints
    NTP_QUERY = bytearray(48) 
    NTP_QUERY[0] = 0x1B

    addr = socket.getaddrinfo(host, 123)[0][-1] # Resolve NTP server address

    # Create UDP socket for NTP query
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    
    epoch = struct.unpack("!I", msg[40:44])[0] # Extract epoch time from NTP response
    epoch -= NTP_DELTA

    frac = struct.unpack("!I", msg[44:48])[0] # Extract fractional time from NTP response
    millisecs = int(frac * 1000 / 2**32) # Convert fractional time to milliseconds

    return epoch, millisecs

def set_time(host):
    """
    Retrieves the board's time to NTP server time
    
    Args:
        host (str): NTP server hostname
    
    Returns:
        Nothing
    """
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3] - 5, tm[4], tm[5], 0))

if __name__ == "__main__":
    import json

    # Use JSON to get WiFi credentials
    with open("credentials.json", "r") as file:
        credentials = json.load(file)
    
    ssid = credentials["Wifi_Name"]
    password = credentials["Wifi_Password"]

    connect_network(ssid, password)
    tm = get_time()
    print(tm)
