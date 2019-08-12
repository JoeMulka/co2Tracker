""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import time
import board
import busio
import adafruit_sgp30

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

#print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

elapsed_sec = 0

def formatLine(co2_value, tvoc_value):
    return ("{},{}\n".format(co2_value,tvoc_value))


while True:
    # print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
    line = formatLine(sgp30.eCO2, sgp30.TVOC)
    with open("log_co2.csv", 'a') as logfile:
        logfile.write(line)
    time.sleep(5)
    #elapsed_sec += 1
    #if False and elapsed_sec > 10:
    #    elapsed_sec = 0
    #    print("**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
    #          % (sgp30.baseline_eCO2, sgp30.baseline_TVOC))
