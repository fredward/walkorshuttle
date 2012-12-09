from django.core.management.base import BaseCommand, CommandError
from wosapp.models import Stop, Walking_Time
from urllib import urlopen, urlencode
from json import load
class Command(BaseCommand):
	def handle(self, *args, **options):
		Walking_Time.objects.all().delete()
		for i in range(len(Stop.objects.all())):
			for j in range(len(Stop.objects.all())):
				start_stop = Stop.objects.all()[i]
				end_stop = Stop.objects.all()[j]
				params = urlencode({'wp.0': str(start_stop.location_lat) + ','+ str(start_stop.location_lon), 'wp.1': str(end_stop.location_lat) + "," + str(end_stop.location_lon), 'key' : 'Am8_5ptSSXJmpyJ1b6hf_U5Uvc7rqMOsY2vkRuDdne5TG-R2VA3hCoNb7gI4RWU5'}) 
				data_return = urlopen("http://dev.virtualearth.net/REST/v1/Routes/Walking?%s" % params)
				route_data = load(data_return)
				travel_duration = route_data['resourceSets'][0]['resources'][0]['travelDuration']
				wt = Walking_Time(start_stop = start_stop.stop, end_stop = end_stop.stop, walking_time = travel_duration)
				wt.save()
				print str(wt) + "\t" + str(travel_duration)
				
