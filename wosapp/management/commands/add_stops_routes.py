

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wosapp.models import Stop, Route, Vehicle, Arrival_Estimate
import json
import pprint
from cPickle import loads

class Command(BaseCommand):
    def handle(self, *args, **options):
        #clear the old stops out
        transaction.enter_transaction_management()
        transaction.managed(True)
        Stop.objects.all().delete()
        #unpickle the data and get the stops request
        raw_data = loads(args[0])
        data = raw_data['stops']
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
                    #print(r.longname + " " + stop.name)
                    order.append(stopid)
                    r.stops.add(stop)
                except django.core.exceptions.ObjectDoesNotExist:
                    print("Exception")
           
            r.order = json.dumps(order)
            r.save()
        # update vehicles as well
        Vehicle.objects.all().delete()
       	data = raw_data['vehicles']
        for veh in data['data']['52']:
            vdata = dict()
            vdata['vid'] = veh['vehicle_id']
            vdata['status'] = veh['tracking_status']
            if veh['heading'] > -1:
              vdata['heading'] = veh['heading']
            vdata['location_lat'] = veh['location']['lat']
            vdata['location_lon'] = veh['location']['lng']
            if(len(Route.objects.filter(rid=veh['route_id'])) > 0):
                vdata['route'] = Route.objects.filter(rid=veh['route_id'])[0]
            else:
                vdata['route'] = None
            vdata['speed'] = veh['speed']
            vdata['updated'] = veh['last_updated_on']
            v = Vehicle(**vdata)
            v.save()

            #add the arrival estimates into the table
            #if(len(veh['arrival_estimates']) > 0):
            #    Arrival_Estimate.objects.filter(vehicle=v).delete()
            for ae in veh['arrival_estimates']:
                aeData = dict()
                if(len(Stop.objects.filter(stop=ae['stop_id'])) > 0):
                    aeData['stop'] = Stop.objects.filter(stop=ae['stop_id'])[0]
                else:
                    aeData['stop'] = None
                if(len(Route.objects.filter(rid=ae['route_id'])) > 0):
                    aeData['route'] = Route.objects.filter(rid=ae['route_id'])[0]
                else:
                    aeData['route'] = None
                aeData['time'] = ae['arrival_at']
                #print vehs[-1]
                aeData['vehicle'] = v
                newAE = Arrival_Estimate(**aeData)
                newAE.save()
        
        transaction.commit()
        transaction.leave_transaction_management()


