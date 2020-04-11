#!/bin/python

import re
import subprocess

TEXT = 0
HEADER = "BAT: "
COLOR = ""
RETURN_TEXT = True

def GetFromShell(processStr):
	out = subprocess.check_output(
		processStr, shell=True, universal_newlines=True).strip()
	return out

def Update():
	# 'acpi -b' returns something like: "Battery 0: Charging, 94%".
	BAT_STATUS = GetFromShell("acpi -b")
	BAT = re.findall(r'\d+', BAT_STATUS)[1]
	STATUS = re.search('%s(.*)%s' % ("Battery "r'\d+'": ", ", "), BAT_STATUS).group(1)
	
	if STATUS == "Unknown":
		# For Unknown status check AC adapter connectivity state.
		# 'acpi -a' returns "Adapter 0: on-line" or "off-line"
		AC = GetFromShell("acpi -a | grep -oP '(?<=: ).*'")
		if AC == "on-line":
			STATUS = "Charging"
		elif AC == "off-line":
			STATUS = "Discharging"

	'''
	if RETURN_TEXT:
		pass
	else:
		if STATUS == "Charging":
			STATUS = 
		elif STATUS == "Discharging":
			if BAT < 50:
				STATUS = 
			elif BAT < 25:
				STATUS = 
			else STATUS = 
	'''

	# Set urgent flag below 5% or use orange below 20%
	global COLOR
	if int(BAT) < 5:
		COLOR = "#FF0000" # red
	elif int(BAT) < 20:
		COLOR = "#FF8000" # orange, I guess
	else:
		COLOR = "#FFFFFF" # white
	
	global TEXT
	TEXT = BAT + "%, " + STATUS

def Dzen():
	return "^fg(" + COLOR + ")" + HEADER + TEXT

def Width(font):
    w = GetFromShell("dzen2-textwidth " + font + " '" + HEADER + TEXT + "'")
    return int(w)