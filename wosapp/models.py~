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
  route = models.PositiveIntegerField()
  speed = models.FloatField()
  updated = models.DateTimeField()

class Arrival_Estimate(models.Model):
  stop = models.PositiveIntegerField()
  route = models.PositiveIntegerField()
  vehicle = models.ForeignKey('Vehicle')
  time = models.DateTimeField()
