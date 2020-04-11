#!/bin/python

#import os
import sys
import subprocess
import time  # for sleep()
import widgets.date
import widgets.volume
import widgets.memory
import widgets.battery
import widgets.wifi

# FONT="bitstream-terminal-bold-r-normal--5-14-10-10-c-11-iso8859-1"
FONT = "-*-fixed-medium-*-*-*-12-*-*-*-*-*-*-*"
BAR_WIDTH = '1920'
BAR_HEIGHT = '16'

# Define colors and spacers etc..:
TX1 = '#DBDADA'     # medium grey text
TX2 = '#F9F9F9'     # light grey text
GRY = '#909090'     # dark grey text
BAR = '#A6F09D'     # green background of bar-graphs
GRN = '#65A765'     # light green (normal)
YEL = '#FFFFBF'     # light yellow (caution)
RED = '#FF0000'     # light red/pink (warning)
WHT = '#FFFFFF'     # white
BLK = '#000000'     # black
SEP = "^p(8;)^fg(" + GRN + ")^r(2x" + BAR_HEIGHT + ")^p(8;)^fg(" + \
    WHT + ")"  # item separator block/line
SLEEP = 1           # update interval (whole seconds, no decimals!)
CHAR = 20      # pixel width of characters of font used

# ------------------------------------------------------------------------------------

def KillProcess(processName, leaveNumInstancesAlive = 1):
    "Kill currently running processes with the given name, and leave alive just the given amount of instances."
    output = GetFromShell(
        "pgrep " + processName + " | awk '{print $1}'")

    instances = output.split()

    for i in range(len(instances) - leaveNumInstancesAlive):
        subprocess.call("kill -9 " + instances[i], shell=True)
    return

def GetFromShell(processStr):
    """Helper function to run Linux shell commands"""
    out = subprocess.check_output(
        processStr, shell=True, universal_newlines=True).strip()
    return out

def AtCenter(word, desiredLen):
    #>>> width = 20
    #>>> print 'HackerRank'.center(width,'-')
    #>>> -----HackerRank-----
    return word.center(desiredLen, ' ')

# -------------------------------------------------------------------------------

# Kill all additional dzen2 instances currently running:
#KillProcess("dzen2", 1)

def Loop():
    while True:

        widgets.date.Update()
        widgets.volume.Update()
        widgets.memory.Update()
        widgets.battery.Update()
        widgets.wifi.Update()

        HEADER = "^fn(" + FONT + ")" + "^ib(1)^pa(0;0)^fg(" + BAR + ")^ro(" + \
            BAR_WIDTH + "x" + BAR_HEIGHT + ")^pa(0;0)"
        
        # Separator is added with every widget:
        OUTPUT = SEP + widgets.date.Dzen()
        OUTPUT += SEP + widgets.memory.Dzen()
        OUTPUT += SEP + widgets.volume.Dzen()
        OUTPUT += SEP + widgets.battery.Dzen()
        OUTPUT += SEP + widgets.wifi.Dzen()
        OUTPUT += SEP

        OUTPUT = HEADER + OUTPUT

        # Send the generated dzen2 abra-cadabra to standard output
        # The 'dzen2-startup.sh' script reads from it and sends it to dzen2 instance.
        sys.stdout.write(OUTPUT + "\n")
        sys.stdout.flush()

        time.sleep(SLEEP)

Loop()
