# adds vehicles to the Vehicle model that come in a pickled python dict from the unpacked from the transLoc API

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wosapp.models import Vehicle, Arrival_Estimate, Route, Stop
from json import loads
#import pprint
class Command(BaseCommand):
    def handle(self, *args, **options):
        transaction.enter_transaction_management(True)
        transaction.managed(True)
        data = loads(args[0])
        Vehicle.objects.all().delete()
        
        aes = []
        #conveinence printer
       # pp = pprint.PrettyPrinter(indent=4)
       # pp.pprint(data['data']['52'])
       	
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
                aes.append(newAE)
        Arrival_Estimate.objects.all().delete()
        for ae in aes:
        	ae.save()
    	transaction.commit()        
    	transaction.leave_transaction_management()

        
        	 
            