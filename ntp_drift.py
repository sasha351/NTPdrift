import ntp_utils
import yaml
import machine
import csv
import time

"""
Notes:
- return network connection from utils and add checking for network connection to see if its still active
"""

NTP_DELTA = 2208988800
MINUTES = 5
WAIT_PERIOD = MINUTES * 60

rtc = machine.RTC()

# Get WiFi Credentials with YAML
with open("credentials.yaml", "r") as file:
    credentials = yaml.safe_load(file)

ssid = credentials["Wifi_Name"]
password = credentials["Wifi_Password"]

# Connect board to WiFi
ntp_utils.connect_network(ssid, password)

# Set initial time on board to agree with NTP server
initial_time = ntp_utils.get_time()

# Convert NTP timestamp to datetime tuple with milliseconds
tm = time.localtime(initial_time)
milliseconds = (time.time_ns() // 1_000_000) % 1000  # Get current milliseconds

# RTC datetime format: (year, month, day, weekday, hours, minutes, seconds, subseconds)
# Convert milliseconds to subseconds (0-255 range)
subseconds = int((milliseconds / 1000) * 255)

rtc.datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], subseconds))

# Verify the time was set
current_time = rtc.datetime()
print(f"Board time set to: {current_time}")