import json
import tsp

from osgeo import osr
from osgeo import ogr

def project_to_meters(lat, lng):
    """Translate EPSG:4326 -> EPSG:3857

    This is done in order to get evaluation of distance in meters.
    """
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(3857)

    transform = osr.CoordinateTransformation(source, target)

    point = ogr.CreateGeometryFromWkt(f"POINT ({lat} {lng})")
    point.Transform(transform)

    return (int(point.GetX()), int(point.GetY()))

def main():
    randojson = ""
    points_of_interest = []
    points_of_interest_orig = []

    starting_point = { 'lat': 60.344230, 
        'lng': 24.836719,
        'name': "STARTING POINT"}

    # Ride with GPS JSON
    with open('rando.json') as randofile:
        randojson = json.load(randofile)
        points_of_interest_orig = randojson['points_of_interest']

    points_of_interest_orig.insert(0, starting_point)

    # Limit the area
    for point in points_of_interest_orig:
        if point['lng'] > 24.506857123730356 and point['lng'] < 26.835505390216667:
            points_of_interest.append(point)

    coordinates = []
    for point in points_of_interest:
        lat = point['lat'] 
        lng = point['lng']
        latlng = (lat, lng)
        xy = project_to_meters(lat, lng)
        coordinates.append(xy)

    print("Calculating the order...")
    distance, best_state = tsp.tsp(coordinates)

    for state in best_state:
        print(points_of_interest[state]['name'])

    print('The best state found is: ', best_state)

    print('The distance at the best state is: ', distance)

if __name__ == '__main__':
    main()