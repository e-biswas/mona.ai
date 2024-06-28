from flask import Flask, request, jsonify, render_template
import pandas as pd
import googlemaps
from datetime import datetime
import time

app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyCDKwj1fOxCW6VAQOc8djbb0mclhywXUcI')

# Load the emergency services data
resources_df = pd.read_csv('data/generated_data.csv')

# Extract unique skills from the dataset
all_skills = set(skill.strip() for skills in resources_df['skills'] for skill in skills.strip("[]").replace("'", "").split(','))

# Function to check if a service is open at a given time
def is_open(service, current_time):
    current_day = current_time.strftime('%A').lower()
    open_hour_start = service[f'open_hour_{current_day}_start']
    open_hour_end = service[f'open_hour_{current_day}_end']
    
    if open_hour_start == "00:00" and open_hour_end == "23:59":
        return True

    open_time = datetime.strptime(open_hour_start, "%H:%M").time()
    close_time = datetime.strptime(open_hour_end, "%H:%M").time()
    
    if open_time <= current_time.time() <= close_time:
        return True
    return False

# Function to find the nearest service
def find_nearest_service(emergency_location, required_skills, required_team_size):
    now = datetime.now()
    distances = []
    
    for index, service in resources_df.iterrows():
        if is_open(service, now) and required_skills.issubset(set(service['skills'].strip("[]").replace("'", "").split(', '))) and service['team_size'] >= required_team_size:
            service_location = (service['geometry/location/lat'], service['geometry/location/lng'])
            distance_matrix = gmaps.distance_matrix(emergency_location, service_location, mode="driving", departure_time=now)
            distance_info = distance_matrix['rows'][0]['elements'][0]
            distances.append((index, distance_info['distance']['value'], distance_info['duration']['value']))

    if not distances:
        return None
    
    nearest_service_index, min_distance, min_duration = min(distances, key=lambda x: x[1])
    nearest_service = resources_df.loc[nearest_service_index]
    nearest_service['distance'] = min_distance
    nearest_service['duration'] = min_duration

    return nearest_service

@app.route('/')
def index():
    return render_template('index.html', skills=all_skills)

@app.route('/find_service', methods=['POST'])
def find_service():
    data = request.json
    emergency_location = (data['lat'], data['lng'])
    required_skills = set(data['skills'])
    required_team_size = data['team_size']
    nearest_service = find_nearest_service(emergency_location, required_skills, required_team_size)
    
    if nearest_service is not None:
        return jsonify(nearest_service.to_dict())
    else:
        return jsonify({'error': 'No matching service found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
