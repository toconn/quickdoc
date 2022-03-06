#!/usr/bin/env python3

from sys import argv
from sys import exit


HELP = '''Usage: {{name}}
'''


## Utils ###################################################

def argument(n, default = ''):
	if len(argv) > n:
		return argv[n]
	return default

def nl():
	print()

def no_arguments():
	return len(argv) <= 1

def show_help():
	print(HELP)
	print()


## Main ####################################################

nl()

if no_arguments():
	show_help()
	exit()


