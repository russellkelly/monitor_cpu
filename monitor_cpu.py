#!/usr/bin/env python


from jsonrpclib import Server
from pprint import pprint as pp
from multiprocessing import Process
from threading import Thread
import json
import os
import re
import signal
import sys
import socket
from time import sleep
import subprocess
import argparse
import pyeapi
import getopt
import optparse
import errno
import collections



def parse_args(argv):
    nodes = []
    hostname_list = []
    switches = []
    switch_dict = {}
    switch_dict = {}
    
    parser = optparse.OptionParser()  
    parser.add_option('-u', help='Username. Mandatory option', dest='username', action='store')
    parser.add_option('-p', help='Password. Mandatory option', dest='password', action='store')
    parser.add_option('-r', help='explicit refresh rate running the command. By default the programs sets the system default refresh to 2 seconds,', dest='refresh_rate', type=int, default=2, action='store')
    parser.add_option('-a', help='One or more hostnames (or IP addresses) of the switches to poll.  Comma separated.  Mandatory option with multiple arguments', dest='hostnames', action='store')
    (opts, args) = parser.parse_args()
    mandatories = ['username', 'password', 'hostnames']
    for m in mandatories:
        if not opts.__dict__[m]:
            print "mandatory option is missing\n"
            parser.print_help()
            print "\n\n"
            exit(-1)
    hostname_list = opts.hostnames.split(',')
    for IPorHM in hostname_list:
        switch = connect (opts.username, opts.password, IPorHM)
        switches.append(switch)
    switch_dict = {k: v for k, v in zip(hostname_list, switches)}
    return opts.refresh_rate,switch_dict, hostname_list


def connect(user, password, address):
   #Connect to Switch via eAPI
    switch = Server("http://"+user+":"+password+"@"+address+"/command-api")
    #capture Connection problem messages:
    try:
        response = switch.runCmds(1, ["show version"])
    except socket.error, error:
        error_code = error[0]
        if error_code == errno.ECONNREFUSED:
            run_error = str("[Error:"+str(error_code)+"] Connection Refused!(eAPI not configured?)")
            print "\n\nswitch: " + str(address)
            print run_error
            print "\n\n"
            sys.exit(2)
        elif error_code == errno.EHOSTUNREACH:
            run_error = str("[Error:"+str(error_code)+"] No Route to Host(Switch powered off?)")
            print "\n\nswitch: " + str(address)
            print run_error
            print "\n\n"
            sys.exit(2)
        elif error_code == errno.ECONNRESET:
            run_error = str("[Error:"+str(error_code)+"] Connection RST by peer (Restart eAPI)")
            print "\n\nswitch: " + str(address)
            print run_error
            sys.exit(2)
            print "\n\n"
        else:
            # Unknown error - report number and error string (should capture all)
            run_error = str("[Error5:"+str(error_code) + "] "+error[1])
            #raise error;
            print "\n\nswitch: " + str(address)
            print run_error
            sys.exit(2)
            print "\n\n"
    else:
        return switch


class cpu_monitor(Process):
	def __init__(self):
		super(cpu_monitor, self).__init__()
	def run(self):
		while True:
			self.refresh_rate,self.switches, self.hostname_list  = parse_args(sys.argv[1:])
			self.print_counter(self.refresh_rate,self.switches, self.hostname_list)
	def print_counter(self, refresh_rate, switches, hostname_list):
		self.oldstdout = sys.stdout
		self.script_dir = os.path.dirname(__file__)
		self.rel_path = "CPUOutput"
		self.abs_file_path = os.path.join(self.script_dir, self.rel_path)
		while True:
			try:
				self.f = open(self.abs_file_path,'w')
				sys.stdout = self.f
				for switch in switches.values():
					output = switch.runCmds ( 1, [ "show processes top once | grep 'Cpu(s)' " ], "text" )
					output = output[0]
					for key, value in switches.items():
						if switch is value:
							print "\n\n================ Switch: " + str(key) +" ===========\n\n"
							for k,v in output.items():
								print k,v
							sleep(self.refresh_rate)
				sys.stdout.close()
				sys.stdout = self.oldstdout
				self.fin = open(self.abs_file_path,'r')
				os.system('clear')
				print self.fin.read()
			except KeyboardInterrupt:
				sys.stdout.close()
				sys.stdout = self.oldstdout
				sys.exit(0)


if __name__ == "__main__":
	refresh_rate, switches, hostname_list  = parse_args(sys.argv[1:])
	print "\n\nStarting....CPU Monitoring.....\n\n"
	cpu_monitor()
	p1 = cpu_monitor()
	p1.start()
	try:
		while True:
		   pass
	except KeyboardInterrupt:
		p1.terminate()
		print "\n\n Exiting the CPU Program........ \n\n"
		sys.exit(0)



