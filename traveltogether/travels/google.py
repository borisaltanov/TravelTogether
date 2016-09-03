import googlemaps


# API Key is deactivated, use you own key for now.
API_KEY = 'YOUR_GOOGLEMAPS_API_KEY_HERE'
gmaps = googlemaps.Client(API_KEY)


def duration(start, end):
    road = gmaps.distance_matrix(start, end)
    return road['rows'][0]['elements'][0]['duration']['text']


def distance(start, end):
    road = gmaps.distance_matrix(start, end)
    return road['rows'][0]['elements'][0]['distance']['text']
