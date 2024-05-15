#!/usr/bin/python3



'''
	variables, in climate:
		[ ] address
		[ ] headless
'''

'''
	itinerary:
		[ ] python3 status.proc.py --headless --front "https://127.0.0.1" --back "https://127.0.0.1"
'''

'''
	requires:
		volts
		click
		selenium
'''

def add_to_system_paths (trails):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	for trail in trails:
		sys.path.insert (0, normpath (join (this_directory, trail)))

add_to_system_paths ([ 
	'structures',
	'structures_pip'
])


import sys
import pathlib
from os.path import dirname, join, normpath
this_directory = pathlib.Path (__file__).parent.resolve ()
guarantees = normpath (join (this_directory, "checks"))
DB_directory = normpath (join (this_directory, "DB"))


if (len (sys.argv) >= 2):
	glob_string = guarantees + '/' + sys.argv [1]
else:
	glob_string = guarantees + '/**/status_*.py'

print ("glob_string:", glob_string)

import biotech
scan = biotech.start (
	# required
	glob_string = glob_string,
	simultaneous = True,
	
	# optional
	module_paths = [	
		normpath (join (this_directory, "structures"))
	],
	
	# optional
	relative_path = this_directory,
	
	records = 1,
	
	db_directory = DB_directory
)

