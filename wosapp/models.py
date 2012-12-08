from django.db import models

# Create your models here.
from django.db import models
#class Shuttle(models.Model):
#
class Vehicle(models.Model):
	vid = models.IntegerField()
	STATUS_CHOICES = (('up','Tracking Up'),('down','Tracking Down'))
	status = models.CharField(max_length=4, choices=STATUS_CHOICES)
	heading = models.IntegerField()
	#the lat lon of the vehical, stored as a dict of decimal fields
	location = dict()
	location_lat = models.DecimalField(db_column = 'lat',max_digits = 18, decimal_places = 15)
	location_lon =	models.DecimalField(db_column = 'lon',max_digits = 18, decimal_places = 15)
	location['lat'] = location_lat
	location['lon'] = location_lon
	#arrival estimates are in new table linked in via a vehicle instance foreign key
	route = models.ForeignKey('Route', null=True)
	speed = models.FloatField()
	updated = models.DateTimeField()
	def __unicode__(self):
		return ('%s' % (self.vid))

			

class Arrival_Estimate(models.Model):
	stop = models.ForeignKey('Stop', null=True)
	route = models.ForeignKey('Route', null=True)
	vehicle = models.ForeignKey('Vehicle')
	time = models.DateTimeField()
	def __unicode__(self):
		return '%s, %s, %s, %s' % (self.vehicle.vid, self.route, self.stop, self.time)
	#all the arrivals after the given one (for the vehicle)
	def arrivals_after(self,num):
		vehicle_ae = Arrival_Estimate.objects.filter(vehicle=self.vehicle)
		mark = False
		ae_set = []
		count = 0
		for ae in vehicle_ae:
			if(mark == True and count < num):
				ae_set.append(ae)
				count += 1
			if(ae == self):
				mark = True
		return ae_set
	#QUERYSET of all arrivals after current for the vehicle 
	def all_arrivals_after(self):
		vehicle_ae = Arrival_Estimate.objects.filter(vehicle=self.vehicle).filter(time__gt=self.time)
		return vehicle_ae

class Stop(models.Model):
	stop = models.PositiveIntegerField()
	name = models.CharField(max_length = 75)
	desc = models.CharField(max_length = 100)
	code = models.CharField(max_length = 25)
	location_lat = models.DecimalField(db_column = 'lat', max_digits = 18, decimal_places = 15)
	location_lon = models.DecimalField(db_column = 'lon', max_digits = 18, decimal_places = 15)
	location = dict()
	location['lat'] = location_lat
	location['lon'] = location_lon
	def __unicode__(self):
		return self.name


class Route(models.Model):
	rid = models.PositiveIntegerField()
	longname = models.CharField(max_length = 100)
	shortname = models.CharField(max_length = 50)
	type = models.CharField(max_length = 15)
	color = models.CharField(max_length = 6)
	desc = models.CharField(max_length = 100)
	# pickled array of segments
	segments = models.CharField(max_length = 400)
	# ManyToMany means that you can 'add' multiple stops into the stops field
	stops = models.ManyToManyField(Stop)
	# order will be a json-ed array of the stopids in the correct order
	order = models.CharField(max_length = 500)
	def __unicode__(self):
		return self.longname

class Walking_Time(models.Model):
	start_stop = models.PositiveIntegerField()
	end_stop = models.PositiveIntegerField()
	walking_time = models.PositiveIntegerField()
	def __unicode__(self):
		return Stop.objects.get(stop=self.start_stop).name + " to " + Stop.objects.get(stop=self.end_stop).name
