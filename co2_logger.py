import time
import board
import busio
import adafruit_sgp30
import csv
import argparse
from atmos import calculate
import adafruit_si7021

# Constants
DEFAULT_HOURS = 12
# How many seconds between reads
seconds_between_reads = 5
# Only need to measure and set humidity every minute
humidity_frequency = 60
humidity_counter = humidity_frequency # so that it sets on the first iteration of the loop
# TODO: Need to get outdoor baseline and hardcode it here as constant

def calculateAbsoluteHumidity(rel_humidity, temperature):
    temp_kelvin = temperature + 273.15
    absolute_humidity = calculate('AH', RH=rel_humidity, p=1e5, T=temp_kelvin, debug=True)[0]
    # convert from kg/m^3 to g/m^3
    absolute_humidity = absolute_humidity * 1000
    return absolute_humidity

parser = argparse.ArgumentParser()
parser.add_argument("--num_hours", type = int, help = "how many hours to run the logger", default = DEFAULT_HOURS)
parser.add_argument("--testing", action="store_true", help = "activate testing mode")
args = parser.parse_args()

# co2 and volatile organic compound sensor
sgp30_i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(sgp30_i2c)

# Humidity and temperature sensor
si_7021_i2c = busio.I2C(board.SCL, board.SDA)
temp_humid_sensor = adafruit_si7021.SI7021(si_7021_i2c)

# Create library object on our I2C port
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x898f, 0x8b77)

# Get current epoch time
start_time = time.time()
end_time = start_time + (args.num_hours * 3600)
current_time = start_time

formatted_start_time = time.strftime("%y_%m_%d_%H_%M")



try:
    while current_time < end_time:
        # If it's been a minute, set the humidity
        if (humidity_counter >= humidity_frequency):
            temp = temp_humid_sensor.temperature
            relative_humidity = temp_humid_sensor.relative_humidity
            absolute_humidity = calculateAbsoluteHumidity(relative_humidity, temp)
            sgp30.set_iaq_humidity(absolute_humidity)
            # Reset the counter
            humidity_counter = 0
        current_time = time.time()
        # write time, c02, and volatile organic compound readings
        line = [str(current_time), sgp30.eCO2, sgp30.TVOC]
        with open("{}.csv".format(formatted_start_time), 'a') as logfile:
            mywriter = csv.writer(logfile)
            mywriter.writerow(line)
        # Baseline info
        baseline_line = [str(current_time), sgp30.baseline_eCO2, sgp30.baseline_TVOC]
        with open("{}_baseline.csv".format(formatted_start_time),'a') as baseline_log:
            mywriter = csv.writer(baseline_log)
            mywriter.writerow(baseline_line)
    
        humidity_counter += seconds_between_reads
        time.sleep(seconds_between_reads)

    print("{} hours of logging complete".format(args.num_hours))

except KeyboardInterrupt as key_int:
     print("logging terminated")
     exit(0)
except:
    print("Unknown error")
    exit(1)
