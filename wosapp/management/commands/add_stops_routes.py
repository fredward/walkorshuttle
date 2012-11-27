

from django.core.management.base import BaseCommand, CommandError
from wosapp.models import Stop
from cPickle import loads
import pprint
class Command(BaseCommand):
    def handle(self, *args, **options):
        #clear the old stops out
        Stop.objects.all().delete()
        #unpickle the data and get the stops request
        data = loads(args[0])['stops']
        #conveinence printer
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data['data'])
        #['data'] is the data array in the json response
        for stop in data['data']:
            sdata = dict()
            sdata['stop'] = stop['stop_id']
            sdata['name'] = stop['name']
            sdata['desc'] = stop['description']
            sdata['code'] = stop['code']
            sdata['location_lat'] = stop['location']['lat']
            sdata['location_lon'] = stop['location']['lng']
            
            
            
            s = Stop(**sdata)
            s.save()

#TODO get routes and create the relations
