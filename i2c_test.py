import time
import board
import busio
import adafruit_sgp30
import csv
import argparse
from atmos import calculate
import adafruit_si7021


def calculateAbsoluteHumidity(rel_humidity, temperature):
    temp_kelvin = temperature + 273.15
    absolute_humidity = calculate('AH', RH=rel_humidity, p=1e5, T=temp_kelvin, debug=True)
    return absolute_humidity

# Humidity and temperature sensor
si_7021_i2c = busio.I2C(board.SCL, board.SDA)
temp_humid_sensor = adafruit_si7021.SI7021(si_7021_i2c)

# 
sgp30_i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(sgp30_i2c)


while True:
    temp = temp_humid_sensor.temperature
    relative_humidity = temp_humid_sensor.relative_humidity
    print("\nTemperature: %0.1f C" % temp)
    print("Humidity: %0.1f %%" % relative_humidity)
    absolute_humidity = calculateAbsoluteHumidity(relative_humidity, temp)[0]
    print("Absolute Humidity: {} kg/m^3".format(absolute_humidity))

    time.sleep(2)
