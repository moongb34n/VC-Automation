#!/usr/bin/python
#
# Automation script for executing commands on Cisco VC equipment
#
# Written by: joreyes@linkedin.com
# v1.0 2016-04
# 
# Variables:
#  *hostsFile	- 1sr argument, containing list of hosts to access in IP format
#  *cmdFile		- 2nd argument, containing list of commands with trailing \n
#  *passwd		- admin password
#  *child		- variable where pexpect process is stored and manipulated
#  *hfile		- file handler for hostsFile
#  *hrow		- list of elements in each row of hostsFile
#  *cfile		- file handler for cmdFile
#  *crow		- list of elements in each row of cmdFile
#  *sshNewKey	- expected string if a host key isn't in .ssh/known_hosts yet
#  *sshError	- expected string for ssh errors, regardless of what they are
#  *sval		- captures possible results of accessing each hosts
#  *sval2		- captures possible returned results of openSSH() in main()
#  *cval		- captures possible command results

import csv
import pexpect
import sys

# Functions
def main(hostsFile,cmdFile,passwd):
	print "Host file: %s" % hostsFile 
	print "Command list: %s" % cmdFile
	with open (hostsFile, 'rb') as hfile:
		for hrow in csv.reader(hfile):
			print "Trying: %s" % hrow[0]
			print "######################"
			sshOpen(passwd,hrow)
			
			'''
			Checks result of returned value of sshOpen
			pexpect.EOF = error conditions
			'''
			sval2 = child.expect ([pexpect.TIMEOUT, pexpect.EOF, 'r Login successful', 'Password: '], timeout = 3)
			if sval2 <= 1:
				'''
				Print blank line and move on to the next host
				if error conditions exist
				'''
				print ""
			elif sval2 == 3:
				print ""
				print "Invalid or no password set"
				child.sendline ('')
				
				'''
				Since correct admin password is hardcoded, 
				I don't need to catch another instance of Password: 
				'''
				cmdExec(cmdFile,child)  
				sshClose(child,hrow)	
			else:
				cmdExec(cmdFile,child)
				sshClose(child,hrow)		
			#debug: print sval2
	hfile.closed
	
def cmdExec(cmdFile,child):
	with open (cmdFile, 'r') as cfile:
		for crow in cfile:
			commandLine = crow.splitlines()
			
			'''
			Captures 'OK' after successful login before executing first command.
			Also captures results of each commands
			'''
			cval = child.expect (['ERROR', 'OK'])
			if cval <= 1:
				command = ', '.join(commandLine)
				child.sendline (command)
	cfile.closed

def sshOpen(passwd,hrow):
	global child
	sshNewKey = "Are you sure you want to continue connecting"
	sshError = "ssh:"
	
	child = pexpect.spawn ('ssh -l admin ' + hrow[0])
	child.logfile_read = sys.stdout
	
	'''
	Evaluate SSH attempt for timeouts, errors, new keys and password prompt
	'''
	sval = child.expect ([pexpect.TIMEOUT, sshNewKey, sshError, 'Password: '], timeout = 3)
	if sval == 0:
		print "SSH Timeout"
	elif sval == 1:
		print "Adding new key to .ssh/known_hosts"
		child.sendline ('Yes')
		child.expect ('Password: ')
		child.sendline (passwd)
		return child
	elif sval == 2:
		print ""
		#print "SSH Error: Unreachable or Invalid host"
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
	print "Warning: This script was written exclusively for use with Cisco VC equipment,"
	print "         use extreme caution when using on other platforms"
	print ""
	
# Start
if len(sys.argv) != 3:
	sys.exit(usage())
else:
	warning()
	hostsFile = sys.argv[1]
	cmdFile = sys.argv[2]
	passwd = "****"
	main(hostsFile,cmdFile,passwd)
	
