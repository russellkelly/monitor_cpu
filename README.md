# monitor_cpu
Script that displays CPU of one or more Arista Devices


# monitor_interface
Monitor Interfaces Command for Arista Devices

This script continually monitors the CPU on one, or more Arista devices.

I created this program to allow one or a number of switches' CPU to be monitored at once, running on-box or off.

See the help below:

```
Usage: monitor_cpu.py [options]

Options:
  -h, --help       show this help message and exit
  -u USERNAME      Username. Mandatory option
  -p PASSWORD      Password. Mandatory option
  -r REFRESH_RATE  explicit refresh rate running the command. By default the
                   programs sets the system default refresh to 2 seconds,
  -a HOSTNAMES     One or more hostnames (or IP addresses) of the switches to
                   poll.  Comma separated.  Mandatory option with multiple
                   arguments




```

As an example if I want to monitor devices lf275,fm213,fm382 I would run the following:

```
python monitor_interfaces.py -u admin -p admin -r 10 -a lf275,fm213,fm382 -r 1
```


