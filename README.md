# Automation script for executing commands on Cisco VC equipment
```
Written by: joreyes@linkedin.com
 v1.0 2016-04

# Variables:
#  *hostsFile	- 1st argument, containing list of hosts to access in IP format
#  *cmdFile		- 2nd argument, containing list of commands with trailing \n
#  *passwd		- admin password
#  *child		- global variable where pexpect process is stored and manipulated
#  *hfile		- file handler for hostsFile
#  *hrow		- list of elements in each row of hostsFile
#  *cfile		- file handler for cmdFile
#  *crow		- list of elements in each row of cmdFile
#  *sshNewKey	- expected string if a host key isn't in .ssh/known_hosts yet
#  *sshError	- expected string for ssh errors, regardless of what they are
#  *sval		- captures possible results of accessing each hosts
#  *sval2		- captures possible returned results of openSSH() in main()
#  *cval		- captures possible command results
#  *outfile		- global variable for log file handler

Usage: ./vccmd.py [host-file] [cmd-file]
	  * [host-file] - list of hosts to access, must be IP format
	  * [cmd-file] - list of commands to execute
Logging generated as: '[IP]_log.txt'
```
