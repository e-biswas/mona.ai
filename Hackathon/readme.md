# Disaster Response Coordination System Challenge

## Background
Saarland has experienced severe rainfall recently, leading to significant flooding and other catastrophes. 
To mitigate future impacts, we need a system that can help coordinate disaster response efforts effectively. 
This challenge involves building an application that can track and manage emergency response resources, 
predict potential flood zones based on rainfall data, and provide real-time alerts to the relevant authorities,
based on their location and skills. The floot happened between 14 - 17 may 2024.


## Objective
Create a program that can:
1. Ingest and process rainfall data. Check if the data is complete and clean.
2. Predict potential flood zones. 
3. Track the availability and location of emergency response resources.
4. Match the best teams to the emergencies based on required skills, team size, and availability based on time of the day, 
travel time, and distance.

## Requirements

### 1. Data Ingestion and Processing
- The program should accept a CSV file containing historical rainfall data. Each entry should include a timestamp, location (latitude and longitude), and rainfall amount (in mm).
- Process this data to calculate the average rainfall over different regions.

### 2. Flood Zone Prediction
- Using the processed rainfall data, predict potential flood zones. For simplicity, assume a basic threshold model where areas receiving more than a certain amount of rainfall within a specific time frame are at risk of flooding.
- The threshold values can be predefined (e.g., 50mm of rainfall in 24 hours).

### 3. Resource Tracking
- Maintain a list of emergency response resources (e.g., rescue boats, medical supplies, personnel) along with their current status (available, deployed, under maintenance) and location.
- The program should be able to update the status and location of these resources dynamically.

### 4. Team Matching
- Match the best teams to the emergencies based on required skills, team size, and availability considering the time of the day, travel time, and distance.
- Ensure that the teams assigned to each emergency have the necessary skills and are the closest in proximity to the emergency location to optimize response time.

## Input
- csv data from the folder


Hints:
- Saarland: https://www.openstreetmap.org/relation/62372
- Saar river: https://www.openstreetmap.org/relation/390393
- Blies river: https://www.openstreetmap.org/relation/410743
