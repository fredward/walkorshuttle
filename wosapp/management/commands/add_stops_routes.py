

from django.core.management.base import BaseCommand, CommandError
from wosapp.models import Stop, Route
import json
import pprint
from cPickle import loads
class Command(BaseCommand):
    def handle(self, *args, **options):
        #clear the old stops out
        Stop.objects.all().delete()
        #unpickle the data and get the stops request
        raw_data = loads(args[0])
        data = raw_data['stops']
        #conveinence printer
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(data['data'])
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


        data = raw_data['routes']
        Route.objects.all().delete()
        #have to filter by agency here to
        for route in data['data']['52']:
            rdata = dict()
            rdata['rid'] = route['route_id']
            rdata['longname'] = route['long_name']
            rdata['shortname'] = route['short_name']
            rdata['type'] = route['type']
            rdata['color'] = route['color']
            rdata['desc'] = route['description']
            rdata['segments'] = json.dumps(route['segments'])
            r = Route(**rdata)
            r.save()
            order = []
            # go through each stop ID in the data and add the corresponding stop to the route stop field
            for stopid in route['stops']:
                try:
                    stop = Stop.objects.get(stop=stopid)
                    print(r.longname + " " + stop.name)
                    order.append(stopid)
                    r.stops.add(stop)
                except django.core.exceptions.ObjectDoesNotExist:
                    print("Exception")
               # print(str(stop.stop) + " on route " + r.longname)
            
            r.order = json.dumps(order)
            r.save()
