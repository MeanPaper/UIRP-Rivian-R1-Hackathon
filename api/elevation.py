import requests
import numpy as np
import requests
import json


def get_route(from_location,to_location):
    api_key = "6NqtgXkhFbfuYnQa6LK2QvtHuvUdDUkK"

    url = f"https://www.mapquestapi.com/directions/v2/route?key={api_key}&from={from_location}&to={to_location}&outFormat=json"

    response = requests.get(url)

    if response.status_code == 200:
        directions = response.json()
        print(directions)
    else:
        print(f"Error: {response.status_code}")

    # Extract latitude, longitude, and distance
    coordinates = []
    for leg in directions['route']['legs']:
        for maneuver in leg['maneuvers']:
            lat = maneuver['startPoint']['lat']
            lng = maneuver['startPoint']['lng']
            distance = maneuver['distance']
            coordinates.append((lat, lng, distance))

    return coordinates

def check_distance(coordinates, threshold):
  newCoordinates = []
  for index, coords in enumerate(coordinates):
    x1, y1, d1 = coords
    if(d1>threshold):
      n = d1//threshold # number of points
      distance = d1/threshold
      x2, y2, d2 = coordinates[index+1]
      interpolated = interpolate_coordinates(x1,y1,x2,y2,int(n),distance)
      newCoordinates.extend(interpolated)
    else:
      newCoordinates.append((x1,y1,d1))
  return newCoordinates

def interpolate_coordinates(lat1, lon1, lat2, lon2, num_points, distance):
    # Create arrays of latitudes and longitudes
    lats = np.linspace(lat1, lat2, num_points)
    lons = np.linspace(lon1, lon2, num_points)
    distances = np.full(num_points, distance)


    # Combine into a list of tuples
    coordinates = list(zip(lats, lons, distances))
    return coordinates

def get_elevation(data):
    # Format the coordinates into the request object
    locations = [{"latitude": lat, "longitude": lon} for lat, lon, _ in data]

    # Create the request payload
    payload = {
        "locations": locations
    }

    # Send the request
    url = "https://api.open-elevation.com/api/v1/lookup"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    elevation = requests.post(url, headers=headers, data=json.dumps(payload))
    elevation = elevation.json()
    path_with_elevation = elevation['results']
    return path_with_elevation


coordinates = get_route("Champaign","Rantoul")
data = check_distance(coordinates,1)
final = get_elevation(data)


