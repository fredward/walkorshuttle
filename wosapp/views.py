# Create your views here.

from django.shortcuts import render

from wosapp.models import Vehicle, Route, Stop

def index(response):
	closest_stop =  Stop.objects.get(name__exact='Boylston Gate')
	#for( veh in vehicles_running):
	#	route = veh.route
	
	possible_routes = Route.objects.filter(stops__name__contains=closest_stop.name)
	print possible_routes.values('id')
	vehicles_running_to_stop = Vehicle.objects.filter(route__in=possible_routes)
	#routes_in_service =  Route.objects.filter(id__in=vehicles_running_to_stop.values['route'])
	
	context = {'routes_in_service' : possible_routes, 'vehicles_running_to_stop' : vehicles_running_to_stop, 'closest_stop' : closest_stop}
	return render(response, 'wosapp/index.html', context)
