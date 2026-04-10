import sys
import time
import datetime
import csv

# import CapeMCA package
sys.path.append('/home/pi/cape_mca')
from capemca import CapeMCA


# -----------------------------
# READ INPUT ARGUMENTS
# -----------------------------
runtime = int(sys.argv[1])     # total run time (seconds)
interval = int(sys.argv[2])    # measurement interval (seconds)
filename = sys.argv[3]         # output file name


# -----------------------------
# DATA STORAGE
# -----------------------------
times = []
counts = []


# -----------------------------
# MAIN MEASUREMENT
# -----------------------------
with CapeMCA() as mca:

    print("Connected. Starting measurement...\n")

    # reset spectrum before starting
    mca.zero_spectrum()

    start_time = time.time()
    next_read = start_time

    while (time.time() - start_time) < runtime:

        # wait until next interval
        now = time.time()
        if now < next_read:
            time.sleep(next_read - now)

        read_start = time.time()

        # take measurement
        status = mca.read_status()
        spectrum = mca.read_spectrum()

        # reset for next interval
        mca.zero_spectrum()

        # timestamp
        timestamp = datetime.datetime.now()

        # use total counts in this interval
        total_counts = sum(spectrum[1:])   # ignore channel 0

        # store data
        times.append(timestamp)
        counts.append(total_counts)

        # print to screen
        elapsed = read_start - start_time
        print(f"[{elapsed:.1f}s] Counts: {total_counts}")

        # schedule next read
        next_read = read_start + interval


print("\nMeasurement complete. Saving data...")


# -----------------------------
# SAVE TO CSV
# -----------------------------
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["Time", "Counts"])

    for t, c in zip(times, counts):
        writer.writerow([t, c])


print(f"Data saved to {filename}")
