#!/bin/python

import subprocess

HEADER = "VOL: "
TEXT = 0

def GetFromShell(processStr):
    out = subprocess.check_output(
        processStr, shell=True, universal_newlines=True).strip()
    return out


def Update():
    global TEXT
    amixerData = GetFromShell("amixer sget Master")
    TEXT = GetFromShell(
        "echo '" + amixerData + "' | grep -m 1 -oP '(?<= \[).*?(?=%\] )'")
    STATUS = GetFromShell("echo '" + amixerData +
                          "' | grep -m 1 -oP '(?<=%\] \[).*?(?=\])'")
    
    # Awesome icons. Doesn't work...
    '''
	if TEXT == 0:
		STATUS =   # level 0 (muted icon)
    elif STATUS == "off":
		STATUS =  # muted (muted icon)
    elif TEXT < 25:
		STATUS =  # 24 and less (low volume icon)
    elif TEXT < 50:
		STATUS =  # 49 and less (medium icon)
    elif TEXT < 75:
		STATUS =  # 74 and less (high volume icon)
    else: STATUS =  # full throttle (high volume icon)
	'''
    return TEXT


def Dzen():
    return HEADER + TEXT

#-------------------------------------------------------------
# Volume change functions. Not used in this project.:

def IncreaseVolume(step):
    GetFromShell("amixer -q sset Master " + step + "%+ unmute")
    Update()

def DecreaseVolume(step):
    GetFromShell("amixer -q sset Master " + step + "%- unmute")
    Update()

def MuteVolume():
    GetFromShell("amixer -q sset Master toggle")

def SetVolume(newVolume):
    GetFromShell("amixer -q sset Master " + newVolume + "$1% unmute")
    Update()

