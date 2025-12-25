import pandas as pd
import numpy as np

# Creating a mock dataset representative of the Global Space Exploration Dataset
data = {
    'mission_id': range(1, 11),
    'mission_name': ['Apollo 11', 'Falcon 9 Launch', 'Mars Rover Perseverance', 'Chandrayaan-3', 'Starlink-105', 'Voyager 1', 'Artemis I', 'Soyuz MS-24', 'Tianwen-1', 'Beresheet'],
    'agency': ['NASA', 'SpaceX', 'NASA', 'ISRO', 'SpaceX', 'NASA', 'NASA', 'Roscosmos', 'CNSA', 'SpaceIL'],
    'agency_type': ['Government', 'Private', 'Government', 'Government', 'Private', 'Government', 'Government', 'Government', 'Government', 'Private'],
    'nation': ['USA', 'USA', 'USA', 'India', 'USA', 'USA', 'USA', 'Russia', 'China', 'Israel'],
    'launch_site': ['Kennedy Space Center', 'Cape Canaveral', 'Kennedy Space Center', 'Satish Dhawan Space Centre', 'Kennedy Space Center', 'Cape Canaveral', 'Kennedy Space Center', 'Baikonur Cosmodrome', 'Wenchang', 'Cape Canaveral'],
    'mission_type': ['Moon', 'Earth Observation', 'Mars', 'Moon', 'Earth Observation', 'Interstellar', 'Moon', 'ISS', 'Mars', 'Moon'],
    'rocket': ['Saturn V', 'Falcon 9', 'Atlas V', 'LVM3', 'Falcon 9', 'Titan IIIE', 'SLS', 'Soyuz-2', 'Long March 5', 'Falcon 9'],
    'payload_weight': [45000, 22800, 1025, 3900, 15000, 722, 95000, 7000, 5000, 585],
    'budget': [25000, 62, 2700, 75, 50, 250, 4100, 150, 8000, 100], # in millions USD
    'launch_date': ['1969-07-16', '2023-05-01', '2020-07-30', '2023-07-14', '2024-01-10', '1977-09-05', '2022-11-16', '2023-09-15', '2020-07-23', '2019-02-22'],
    'status': ['Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Failure'],
    'environmental_impact': [8, 3, 5, 4, 3, 7, 9, 6, 8, 3] # scale 1-10
}

df = pd.DataFrame(data)
df.to_csv('/Users/ahsansaleem/Desktop/krrfinalproject/data/space_missions.csv', index=False)
print("Mock dataset created at /Users/ahsansaleem/Desktop/krrfinalproject/data/space_missions.csv")
