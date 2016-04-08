#!/usr/bin/python
#
# Automation script for executing commands on VC equipment
#
# Written by: joreyes@linkedin.com
# v1.0 2016-04
# 

import csv
import pexpect
import sys

# Functions
def main(hostsFile,cmdFile,passwd):
	print "Host file is: %s" % hostsFile 
	print "Command list is: %s" % cmdFile
	with open (hostsFile, 'rb') as hfile:
		for hrow in csv.reader(hfile):
			print "Trying: %s" % hrow[0]
			print "######################"
			sshOpen(passwd,hrow)
			
			# Checks result of sshOpen
			# pexpect.EOF = error conditions
			sval2 = child.expect ([pexpect.TIMEOUT, pexpect.EOF, 'r Login successful'], timeout = 3)
			if sval2 <= 1:
				print ""
			else:
				cmdExec(cmdFile,child)
				sshClose(child,hrow)		
			# print sval2
	hfile.closed
	
def cmdExec(cmdFile,child):
	with open (cmdFile, 'r') as cfile:
		for crow in cfile:
			commandLine = crow.splitlines()
			
			# Captures OK after successful login before executing first command
			# Also captures successive OK after each commands
			child.expect ('OK')
			command = ', '.join(commandLine)
			child.sendline (command)
	cfile.closed

def sshOpen(passwd,hrow):
	global child
	sshNewKey = "Are you sure you want to continue connecting"
	sshError = "ssh:"
	
	child = pexpect.spawn ('ssh -l admin ' + hrow[0])
	child.logfile_read = sys.stdout
	
	# Evaluate SSH attempt
	sval = child.expect ([pexpect.TIMEOUT, sshNewKey, sshError, 'Password: '], timeout = 5)
	if sval == 0:
		print "SSH Timeout"
	elif sval == 1:
		print "Adding new key to .ssh/known_hosts"
		child.sendline ('Yes')
		child.expect ('Password: ')
		child.sendline (passwd)
		return child
	elif sval == 2:
		print "SSH Error: Unreachable or Invalid host"
	elif sval == 3:
		child.sendline (passwd)
		return child
	
def sshClose(child,hrow):
	child.sendline ('bye')
	child.expect ('Connection to ' + hrow[0] + ' closed.')

def usage():
	print "Usage: ./vccmd.py [host-file] [cmd-file]"
	print "	  * [host-file] - list of hosts to access, must be IP format"
	print "	  * [cmd-file] - list of commands to execute"
	print ""

def warning():
	print "Warning: This script was written exclusively for Cisco VC equipment, use caution when using for other purposes"
	print ""
	
# Start
if len(sys.argv) != 3:
	sys.exit(usage())
else:
	warning()
	hostsFile = sys.argv[1]
	cmdFile = sys.argv[2]
	passwd = raw_input ("Admin password: ")
	main(hostsFile,cmdFile,passwd)