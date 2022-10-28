#!/usr/bin/python

import sys
from lib import DspaceArchive

if len(sys.argv) != 2:
	print("Usage: ./main file.csv")
	sys.exit()

input_file = sys.argv[1]

archive = DspaceArchive(input_file)
archive.write("./output")