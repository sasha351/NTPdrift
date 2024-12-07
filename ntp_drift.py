import ntp_utils
import json
import machine
import time

"""
Notes:
- return network connection from utils and add checking for network connection to see if its still active
"""
# NTP_DELTA necessary for time adjustment
NTP_DELTA = 1751529000
MINUTES = 5
WAIT_PERIOD = MINUTES * 60

rtc = machine.RTC()

# Get WiFi Credentials with YAML
with open("credentials.json", "r") as file:
    credentials = json.load(file)

ssid = credentials["Wifi_Name"]
password = credentials["Wifi_Password"]
host = credentials["NTP_Host"]

# Connect board to WiFi
ntp_utils.connect_network(ssid, password)

# Create text file with headers
with open('time_drift.txt', 'w') as file:
    file.write("Board_Time, NTP_Time, Difference\n")

# Set the time of the board
set_time = 10   # number of tries to set the time
while set_time > 0:
    try:
        ntp_utils.set_time(host)
        break
    except:
        set_time -= 1
        time.sleep(1)
        print('trying to set time...')

# Verify the time was set
current_time = rtc.datetime()
print(f"Board time set to: {current_time}")

# Start monitoring loop
try:
    while True:
        # Get board and NTP time
        # Try to get time from the server, if there is an error then restart the loop
        try:
            ntp_time_s, ntp_time_ms = ntp_utils.get_time(host)
        except:
            continue
        board_time = time.time_ns() // 10**6    # get time in milliseconds

        # Format NTP time
        ntp_time_ms = ntp_time_s + (ntp_time_s * 1000) # convert time to milliseconds

        # Find the difference between times
        diff_ms = abs(board_time - ntp_time_ms) # time difference in milliseconds
        diff_ms = abs(diff_ms - NTP_DELTA) # adjust time difference
        
        # Format output line
        output_line = "%s, %s, %s\n"%(board_time, ntp_time_ms, diff_ms)
        
        # Write to text file
        with open('time_drift.txt', 'a') as file:
            file.write(output_line)
        
        print(output_line)
            
        # Wait for specified period
        time.sleep(WAIT_PERIOD)
        
except KeyboardInterrupt:
    print("\nMonitoring stopped")
