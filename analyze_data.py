import matplotlib.pyplot as plt
import matplotlib
import csv
import argparse
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("datafile", help = "the file containing co2 and TVOC")
args = parser.parse_args()

time = []
co2 = []
tvoc = []

with open(args.datafile) as csvfile:
    myreader = csv.reader(csvfile)
    for row in myreader:
        time.append(float(row[0]))
        co2.append(int(row[1]))
        tvoc.append(int(row[2]))

formatted_time = [matplotlib.dates.epoch2num(timepoint) for timepoint in time]

plt.plot_date(formatted_time, co2, label = "co2")
plt.plot_date(formatted_time, tvoc, label = "tvoc")

plt.legend()
plt.xlabel("time")
plt.ylabel("ppm")

plt.show()
