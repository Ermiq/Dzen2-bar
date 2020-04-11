#!/bin/python

import re
import subprocess

# On some distros you need to change this interface name to "wlan0".
# For example, Devuan uses "wlan0" name for WiFi.
INTERFACE = "wlp2s0"

TEXT = ""
HEADER = "WiFi: "
IS_UP = False
CONNECTED = False
QUALITY = 0
ESSID = ""

def GetFromShell(processStr):
	out = subprocess.check_output(
		processStr, shell=True, universal_newlines=True).strip()
	return out

def Update():
	output = GetFromShell("/sbin/iwconfig " + INTERFACE)
	# Check if WiFi adapter is turned on: "Tx-Power=22 dBm" or "Tx-Power=off"
	POWER_STATE = re.search('%s(.*)%s' % ("Tx-Power=", " "), output).group(1)

	if POWER_STATE != "off":
		IS_UP = True
		# Check connection status:
		if GetFromShell("cat /sys/class/net/" + INTERFACE + "/operstate") != 'down':
			CONNECTED = True

	if IS_UP:
		if CONNECTED:
			# Connected to some SSID:
			global ESSID
			ESSID = re.search('%s(.*)%s' % ('ESSID:"', '"'), output).group(1)
			global QUALITY
			QUALITY = GetQualityLevel()
			output = ESSID + "(" + str(QUALITY) + "%)"
		else:
			# WiFi is on but not connected to any SSID:
			output = "No connection"
	else:
		# Wifi is off:
		output = "Off"
	global TEXT
	TEXT = output

def Dzen():
	# Color depends on connection quality:
	if QUALITY > 80:
		color = "#00FF00"
	elif QUALITY == 0:
		color = "#444444"
	elif QUALITY < 40:
		color = "#FF0000"
	elif QUALITY < 60:
		color = "#FFAE00"
	elif QUALITY < 80:
		color = "#FFF600"

	return "^fg(" + color + ")" + HEADER + TEXT

def Width(font):
	w = GetFromShell("dzen2-textwidth " + font + " '" + HEADER + TEXT + "'")
	return int(w)

def GetQualityLevel():
	'''cat /proc/net/wireless returns this kind of data:

Inter-| sta-|      Quality     |     Discarded packets      | Missed | WE
 face | tus | link level noise | nwid crypt frag retry misc | beacon | 22
wlp2s0: 0000   70.  -39.  -256     0      0      0      0       61      0

To determine connection quality level (0-100%) need to extract the "Qualuty -> link" entry from the table. When this entry = 70. it means the connection quality is 100% stable.
	'''
	with open("/proc/net/wireless") as origin_file:
		# Iterate through lines:
		for line in origin_file:
			# Look for "wlp2s0:" or "wlan0:" in lines:
			if re.search(INTERFACE + ':', line):
				# Found line with values. Split it into a list of entries:
				line = line.split()
				# Get digital value from the 3rd entry (index 2 in list).
				# r'|d+' represents a regular expression for digits:
				line = re.search(r'\d+', line[2]).group(0)
				# 70 in the table means 100%, so gotta change the value to real percentage:
				return int(int(line) * 100 / 70)