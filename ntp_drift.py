import ntp_utils
import json
import machine
import time

"""
Notes:
- return network connection from utils and add checking for network connection to see if its still active
"""
MAX_BUFFER_SIZE = 10
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
with open('time_drift.csv', 'w') as file:
    file.write("Board_Time, NTP_Time, Difference\n")

# Set the time of the board
for i in range(10): # try 10 times until quitting
    try:
        ntp_utils.set_time(host)
        break
    except:
        time.sleep(1)
        print('trying to set time...')

# Verify the time was set
current_time = rtc.datetime()
print(f"Board time set to: {current_time}")

# Start monitoring loop
buffer = [] # initalize buffer to reduce I/O overhead
try:
    while True:
        # Get board and NTP time
        # Try to get time from the server, if there is an error then restart the loop
        try:
            secs, millisecs = ntp_utils.get_time(host) # get NTP server time
            board_time = time.time_ns() // 10**6 # get board time in milliseconds

            millisecs += millisecs + secs * 1000

            diff_ms = abs(board_time - millisecs) # time difference in milliseconds
            
            output_line = "%s, %s, %s\n"%(board_time, millisecs, diff_ms) # format output line
            
            buffer.append(output_line) # 

            # Write to text file if buffer size hit
            if len(buffer) >= MAX_BUFFER_SIZE:
                with open('time_drift.csv', 'a') as file:
                    for line in buffer:
                        file.write(line)
                buffer = []  # clear buffer
            
            print(output_line)

        except:
            print("Error in drift monitoring.\n")
            
        # Wait for specified period
        time.sleep(WAIT_PERIOD)
        
except (SystemExit, KeyboardInterrupt, Exception):
    if buffer:
        with open('time_drift.csv', 'a') as file:
            for line in buffer:
                    file.write(line)

    print("\nMonitoring stopped")