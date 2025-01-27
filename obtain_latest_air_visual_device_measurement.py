import sys
import requests
import json

if (len(sys.argv) < 2): 
    sys.exit("Need graphql_url")

graphql_url=sys.argv[1]

graphql_query = '''
query LastAirVisualDeviceMeasurement {
  getLatestAirVisualDeviceMeasurement  {
    success
    errors
    air_visual_device_measurement {
      id
      co2
      pm25 { conc aqius aqicn }
      pm10 { conc aqius aqicn }
      pm1 { conc aqius aqicn }
      pr
      hm
      tp
      aqius
      aqicn
      mainus
      maincn
      ts
      created_at
    }
  }
}
'''

r = requests.post(graphql_url, json={'query': graphql_query})

data = json.loads(r.text)['data']
print(data['getLatestAirVisualDeviceMeasurement'])
