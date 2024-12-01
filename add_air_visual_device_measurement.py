import sys

if (len(sys.argv) < 3): 
    sys.exit("Need airvisual_device_url and graphql_url")

airvisual_device_url=sys.argv[1]
graphql_url=sys.argv[2]

import requests
import json

# Load device data
response = requests.get(airvisual_device_url)
data = json.loads(response.text)

graphql_query = '''
mutation CreateNewAirvisualDeviceMeasurement($input: AirvisualDeviceMeasurementInput!) {
  createAirvisualDeviceMeasurement(input: $input) {
    airvisual_device_measurement { id co2 hm aqius pr aqicn }
    success
    errors 
  }
}
'''

r = requests.post(graphql_url, json={'query': graphql_query, 'variables': {'input': data['current']}})

print(json.loads(r.text))

# TODO How to handle errors, success in response is not True?
