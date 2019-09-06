import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

formatted_time = [mdates.epoch2num(timepoint) for timepoint in time]

myfig = plt.figure()
ax = myfig.add_subplot(1,1,1)
ax.plot_date(formatted_time, co2, xdate=True, label = "co2")
ax.plot_date(formatted_time, tvoc, xdate=True, label = "tvoc")

plt.legend()
plt.xlabel("time")
plt.ylabel("ppm")
date_format = mdates.DateFormatter('%I:%M%p')
ax.xaxis.set_major_formatter(date_format)

plt.show()
