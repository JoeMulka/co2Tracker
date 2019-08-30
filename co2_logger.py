""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import time
import board
import busio
import adafruit_sgp30
import csv

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

#print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

elapsed_sec = 0

#def formatLine(current_time, co2_value, tvoc_value):
#    return ("{},{},{}\n".format(current_time, co2_value, tvoc_value))

baseline_counter = 11
try:
    while True:
        baseline_counter += 1
        current_time = str(time.time())
        line = [current_time, sgp30.eCO2, sgp30.TVOC]
        with open("log_co2.csv", 'a') as logfile:
            mywriter = csv.writer(logfile)
            mywriter.writerow(line)
        # Write the baseline every 60 seconds
        if baseline_counter == 12:
            baseline_line = [current_time, sgp30.baseline_eCO2, sgp30.baseline_TVOC]
            with open("baseline_log.csv",'a') as baseline_log:
                mywriter = csv.writer(baseline_log)
                mywriter.writerow(baseline_line)
            baseline_counter = 0
        time.sleep(5)
except KeyboardInterrupt as key_int:
     print("logging terminated")
     exit(0)
