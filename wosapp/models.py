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
  location_lon =  models.DecimalField(db_column = 'lon',max_digits = 18, decimal_places = 15)
  location['lat'] = location_lat
  location['lon'] = location_lon
  #arrival estimates are in new table linked in via a vehicle instance foreign key
  route = models.ForeignKey('Route')
  speed = models.FloatField()
  updated = models.DateTimeField()
  def __unicode__(self):
    return ('%s' % (self.vid))

class Arrival_Estimate(models.Model):
  stop = models.ForeignKey('Stop')
  route = models.ForeignKey('Route')
  vehicle = models.ForeignKey('Vehicle')
  time = models.DateTimeField()
  def __unicode__(self):
    return '%s, %s, %s, %s' % (self.vehicle.vid, self.route, self.stop, self.time)

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
