import googlemaps

API_KEY = 'AIzaSyANPmwlkany9JXvhyR8ytfleha3fQQYbKI'
gmaps = googlemaps.Client(API_KEY)


def duration(start, end):
    road = gmaps.distance_matrix(start, end)
    return road['rows'][0]['elements'][0]['duration']['text']


def distance(start, end):
    road = gmaps.distance_matrix(start, end)
    return road['rows'][0]['elements'][0]['distance']['text']
