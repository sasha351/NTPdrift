"""
Returns the time from NTP server specified, taken and modified from aallan on GitHub

Attribution:

https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c
"""
import network
import socket
import time
import struct
import machine

def connect_network(ssid, password):
    # Connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

def get_time(host='pool.ntp.org'):
    # NTP Server Communication
    NTP_DELTA = 2208988800
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
    
    secs = struct.unpack("!I", msg[40:44])[0]
    frac = struct.unpack("!I", msg[44:48])[0]
    secs = secs - NTP_DELTA
    millisecs = int(frac * 1000 / 2**32)

    return secs, millisecs

if __name__ == "__main__":
    import yaml

    # Use yaml to get wifi credentials
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
    
    ssid = credentials["Wifi_Name"]
    password = credentials["Wifi_Password"]

    connect_network(ssid, password)
    tm = get_time()
    print(tm)
