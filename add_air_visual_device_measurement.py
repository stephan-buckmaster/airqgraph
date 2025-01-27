import sys
import requests
import json

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

r = requests.post(graphql_url, json={'query': graphql_query, 'variables': {'input': data['current']}})

print(json.loads(r.text))

# TODO How to handle errors, success in response is not True?
