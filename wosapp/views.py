# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from wosapp.packages.distance import haversine
from wosapp.models import Vehicle, Route, Stop, Arrival_Estimate
from django.core import serializers
import json

def index(request):

#	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name) 
#	print possible_routes.values('id')
#	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	#routes_in_service =  Route.objects.filter(id__in=vehicles_running_to_stop.values['route'])
	# get the next shuttles at the closest stop, ordered by time
#	arrival_estimates_at_stop = []
#	context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop, 'next_shuttles' : arrival_estimates_at_stop}
	return render(request, 'wosapp/index.html', {'routes_in_service' : Route.objects.all()})

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
       	#context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop, 'next_shuttles' : arrival_estimates_at_stop}
	print possible_routes
	return HttpResponse(json.dumps({'closest' : closest_stop.name, "next_shuttles" : serializers.serialize('json', arrival_estimates_at_stop)}))