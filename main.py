#!/usr/bin/python

import shutil
import sys
from lib import DspaceArchive

if len(sys.argv) != 2:
	print("Usage in windows: python main.py .\to_load\file.csv")
	sys.exit()

input_file = sys.argv[1]

archive = DspaceArchive(input_file)

groups = archive.getGroups()
unique_groups = list(set(groups))

for group in unique_groups:
	idxs = [idx for idx, value in enumerate(groups) if value == group]
	items_work = []
	for idx in idxs:
		items_work.append(archive.getItem(idx))
	dirpath = "./output/" + group
	
	archive.write(items=items_work, dir=dirpath)
	shutil.make_archive(dirpath, 'zip', dirpath)
	shutil.rmtree(dirpath)