# Create your views here.

from django.shortcuts import render

from wosapp.models import Vehicle

def index(response):
	vehicles_running = Vehicle.objects.all()
	context = {'vehicles_running' : vehicles_running}
	return render(response, 'wosapp/index.html', context)
