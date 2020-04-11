#!/bin/python

import subprocess
import re

TEXT = 0
HEADER = "RAM: "

def GetFromShell(processStr):
	out = subprocess.check_output(
		processStr, shell=True, universal_newlines=True).strip()
	return out


INDICATOR_LENGHT = 50
SCARCE_THRESHOLD = 95
BAR = '#A6F09D'     # green background of bar-graphs
GRN = '#65A765'     # light green (normal)
RED = '#FF0000'     # light red/pink (warning)


def Update():
	global TEXT
	global SCARCE_THRESHOLD
	TEXT = ""
	totalRAM = 0
	freeRAM = 0
	with open("/proc/meminfo") as origin_file:
		for line in origin_file:
			if re.search(r'MemTotal:', line):
				line = re.findall(r'\d+', line)
				if line:
					totalRAM = int(line[0])
			else:
				if re.search(r'MemFree:', line):
					line = re.findall(r'\d+', line)
					if line:
						freeRAM = int(line[0])

	usedRAM = totalRAM - freeRAM
	usedbar = int(usedRAM * INDICATOR_LENGHT / totalRAM)
	freebar = int(freeRAM * INDICATOR_LENGHT / totalRAM)

	if usedbar >= (INDICATOR_LENGHT / 100 * SCARCE_THRESHOLD):
		fgcol = "^fg(" + RED + ")"
	else:
		fgcol = "^fg(" + GRN + ")"
	TEXT = "^fg(white)^p(;4)" + fgcol + "^r(" + str(usedbar) + \
		"x8)^fg(" + BAR + ")^r(" + str(freebar) + "x8)^p(;-4)"


def Dzen():
	return HEADER + TEXT