from math import radians, cos, sin, asin, sqrt
import datetime
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    #km = 6367 * c # s = radius * theta
    mile = 3,959 * c
    return mile 

# calculates time difference between the current time and the supplied one to the nearest 1/10th of a min
def calculate_min_until(atime):
	atime = atime.replace(tzinfo=None)
	timedifference = atime - datetime.datetime.utcnow()
	return round(timedifference.total_seconds()/60 , 1)
    
    
