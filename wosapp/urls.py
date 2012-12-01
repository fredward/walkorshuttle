from django.conf.urls import patterns, url
from wosapp import views

urlpatterns = patterns('',
         url(r'^geolocate/$', views.process_location),
	 url(r'^$', views.index, name='index'),
	 url(r'^destinations/$', views.get_destinations),
)
