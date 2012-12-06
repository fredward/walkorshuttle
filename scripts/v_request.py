from subprocess import call
import urllib, json, cPickle
import os
from time import sleep
dir = os.path.dirname(__file__)
manager_path = os.path.join(dir, '../manage.py')

for i in range(60):
	try:
		params = urllib.urlencode({"agencies" : 52})
		f = urllib.urlopen("http://api.transloc.com/1.1/vehicles.json?%s" % params)
		#print json.load(f)['data'][params['agencies']]
		call(['python',manager_path,'add_vehicle',cPickle.dumps(json.load(f))])
		print("Success!\t%s" % i)
		sleep(1)
	except:
		continue