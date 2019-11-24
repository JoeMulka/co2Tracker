import time
import board
import busio
import adafruit_sgp30
import csv
import argparse
from atmos import calculate

DEFAULT_HOURS = 12


def calculateAbsoluteHumidity(rel_humidity, temperature):
    temp_kelvin = temperature + 273.15
    absolute_humidity = calculate('AH', RH=rel_humidity, p=1e5, T=temp_kelvin, debug=True)[0]
    # convert from kg/m^3 to g/m^3
    absolute_humidity = absolute_humidity * 1000
    return absolute_humidity

parser = argparse.ArgumentParser()
parser.add_argument("--num_hours", type = int, help = "how many hours to run the logger", default = DEFAULT_HOURS)
args = parser.parse_args()

sgp30_i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(sgp30_i2c)

#print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x898f, 0x8b77)

# Get current epoch time
start_time = time.time()
end_time = start_time + (args.num_hours * 3600)
current_time = start_time

formatted_start_time = time.strftime("%y_%m_%d_%H_%M")

try:
    while current_time < end_time:
        current_time = time.time()
        line = [str(current_time), sgp30.eCO2, sgp30.TVOC]
        with open("{}.csv".format(formatted_start_time), 'a') as logfile:
            mywriter = csv.writer(logfile)
            mywriter.writerow(line)
        baseline_line = [str(current_time), sgp30.baseline_eCO2, sgp30.baseline_TVOC]
        with open("{}_baseline.csv".format(formatted_start_time),'a') as baseline_log:
            mywriter = csv.writer(baseline_log)
            mywriter.writerow(baseline_line)
        time.sleep(5)
    print("{} hours of logging complete".format(args.num_hours))

except KeyboardInterrupt as key_int:
     print("logging terminated")
     exit(0)
