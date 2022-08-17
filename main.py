import time
import argparse
import sys

from adf41020 import ADF41020
from fx import Fx2, FakeFx

parser = argparse.ArgumentParser(description='Make some ramp')
parser.add_argument('--freq', type=int, default=0,   help="Just set freq (MHz)")
parser.add_argument('--start', type=int, default=11500,   help="Start Freq (MHz)")
parser.add_argument('--stop', type=int, default=11700,   help="Stop Freq (MHz)")
parser.add_argument('--step', type=int, default=10,   help="Step Freq (MHz)")
parser.add_argument('--dwell', type=int, default=10,   help="Dwell time in (ms)")

args = parser.parse_args()

fx = Fx2()
#fx = FakeFx()
adf = ADF41020(fx)

if not args.freq == 0:
    print("setting freq to", args.freq)
    adf.set_freq(args.freq)
    sys.exit(0)

print("Start", args.start, "stop", args.stop, "dwell", args.dwell)
print("total time:", (args.stop - args.start)/args.step * args.dwell)


freq = args.start

try:
    while True:

        # set freq
        print("Setting freq", freq, "\r", end='')
        adf.set_freq(freq)

        time.sleep(args.dwell/1000)

        freq += args.step
        if freq > args.stop:
            freq = args.start
except:
    print("end")


