from subprocess import call
import urllib, json, cPickle

dataDict = dict()
params = urllib.urlencode({"agencies" : 52})
f = urllib.urlopen("http://api.transloc.com/1.1/stops.json?%s" % params)
#print json.load(f)['data']#[params['agencies']]

dataDict['stops'] = json.load(f)

f = urllib.urlopen("http://api.transloc.com/1.1/routes.json?%s" % params)

dataDict['routes'] = json.load(f)
call(['python','/Users/carlcward/Documents/cs50/walkorshuttle/manage.py','add_stops_routes',cPickle.dumps(dataDict)])
