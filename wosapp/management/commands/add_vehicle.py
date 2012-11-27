from django.core.management.base import BaseCommand, CommandError
from wosapp.models import Vehicle, Arrival_Estimate
from cPickle import loads
import pprint
class Command(BaseCommand):
    def handle(self, *args, **options):
        Vehicle.objects.all().delete()
        data = loads(args[0])
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data['data']['52'])
        for veh in data['data']['52']:
            vdata = dict()
            vdata['vid'] = veh['vehicle_id']
            vdata['status'] = veh['tracking_status']
            vdata['heading'] = veh['heading']
            vdata['location_lat'] = veh['location']['lat']
            vdata['location_lon'] = veh['location']['lng']
            vdata['route'] = veh['route_id']
            vdata['speed'] = veh['speed']
            vdata['updated'] = veh['last_updated_on']
            v = Vehicle(**vdata)
            v.save()

            #add the arrival estimates into the table
            if(len(veh['arrival_estimates']) > 0):
                Arrival_Estimate.objects.all().delete()
            for ae in veh['arrival_estimates']:
                newAE = Arrival_Estimate(stop = ae['stop_id'], route = ae['route_id'], time = ae['arrival_at'], vehicle = v)
                newAE.save()
