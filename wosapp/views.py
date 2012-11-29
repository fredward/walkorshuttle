# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from wosapp.packages.distance import haversine
from wosapp.models import Vehicle, Route, Stop, Arrival_Estimate
from django.core import serializers
import json
import datetime

def index(request):

#	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name) 
#	print possible_routes.values('id')
#	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	#routes_in_service =  Route.objects.filter(id__in=vehicles_running_to_stop.values['route'])
	# get the next shuttles at the closest stop, ordered by time
#	arrival_estimates_at_stop = []
#	context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop, 'next_shuttles' : arrival_estimates_at_stop}
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

	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name) 
	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	arrival_estimates_at_stop = Arrival_Estimate.objects.filter(stop=min_stop).order_by('time')
	next_shuttles = list()
	for ae in arrival_estimates_at_stop:
		next_shuttles.append([ae.route.longname, calculate_min_until(ae.time)])
       	#context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop, 'next_shuttles' : arrival_estimates_at_stop}
	return HttpResponse(json.dumps({'closest' : closest_stop.name, "next_shuttles" : next_shuttles}))

def calculate_min_until(atime):
	atime = atime.replace(tzinfo=None)
	timedifference = atime - datetime.datetime.utcnow()
	return round(timedifference.total_seconds()/60 , 1)
	