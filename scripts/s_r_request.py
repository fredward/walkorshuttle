from subprocess import call
import urllib, json, cPickle
import os, pprint
from datetime import datetime
dir = os.path.dirname(__file__)
manager_path = os.path.join(dir, '../manage.py')

dataDict = dict()
params = urllib.urlencode({"agencies" : 52})
f = urllib.urlopen("http://api.transloc.com/1.1/stops.json?%s" % params)
#print json.load(f)['data']#[params['agencies']]

dataDict['stops'] = json.load(f)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(dataDict)

f = urllib.urlopen("http://api.transloc.com/1.1/routes.json?%s" % params)

dataDict['routes'] = json.load(f)
#It got good data from transloc then call it
if 'data' in dataDict['routes']:
	call(['/usr/bin/python',manager_path,'add_stops_routes',cPickle.dumps(dataDict)])

print "Stops and Routes Loaded at: %s" % (datetime.now())