from pico_lte.utils.atcom import ATCom
from pico_lte.common import debug
import machine
import time

def print_sys_time(rtc):
    current_time = rtc.datetime()
    formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[0],  # Year
        current_time[1],  # Month
        current_time[2],  # Day
        current_time[3],  # Hour
        current_time[4],  # Minute
        current_time[5]   # Second
    )

    print(formatted_time)
    return

rtc = machine.RTC()

print_sys_time(rtc)

#debug.set_level(0)
atcom = ATCom()
time.sleep(5)
commands = ["AT+CMEE=1", "AT+CREG?", "AT+CSQ", "AT+CCLK?"]

for comm in commands:
    res = atcom.send_at_comm(comm)
    print(res)
    
print_sys_time(rtc)
