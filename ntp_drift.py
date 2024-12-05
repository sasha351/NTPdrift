import ntp_utils
import yaml
import csv

# Get WiFi Credentials with YAML
with open("credentials.yaml", "r") as file:
    credentials = yaml.safe_load(file)

ssid = credentials["Wifi_Name"]
password = credentials["Wifi_Password"]

# Connect board to WiFi
ntp_utils.connect_network(ssid, password)

# Set initial time on board to agree with NTP server
initial_time = ntp_utils.get_time()
