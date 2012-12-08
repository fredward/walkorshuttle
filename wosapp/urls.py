from django.conf.urls import patterns, url
from wosapp import views

urlpatterns = patterns('',
   url(r'^geolocate/$', views.process_location),
	 url(r'^$', views.index, name='index'),
	 url(r'^destinations/$', views.get_destinations),
	 url(r'^route/$', views.calculate_routes),
	 url(r'^destination_selected/$', views.destination_selected),
	 # url to run the method to get all walking times from stop to stop
	 url(r'^getwalkingtimes/$', views.get_stop_walking_times)
)
