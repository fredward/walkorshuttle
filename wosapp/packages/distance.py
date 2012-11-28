from math import radians, cos, sin, asin, sqrt

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

#def euclidian(lon1, lat1, lon2, lat2):
#    dist = sqrt( (lon1-lon2)*(lon1-lon2) + (lat1-lat2)*(lat1-lat2) )
    
    
