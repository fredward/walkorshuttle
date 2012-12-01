# Create your views here.
# Bing Maps Key: Am8_5ptSSXJmpyJ1b6hf_U5Uvc7rqMOsY2vkRuDdne5TG-R2VA3hCoNb7gI4RWU5
from django.http import HttpResponse
from django.shortcuts import render
from wosapp.packages.distance_time import haversine, calculate_min_until
from wosapp.models import Vehicle, Route, Stop, Arrival_Estimate
from django.core import serializers
from urllib import urlopen, urlencode
import json

def index(request):


#	some code to display the running routes and the stops in current order, this needs to be displayed in a better fashion
	ordered_stops = dict()
	for r in Route.objects.all():
		ordered_stops[r.longname] = list()
		for o in json.loads(r.order):
			ordered_stops[r.longname].append(Stop.objects.get(stop=o).name)
	print ordered_stops
	return render(request, 'wosapp/index.html', {'ordered_stops': ordered_stops})

def process_location(request):
	# request comes in as a query dict where lat has the key 'coords[latitiude] and lon 'coords[longitude]'
	if( request.method == "POST" ):
		lat = request.POST.get('coords[latitude]')
		lon = request.POST.get('coords[longitude]')

    # get the closest shuttle stop
	stops  = Stop.objects.all()
	min_dist = 0.0
	print( str(lat) + ',' + str(lon))
	if( len(stops) > 0 ):
		min_dist = haversine(float(lat), float(lon), stops[0].location_lat, stops[0].location_lon)
		min_stop = stops[0]
		for stop in stops:
			dist = haversine(float(lat), float(lon), stop.location_lat, stop.location_lon)
			if(dist < min_dist):
				min_dist = dist
				min_stop = stop
	
	closest_stop =  min_stop
	
	#get data from db about closest stop
	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name) 
	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	arrival_estimates_at_stop = Arrival_Estimate.objects.filter(stop=min_stop).order_by('time')
	
	#get the next X shuttles in the arrival estimates for each vehicles
	#these will be displayed with each shuttle that is arriving at the users closest stop
	next_shuttles_per_route = {}
	# for each arrival estimate
	for close_ae in arrival_estimates_at_stop:
		#get the next 3 arrival estimates for the given ae
		ae_set = close_ae.arrivals_after(3)
		for ae in ae_set:
			next_shuttles_per_route.setdefault(close_ae.id, []).append([ae.route.longname, ae.stop.name, calculate_min_until(ae.time)])

			
				
	next_shuttles = list()
	for ae in arrival_estimates_at_stop:
		next_shuttles.append([ae.route.longname, calculate_min_until(ae.time), ae.id])
       	
	return HttpResponse(json.dumps({'closest' : closest_stop.name, "next_shuttles" : next_shuttles, 'next_shuttles_route' : next_shuttles_per_route}))

#return possible destinations to show on the main page
def get_destinations(request):
	destinations = list()
	for s in Stop.objects.all():
		dest = dict()
		dest['name'] = s.name
		dest['id'] = s.stop
		destinations.append(dest)
	return HttpResponse(json.dumps(destinations))
		


# the method that takes a location for start and destination and gives you the fastest route
#def calculate_route(request):
#	data = request.POST
#	current_location = #
#	destination_stop = #get data from post
#	#http://dev.virtualearth.net/REST/v1/Walking?
#	#get walking distances to all stops
#	stop_walking_times = dict()
#	for stop in Stop.objects.all():
#		params = urlencode({'wp.0': str(current_location['lat']) + str(current_location['lon']), 'wp.1': str(stop.location_lat) + "," + str(stop.location_lon), 'key' : 'Am8_5ptSSXJmpyJ1b6hf_U5Uvc7rqMOsY2vkRuDdne5TG-R2VA3hCoNb7gI4RWU5') 
#		data_return = urlopen("http://dev.virtualearth.net/REST/v1/Walking?%s" % params)
#		route_data = json.load(data_return)
#		travel_duration = route_data['resourceSets']['resources']['travelDuration']
#		stop_walking_times[stop] = travel_duration
