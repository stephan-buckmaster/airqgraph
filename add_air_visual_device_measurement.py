import sys
import requests
import json
import os

if (len(sys.argv) < 3): 
    sys.exit("Need air_visual_device_url and graphql_url")

air_visual_device_url=sys.argv[1]
graphql_url=sys.argv[2]

# Load device data
response = requests.get(air_visual_device_url)
data = json.loads(response.text)

graphql_query = '''
mutation CreateNewAirVisualDeviceMeasurement($input: AirVisualDeviceMeasurementInput!) {
  createAirVisualDeviceMeasurement(input: $input) {
    air_visual_device_measurement { id co2 hm aqius pr aqicn  created_at}
    success
    errors 
  }
}
'''


headers = {}
if os.getenv("BEARER_AUTH_TOKEN_FILE"):
  token =  open(os.getenv("BEARER_AUTH_TOKEN_FILE")).readline().strip()
  headers['Authorization'] = f"Bearer {token}"

result = requests.post(graphql_url, json={'query': graphql_query, 'variables': {'input': data['current']}}, headers=headers)

if result.status_code == requests.codes.ok:
    print(json.loads(result.text))
else:
    print("Response status",  result.status_code)
    print(result.text)
