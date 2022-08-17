
# EVAL-ADF41020 control program

This is very simple program to control ADF41020 eval board from linux (or windows if you wish)

It can work in 2 modes: set freq, sweep.


For freq you run:

main.py --freq xxy

For sweep:

main --start start_mhz --stop stop_mhz --step MHZ_step --dwell in_ms

start_mhz - start frequency


It is also very simple example on how to load FX2 code from python.

PLL setting code is from decompiler ADI sw.

Have fun.
