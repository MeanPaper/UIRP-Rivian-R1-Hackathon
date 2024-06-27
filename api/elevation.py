import requests
import numpy as np
import json

def get_route(from_location, to_location):
    api_key = "6NqtgXkhFbfuYnQa6LK2QvtHuvUdDUkK"
    url = f"https://www.mapquestapi.com/directions/v2/route?key={api_key}&from={from_location}&to={to_location}&outFormat=json"
    response = requests.get(url)

    if response.status_code == 200:
        directions = response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

    # Extract latitude, longitude, distance, and instructions
    coordinates = []
    for leg in directions['route']['legs']:
        for maneuver in leg['maneuvers']:
            lat = maneuver['startPoint']['lat']
            lng = maneuver['startPoint']['lng']
            distance = maneuver['distance']
            instr = maneuver['narrative']
            coordinates.append((lat, lng, distance, instr))

    return coordinates

def check_distance(coordinates, threshold):
    if threshold == "Low":
        threshold = 0.1
    elif threshold == "Medium":
        threshold = 0.05
    else:
        threshold = 0.01
    newCoordinates = []
    for index, coords in enumerate(coordinates[:-1]):  # Ensure the next index exists
        lat1, lon1, d1, instr1 = coords
        if d1 > threshold:
            num_points = int(d1 // threshold) + 1  # Number of points to interpolate
            distance = d1 / num_points
            lat2, lon2, d2, instr2 = coordinates[index + 1]
            interpolated = interpolate_coordinates(lat1, lon1, lat2, lon2, num_points, distance, instr1)
            newCoordinates.extend(interpolated)
        else:
            newCoordinates.append((lat1, lon1, d1, instr1))
    return newCoordinates

def interpolate_coordinates(lat1, lon1, lat2, lon2, num_points, distance, instr):
    # Create arrays of latitudes and longitudes
    lats = np.linspace(lat1, lat2, num_points)
    lons = np.linspace(lon1, lon2, num_points)
    distances = np.full(num_points, distance)
    instrs = np.full(num_points, instr)

    # Combine into a list of tuples
    coordinates = list(zip(lats, lons, distances, instrs))
    return coordinates

def get_elevation(data):
    # Format the coordinates into the request object
    locations = [{"latitude": lat, "longitude": lon} for lat, lon, _, _ in data]

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

    # Combine elevation data with the original data
    path_with_elevation = []
    for i, elevation_data in enumerate(elevation['results']):
        lat = elevation_data['latitude']
        lon = elevation_data['longitude']
        elev = elevation_data['elevation']
        distance = data[i][2]
        instr = data[i][3]
        path_with_elevation.append({
            'latitude': lat,
            'longitude': lon,
            'elevation': elev,
            'distance': distance,
            'instr': instr
        })

    return path_with_elevation

