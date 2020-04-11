#!/bin/python

import subprocess

TEXT = ""

def GetFromShell(processStr):
    out = subprocess.check_output(
        processStr, shell=True, universal_newlines=True).strip()
    return out

def Update():
    global TEXT
    TEXT = GetFromShell("date +'%H:%M:%S %a %x'")

def Dzen():
    return TEXT

def Width(font):
    w = GetFromShell("dzen2-textwidth " + font + " '" + TEXT + "'")
    return int(w)