#!/usr/bin/python
#
# Automation script for executing commands on Cisco VC equipment
#
# Written by: joreyes@linkedin.com
# v1.0 2016-08
# 
# 8/25/2016 - latest version
#

import csv
import pexpect
import sys

# Functions
def main(hostsFile,cmdFile,passwd):
        print "Host file: %s" % hostsFile 
        print "Command list: %s" % cmdFile
        with open (hostsFile, 'rb') as hfile:
                for hrow in csv.reader(hfile):
                        if not hrow:
                                print "empty row"
                        else:
                                print "Trying: %s" % hrow[0] + " " + hrow[1]
                                print "######################"
                                sshOpen(passwd,hrow)
                                '''
                                Checks result of returned value of sshOpen
                                pexpect.EOF = error conditions
                                '''
                                sval2 = child.expect ([pexpect.TIMEOUT, pexpect.EOF, 'r Login successful', 'Password: '], timeout = 6)
                                if sval2 <= 1:
                                        '''
                                        Print blank line and move on to the next host
                                        if error conditions exist
                                        '''
                                        print ""
                                elif sval2 == 3:
                                        print ""
                                        print "Invalid or no password set, using blank password"
                                        child.sendline ('')
                                        '''
                                        Since correct admin password is hardcoded, 
                                        I don't need to catch another instance of 'Password:'
                                        '''
                                        print child.before
                                        cmdLog(child,hrow)
                                        cmdExec(cmdFile,child)  
                                        sshClose(child,hrow)
                                        outfile.closed
                                else:
                                        print child.before
                                        cmdLog(child,hrow)
                                        cmdExec(cmdFile,child)
                                        sshClose(child,hrow)
                                        outfile.closed
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
                                if not command.startswith('#'):
                                        child.sendline (command)
        cfile.closed

def cmdLog(child,hrow):
        global outfile

        print "Creating command log for %s " % hrow[1]
        print ""

        '''
        if hrow[1] is empty, then log file will default to "_log.txt"
        '''
        outfile = open (hrow[1] + '_log.txt', 'wb')
        child.logfile_read = outfile
        child.logfile_send = sys.stdout
        return outfile

def sshOpen(passwd,hrow):
        global child

        sshNewKey = "Are you sure you want to continue connecting"
        sshError = "ssh:"

        child = pexpect.spawn ('ssh -l admin ' + hrow[0])

        #debug: child.logfile_read = sys.stdout
        '''
        Evaluate SSH attempt for timeouts, errors, new keys and password prompt
        '''
        sval = child.expect ([pexpect.TIMEOUT, sshNewKey, sshError, 'Password: '], timeout = 6)
        if sval == 0:
                print "SSH Timeout"
        elif sval == 1:
                print "Adding new key to .ssh/known_hosts"
                child.sendline ('Yes')
                child.expect ('Password: ')
                child.sendline (passwd)
                return child
        elif sval == 2:
                child.expect (pexpect.EOF)
                print child.before
        elif sval == 3:
                child.sendline (passwd)
                return child

def sshClose(child,hrow):
        child.sendline ('bye')
        child.expect ('Connection to ' + hrow[0] + ' closed.')
        print child.after

def usage():
        print "Usage: ./vccmd.py [host-file] [cmd-file]"
        print "   * [host-file] - list of hosts to access in IP format"
        print "   * [cmd-file] - list of commands to execute"
        print "Logging generated as: '[name]_log.txt'"
        print ""

def message():
        print "Warning: This script was written exclusively for use with Cisco VC equipment,"
        print "         use extreme caution when using on other platforms."
        print ""

# Start
if len(sys.argv) != 3:
        sys.exit(usage())
else:
        message()
        hostsFile = sys.argv[1]
        cmdFile = sys.argv[2]
        passwd = "7412"
        main(hostsFile,cmdFile,passwd)
