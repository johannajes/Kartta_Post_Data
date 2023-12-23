import xml.etree.ElementTree as ET

import requests

# Define the namespace used in the XML file
namespaces = {'ns': 'http://www.topografix.com/GPX/1/1'}
# Load and parse the XML file
tree = ET.parse('11235_talvireitti_kurikka_pattikangas.gpx')
root = tree.getroot()

coordinates = []

# Find all track points and prepare them in JSON format
for trkseg in root.findall('.//ns:trkseg', namespaces):
    for trkpt in trkseg.findall('ns:trkpt', namespaces):
        lat = trkpt.get('lat')
        lon = trkpt.get('lon')
        
        # Creating a JSON object for each coordinate
        json_data = {
            'lat': lat,
            'lon': lon
        }

        # Send the JSON data to the server
        try:
            response = requests.post("http://localhost:5000/uusimittaus", json=json_data)
            if response.ok:
                print(f"Success: {response.json()}")
            else:
                print(f"Error: Status Code {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")

