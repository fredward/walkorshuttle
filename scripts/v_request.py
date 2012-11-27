from subprocess import call
import urllib, json, cPickle


params = urllib.urlencode({"agencies" : 52})
f = urllib.urlopen("http://api.transloc.com/1.1/vehicles.json?%s" % params)
#print json.load(f)['data'][params['agencies']]
call(['python','/Users/carlcward/Documents/cs50/walkorshuttle/manage.py','add_vehicle',cPickle.dumps(json.load(f))])
