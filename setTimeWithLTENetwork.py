import utime
import machine

rtc = machine.RTC()

# machine time before altering
print(rtc.datetime())
current_time = utime.localtime()
formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[0],  # Year
        current_time[1],  # Month
        current_time[2],  # Day
        current_time[3],  # Hour
        current_time[4],  # Minute
        current_time[5]   # Second
    )
print(formatted_time)

# changing machine time and reprinting
rtc.datetime((2024,11,19,2,10,30,0,0))
print(rtc.datetime())
current_time = utime.localtime()
formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[0],  # Year
        current_time[1],  # Month
        current_time[2],  # Day
        current_time[3],  # Hour
        current_time[4],  # Minute
        current_time[5]   # Second
    )

print(formatted_time)
