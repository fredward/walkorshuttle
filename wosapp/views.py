# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from wosapp.packages.distance import haversine
from wosapp.models import Vehicle, Route, Stop, Arrival_Estimate
from django.core import serializers
import json
import datetime

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
		#get the arrival estimates for that route
		arrival_est_route = Arrival_Estimate.objects.filter(route=close_ae.route).order_by('time')
		mark = False
		count = 0
		#for each of these estimates
		for ae in arrival_est_route:
			# if we are 'past' our stop and the vehicles match and the count is under 3
			if(mark == True and count < 3 and ae.vehicle.vid == close_ae.vehicle.vid): # a sort of "flag" for the iteration, I hope its the least computationally expensive
				next_shuttles_per_route.setdefault(close_ae.id, []).append([ae.route.longname, ae.stop.name, calculate_min_until(ae.time)])
				print(ae.route.longname + ", " + ae.stop.name + "," + str(ae.vehicle.vid)+","+ str(close_ae.id))
				count+=1
			if(ae == close_ae):
				mark = True
			
				
	next_shuttles = list()
	for ae in arrival_estimates_at_stop:
		next_shuttles.append([ae.route.longname, calculate_min_until(ae.time), ae.id])
       	#context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop, 'next_shuttles' : arrival_estimates_at_stop}
	print(next_shuttles_per_route)
	return HttpResponse(json.dumps({'closest' : closest_stop.name, "next_shuttles" : next_shuttles, 'next_shuttles_route' : next_shuttles_per_route}))

# calculates time difference between the current time and the supplied one to the nearest 1/10th of a min
def calculate_min_until(atime):
	atime = atime.replace(tzinfo=None)
	timedifference = atime - datetime.datetime.utcnow()
	return round(timedifference.total_seconds()/60 , 1)
	