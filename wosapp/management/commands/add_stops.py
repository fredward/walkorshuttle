# adds vehicles to the Vehicle model that come in a pickled python dict from the unpacked from the transLoc API

from django.core.management.base import BaseCommand, CommandError
from wosapp.models import Stop
from cPickle import loads
import pprint
class Command(BaseCommand):
    def handle(self, *args, **options):
        #clear the old stops out
        Stop.objects.all().delete()
        data = loads(args[0])
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

