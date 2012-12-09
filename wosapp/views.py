# Create your views here.
# Bing Maps Key: Am8_5ptSSXJmpyJ1b6hf_U5Uvc7rqMOsY2vkRuDdne5TG-R2VA3hCoNb7gI4RWU5
from django.http import HttpResponse
from operator import itemgetter
from django.shortcuts import render
from wosapp.packages.distance_time import haversine, calculate_min_until, calculate_time_between
from django.contrib.sessions.models import Session
from wosapp.models import Vehicle, Route, Stop, Arrival_Estimate, Walking_Time
from django.core import serializers
from urllib import urlopen, urlencode
from datetime import datetime, timedelta
from django.core.context_processors import csrf
from pytz import UTC
from time import clock
from django.views.decorators.cache import never_cache
import json
import time

def index(request):
	#csrf token
	c = {}
	c.update(csrf(request))
	# this makes our session data immediately available
	request.session.save()
#	some code to display the running routes and the stops in current order, this needs to be displayed in a better fashion
	ordered_stops = dict()
	for r in Route.objects.all():
		ordered_stops[r.longname] = list()
		for o in json.loads(r.order):
			ordered_stops[r.longname].append(Stop.objects.get(stop=o).name)
	c.update({'ordered_stops': ordered_stops})
	#print c
	return render(request, 'wosapp/index.html', c)

def process_location(request):
	#if(Access.objects.get(id)
	# request comes in as a query dict where lat has the key 'coords[latitiude] and lon 'coords[longitude]'
	if( request.method == "POST" ):
		lat = request.POST.get('coords[latitude]')
		lon = request.POST.get('coords[longitude]')
	#calculate_routes({'lat' : lat, 'lon' : lon}, request)
    # get the closest shuttle stop
	stops  = Stop.objects.all()
	min_dist = 0.0
	min_stop = 0
	print( str(lat) + ',' + str(lon))
	if( len(stops) > 0 ):
		min_dist = haversine(float(lat), float(lon), stops[0].location_lat, stops[0].location_lon)
		min_stop = stops[0]
		for stop in stops:
			dist = haversine(float(lat), float(lon), stop.location_lat, stop.location_lon)
			if(dist < min_dist):
				min_dist = dist
				min_stop = stop
	else:
		# we failed to load the stops
		return HttpResponse(json.dumps({'success' : 'fail'}))
	closest_stop =  min_stop
	
	#get data from db about closest stop
	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name) 
	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	arrival_estimates_at_stop = Arrival_Estimate.objects.filter(stop=min_stop).order_by('time')
	
	#get the next X shuttles in the arrival estimates for each vehicles
	#these will be displayed with each shuttle that is arriving at the users closest stop
	next_shuttles_per_route = []
	# for each arrival estimate
	i = 0;
	for close_ae in arrival_estimates_at_stop:
		#get the next 3 arrival estimates for the given ae
		ae_set = close_ae.arrivals_after(3)
		next_shuttles_per_route.append([close_ae.route.longname, close_ae.stop.name, calculate_min_until(close_ae.time), []])
		print next_shuttles_per_route
		#store in dict
		for ae in ae_set:
			next_shuttles_per_route[i][3].append([ae.route.longname, ae.stop.name, calculate_min_until(ae.time)])
		i+= 1

			
	
	#next_shuttles = list()
	#for ae in arrival_estimates_at_stop:
	#	next_shuttles.append([ae.route.longname, calculate_min_until(ae.time), ae.id])
	#store the closest stop id in the stop variable
	request.session['closest_stop'] = closest_stop.stop  	
	return HttpResponse(json.dumps({'closest' : closest_stop.name, 'next_shuttles_route' : next_shuttles_per_route, 'success' : 'success'}))

#return possible destinations to show on the main page
def get_destinations(request):
	destinations = list()
	for s in Stop.objects.all():
		dest = dict()
		dest['name'] = s.name
		dest['id'] = s.stop
		destinations.append(dest)
	return HttpResponse(json.dumps(destinations))

@never_cache
def destination_selected(request):
	s = Session.objects.get(pk=request.session.session_key)
	start = time.clock()
	#wait up to 15 seconds for walking data to come back from Bing maps
	while 'walking_times' not in s.get_decoded():
		s = Session.objects.get(pk=request.session.session_key)
		if time.clock() - start >15:
			return HttpResponse(json.dumps({'route_string': "Could not load walking data!"}))
	print "Selected stop: " + Stop.objects.get(stop=request.POST['destination_id']).name
	selected_stop = Stop.objects.get(stop=request.POST['destination_id'])
	print "It will take " + str(request.session['walking_times'][request.POST['destination_id']]) + " sec to get to stop " + request.POST['destination_id']
	just_walking_time = request.session['walking_times'][request.POST['destination_id']]
	min_time = 10000
	min_time_walk = 10000
	min_transit = 10000
	min_transit_total = 10000
	min_walk = 10000
	min_walk_total = 10000
	path = []
	walk_path = []
	transit_path = []
	
	#if we dont have any arrival_estimates, fail
	if request.session['closest_stop'] == selected_stop.stop:
		return HttpResponse(json.dumps({'success' : 'chose identity stop', 'just_walking_time': just_walking_time}))
	if len(Arrival_Estimate.objects.all()) == 0:
		return HttpResponse(json.dumps({'success' : 'failed to load arrivals', 'just_walking_time': just_walking_time}))
	# for every stop at harvard

	for stop in Stop.objects.all():
		# get the walking time to it
		walk_time_to_stop = request.session['walking_times'][str(stop.stop)]
		current_time = datetime.utcnow()
		arrival_time = current_time + timedelta(seconds=walk_time_to_stop)
		
		#figure out what time UTC you will arrive at the stop if you walked to it
		arrival_time = arrival_time.replace(tzinfo=UTC)
		
		#get all vehicle arrivals at that stop after your arrival time
		useable_arrivals = Arrival_Estimate.objects.filter(time__gte=arrival_time).filter(stop=stop)
		#for each of these arrivals
		for ae in useable_arrivals:
			#print str(ae.stop)
			
			#get the next arrivals for that vehicle at your selected stop (see models.py)	
			arrivals_after = ae.all_arrivals_after()#.filter(stop=selected_stop)
			
			#for each of these arrivals
			for arrival_ae in arrivals_after:
				shuttle_time = calculate_time_between(arrival_ae.time, ae.time)
				#total_transit_time = shuttle_time + timedelta(seconds=walk_time_to_stop)
				
				#get the total time from now to when shuttle arrives
				walk_time_from_stop = Walking_Time.objects.get(start_stop=arrival_ae.stop.stop, end_stop=selected_stop.stop).walking_time
				total_time = calculate_time_between(arrival_ae.time, current_time).total_seconds() + walk_time_from_stop
				arrival_time = current_time + timedelta(seconds = total_time);
				#total_time = shuttle_time #+ timedelta(seconds=walk_time_to_stop)

				#if its a new fastest time add it
				transit_time = walk_time_to_stop + walk_time_from_stop + shuttle_time.total_seconds()

				# the next 3 selection structures build our 3 forms of optimization: total time, transit time, and walking time
				# each method has a 'secondary' optimization if the times are equal or sufficiently equal
				# the variables are somewhat standard. min_blank is the minimum time for that mode
				# min_blank_blank is the secondary optimization minimum
				# for instance min_walk is minimum walk time found and min_walk_total is the total time for that minimum walk 
				if round(total_time/60) < round(min_time/60):
					print "Start: %s: %s\tEnd: %s: %s \tdiff: %s \twalk1: %s walk2: %s\ttotal: %s" % (ae.stop,ae.time, arrival_ae.stop,arrival_ae.time, shuttle_time, walk_time_to_stop, walk_time_from_stop, total_time)
					min_time = total_time
					path = []
					path.append(ae)
					path.append(arrival_ae)
					path.append(selected_stop)
					path.append(total_time)
					path.append(transit_time)
					min_time_walk = walk_time_to_stop
					#print 'FASTER: ' + str(ae.stop.name) + " to " + str(arrival_ae.stop.name) + "\ttime:" + str(total_time)
				#if they are EQUAL take the one with least walking to the first stop
				elif round(total_time/60) == round(min_time/60):
					if walk_time_to_stop < min_time_walk:
						print "Start: %s: %s\tEnd: %s: %s \tdiff: %s \twalk1: %s walk2: %s\ttotal: %s" % (ae.stop,ae.time, arrival_ae.stop,arrival_ae.time, shuttle_time, walk_time_to_stop, walk_time_from_stop, total_time)
						min_time = total_time
						min_time_walk = walk_time_to_stop
						path = []
						path.append(ae)
						path.append(arrival_ae)
						path.append(selected_stop)
						path.append(total_time)
						path.append(transit_time)
				# for convenience get the path with the LEAST walking
				if round((walk_time_to_stop + walk_time_from_stop)/60) < round(min_walk/60):
					min_walk = walk_time_to_stop + walk_time_from_stop
					walk_path =[]
					walk_path.append(ae)
					walk_path.append(arrival_ae)
					walk_path.append(selected_stop)
					walk_path.append(total_time)
					walk_path.append(transit_time)
					min_walk_total = total_time
					print "MIN_WALK: %s: %s\tEnd: %s: %s \tdiff: %s \twalk1: %s walk2: %s\ttotal: %s" % (ae.stop,ae.time, arrival_ae.stop,arrival_ae.time, shuttle_time, walk_time_to_stop, walk_time_from_stop, total_time)
				elif round((walk_time_to_stop + walk_time_from_stop)/60) == round(min_walk/60):
					if total_time < min_walk_total:
						min_walk = walk_time_to_stop + walk_time_from_stop
						min_walk_total = total_time
						walk_path =[]
						walk_path.append(ae)
						walk_path.append(arrival_ae)
						walk_path.append(selected_stop)
						walk_path.append(total_time)
						walk_path.append(transit_time)
				if (round(transit_time/60) < round(min_transit/60)):
					min_transit = transit_time
					transit_path = []	
					transit_path.append(ae)
					transit_path.append(arrival_ae)
					transit_path.append(selected_stop)
					transit_path.append(total_time)
					transit_path.append(transit_time)
					min_transit_total = transit_time
				elif (round(transit_time/60) == round(min_transit/60)):
					if total_time < min_transit_total:
						min_transit = transit_time
						min_transit_total = total_time
						transit_path = []	
						transit_path.append(ae)
						transit_path.append(arrival_ae)
						transit_path.append(selected_stop)
						transit_path.append(total_time)
						transit_path.append(transit_time)	

	# build our three context dictionaries for output to the file
	fastest = {'on_stop' : path[0].stop.name,'board_time' : (path[0].time - current_time.replace(tzinfo=UTC)).total_seconds(),'route' : path[0].route.longname, 'off_stop' : path[1].stop.name, 'end_stop' : path[2].name, 'total_time' : path[3], 'transit_time' : path[4]}
	least_walking = {'on_stop' : walk_path[0].stop.name,'board_time' : (walk_path[0].time - current_time.replace(tzinfo=UTC)).total_seconds(), 'route' : walk_path[0].route.longname, 'off_stop' : walk_path[1].stop.name, 'end_stop' : walk_path[2].name, 'total_time' : walk_path[3], 'transit_time' : walk_path[4]}
	least_transit = {'on_stop' : transit_path[0].stop.name,'board_time' : (transit_path[0].time - current_time.replace(tzinfo=UTC)).total_seconds(), 'route' : walk_path[0].route.longname, 'off_stop' : transit_path[1].stop.name, 'end_stop' : transit_path[2].name, 'total_time' : transit_path[3], 'transit_time' : transit_path[4]}
	
	#return the json object
	return HttpResponse(json.dumps({ 'just_walking_time' : just_walking_time, 'fastest' : fastest,'least_walking' : least_walking, 'least_transit' : least_transit, 'success':'success'} ))


# calculate the walking times from the users location to all shuttle stops
def calculate_routes(request):
	#data = request.POST
	current_location = {'lat' : request.POST.get('coords[latitude]'), 'lon' : request.POST.get('coords[longitude]')}
	#destination_stop = Stop.objects.filter(name='Quad')
	#http://dev.virtualearth.net/REST/v1/Routes/Walking?
	#get walking distances to all stops
	stop_walking_times = dict()
	
	for stop in Stop.objects.all():
		#get the walking data from Bing maps
		params = urlencode({'wp.0': str(current_location['lat']) + ','+ str(current_location['lon']), 'wp.1': str(stop.location_lat) + "," + str(stop.location_lon), 'key' : 'Am8_5ptSSXJmpyJ1b6hf_U5Uvc7rqMOsY2vkRuDdne5TG-R2VA3hCoNb7gI4RWU5'}) 
		
		data_return = urlopen("http://dev.virtualearth.net/REST/v1/Routes/Walking?%s" % params)
	
		route_data = json.load(data_return)
		travel_duration = route_data['resourceSets'][0]['resources'][0]['travelDuration']
		stop_walking_times[str(stop.stop)] = travel_duration
	#store it into a session variable for later access
	request.session['walking_times'] = stop_walking_times
	request.session.save()
	return HttpResponse('')		
	
