from subprocess import call
import urllib, json, cPickle


params = urllib.urlencode({"agencies" : 52})
f = urllib.urlopen("http://api.transloc.com/1.1/stops.json?%s" % params)
#print json.load(f)['data']#[params['agencies']]
call(['python','/Users/carlcward/Documents/cs50/walkorshuttle/manage.py','add_stops',cPickle.dumps(json.load(f))])
