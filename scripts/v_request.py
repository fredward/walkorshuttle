# request the vehicles from transloc and pass it off to a script for loading into the db
from subprocess import call
import urllib, json, cPickle
import os
from time import sleep
dir = os.path.dirname(__file__)
manager_path = os.path.join(dir, '../manage.py')

try:
	params = urllib.urlencode({"agencies" : 52})
	f = urllib.urlopen("http://api.transloc.com/1.1/vehicles.json?%s" % params)
	#print json.load(f)['data'][params['agencies']]
	#stuff = json.load(f)
	stuff = f.read()
	call(['python',manager_path,'add_vehicle',stuff])
	print("Success!")
except:
	print "failure"