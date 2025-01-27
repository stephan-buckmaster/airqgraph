# Air Quality Monitoring Server


Motivation: I have an [IQAir](https://www.iqair.com) air quality monitor which measures air pollution exposure just outside our home. Their mobile app allows viewing real-time and historic air quality. I can share the sensor data with millions of users through the same app. 

However, these users (including my friends) need to create an account and log in to use the app -- an unnecessary hurdle. So I have developed this application to make the data available without an account.

## Overview
The system involves two primary APIs:

1. IQAir API: This API is provided by IQAir and is used to fetch the current air quality measurements from the device. The device uploads these measurements to the IQAir cloud, where they are accessible via the web and mobile apps, as well as the API.
2. GraphQL API (This Server): This custom GraphQL API is developed to handle the data fetched from the IQAir API. It allows:
    - Submitting the current air quality measurements to store in a PostgreSQL database.
    - Retrieving the most recent air quality records for further processing, such as displaying on a web application.

The API server is a Flask application using Ariadne.

## IQAir API specifics

In general, the device id used in the API requests would only be known to the owner. So this API allows such owners to publish the data recorded by their device. They can find this device id by logging into their account and navigating to their device page. On the right will be a list of API links.

![Screenshot of IQAir Device Page](images/iqair-device-page.png?raw=true "Screenshot of IQAir Device Page")


This curl command can be used to obtain the JSON of the measurements:

```
curl https://device.iqair.com/v2/1234567890abcdef12345678
```

The response is JSON which is unfortunately not further documented. One key of the hash is `current` with sample values like this:

```
{
  "current": {
    "co2": 476,
    "pm25": {
      "conc": 24,
      "aqius": 79,
      "aqicn": 34
    },
    "pm10": {
      "conc": 36,
      "aqius": 33,
      "aqicn": 36
    },
    "pm1": {
      "conc": 19,
      "aqius": 69,
      "aqicn": 27
    },
    "pr": 102406,
    "hm": 87,
    "tp": 4.8,
    "ts": "2024-12-03T04:10:11.000Z",
    "mainus": "pm25",
    "maincn": "pm10",
    "aqius": 79,
    "aqicn": 36
  }
}
```

The metrics provided are:

* `co2`: Carbon dioxide concentration
* `pm25, pm10, pm1`: Particulate matter concentrations and air quality indices (AQI) for various particle sizes
* `conc`: Concentration of particulate matter
* `aqius`: AQI based on the US standard
* `aqicn`: AQI based on the China standard
* `pr`: Atmospheric pressure
* `hm`: Humidity
* `tp`: Temperature
* `ts`: Timestamp of the data
* `mainus`: The main pollutant according to US standards
* `maincn`: The main pollutant according to China standards
* `aqius`: Overall AQI based on US standards
* `aqicn`: Overall AQI based on China standards


In the database, fields related to particulate matter are expanded so that one measurement corresponds to one table row. For example, `pm25.conc` is stored as `pm25_conc`.

## GraphQL Server and database schema

The server provides three queries and one mutation:


```
type Query {
    listAirVisualDeviceMeasurements: AirVisualDeviceMeasurementsResult!
    getLatestAirVisualDeviceMeasurement: AirVisualDeviceMeasurementResult!
    getAirVisualDeviceMeasurement(id: ID!): AirVisualDeviceMeasurementResult!
}

type Mutation {
    createAirVisualDeviceMeasurement(input: AirVisualDeviceMeasurementInput): AirVisualDeviceMeasurementResult!
}
```

The fields of a AirVisualDeviceMeasurement are those of IQAir's JSON response, plus a separate timestamp, and a database id.
The structure of pm1, pm10, pm25 are the same in the GraphQL query, the nesting is kept. But not so in the database schema where this is flattened.

```
=> \d air_visual_device_measurement;
                                         Table "public.air_visual_device_measurement"
   Column   |            Type             | Collation | Nullable |                          Default
------------+-----------------------------+-----------+----------+-----------------------------------------------------------
 id         | integer                     |           | not null | nextval('air_visual_device_measurement_id_seq1'::regclass)
 co2        | double precision            |           |          |
 pm25_conc  | double precision            |           |          |
 pm25_aqius | double precision            |           |          |
 pm25_aqicn | double precision            |           |          |
 pm10_conc  | double precision            |           |          |
 pm10_aqius | double precision            |           |          |
 pm10_aqicn | double precision            |           |          |
 pm1_conc   | double precision            |           |          |
 pm1_aqius  | double precision            |           |          |
 pm1_aqicn  | double precision            |           |          |
 pr         | double precision            |           |          |
 hm         | double precision            |           |          |
 tp         | double precision            |           |          |
 aqius      | double precision            |           |          |
 aqicn      | double precision            |           |          |
 mainus     | character varying           |           |          |
 maincn     | character varying           |           |          |
 ts         | character varying           |           |          |
 created_at | timestamp without time zone |           | not null |
Indexes:
    "air_visual_device_measurement_pkey1" PRIMARY KEY, btree (id)
```

The application uses no other database table.

# Installation

Using Python version 3.13 or higher:

```
pip install -r requirements.txt
```

The flask application will use this common setting from file `.env`:

```
DATABASE_URI='postgresql://db_user:db_password@db_host:1234/db_database'
```

Then this command will create the database table:

```
$ python create_db_tables.py
```

And this command will run the server in development mode (as usual):

```
flask run
```

## Submitting data from IQAir's API

A script is provided to submit data, given device id, and URL of the GraphQL server (e.g. `localhost:5000`):

```
python add_air_visual_device_measurement.py https://device.iqair.com/v2/1234567890abcdef12345678 http://localhost:5000/graphql
```

The code also illustrates a GraphQL mutation to use for creating records.

## Retrieving data from the GraphQL server

A script is provided to obtain the most recent data given the URL of the GraphQL server (e.g. `localhost:5000`). This command also shows sample output:

```
$ python obtain_latest_air_visual_device_measurement.py http://localhost:5000/graphql 
{'air_visual_device_measurement': {'aqicn': 39.0, 'aqius': 71.0, 'co2': 463.0, 'created_at': '2024-12-03T06:54:46.470086', 'hm': 88.0, 'id': '75', 'maincn': 'pm10', 'mainus': 'pm25', 'pm1': {'aqicn': 16.0, 'aqius': 55.0, 'conc': 11.0}, 'pm10': {'aqicn': 39.0, 'aqius': 36.0, 'conc': 39.0}, 'pm25': {'aqicn': 29.0, 'aqius': 71.0, 'conc': 20.0}, 'pr': 102444.0, 'tp': 2.9, 'ts': '2024-12-03T14:53:41.000Z'}, 'errors': None, 'success': True}
.py https://device.iqair.com/v2/1234567890abcdef12345678 http://localhost:5000/graphql
```

The code contains a suitable GraphQL query to use.
