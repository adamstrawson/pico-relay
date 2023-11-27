# pico-relay

A basic script written in [MicroPython](https://micropython.org/), for a Raspberry Pico W and a single channel relay. 

This script will:
- Create a soft access point, for being able to connect to the Pico and toggle the relay manually
- Run a cron like schedule to automaticly trigger the relay at the defined times.

This was written to control the operation of a Christmas Tree within a field, that has no power or network connectivity, without any manual intervention. 
