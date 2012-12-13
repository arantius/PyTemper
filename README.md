# Documentation

PyTemper is a simple python class to handle interfacing with USB Temper thermometer devices.  See [my original blog post](http://programming.arantius.com/pytemper-read-usb-temper-in-python) for further details.

It provides the `Temper` class, which takes a port number and temperature offset value.
You can also provide the `mode` parameter; 'f' means Fahrenheit, otherwise means Celsius.
The object this creates exposes a `read()` method which will return the appropriate temperature as a float.

It is currently only tested with Temper "v2" devices.  (v1 will say -20 to +100 C on the device, v2 claims -40 to +120.)

PyTemper depends on [pyserial](http://pyserial.sourceforge.net/) to interface with the device.

# License

PyTemper is Open Source software, released under the MIT license.

# Changelog

 * Version 1.0.3 (Jan 10, 2011)
   * Allow device and offset parameters on the command line.
   * Allow arbitrary device names (not just `ttyUSB` port numbers).
   * Fix bug reading temperatures below 0 Celsius.
 * Version 1.0.2 (Jul 13, 2009)
   * Increased `sleep()` delays resolve timing issues with newer (2.6.29) (and faster?) linux kernel drivers.
 * Version 1.0.1 (Dec 8, 2008)
   * Bugfix release, for very low temperatures.
 * Version 1.0 (Nov 27, 2008)
   * First stable release.
 * Version 0.1 (Nov 24, 2008)
   * Initial release.  Buggy, and immediately removed.
