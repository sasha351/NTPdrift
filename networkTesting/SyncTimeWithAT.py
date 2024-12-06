"""
Uses PicoLTE module and atcom.send_at_comm() function to send AT commands.
Commands will connect board to network and then ask the 4G network itself for the time.
This script does not sync the boards time, it just asks for the time and prints it.
"""
from pico_lte.core import PicoLTE
import time
import json

with open("credentials.json", "r") as file:
    credentials = json.load(file)

apn = credentials["APN"]

picoLTE = PicoLTE()

AT_commands = ["AT+CFUN=1", "AT+CGATT=1", f'AT+CGDCONT=1,"IP","{apn}"', "AT+CCLK?"]

"""
AT+CFUN=1:
Enables full functionality of the modem, allows for network connection

AT+CGATT=1:
Attatched the device to the packet-switched service of the network.
Needed for data communication (data recieving and transmitting)

AT+CGDCONT=1,"IP","APN":
Configures the packet data protocol context for the modem.
1 -> identifies the session
IP -> specifies the type of connection
super -> APN, access point name for the network

AT+CCLK?:
Asks the network for the time
"""

for comm in AT_commands:
    res = picoLTE.atcom.send_at_comm(comm)
    print(res)
    time.sleep(1)

