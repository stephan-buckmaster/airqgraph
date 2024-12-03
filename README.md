# Air Quality Monitoring Server

This project comprises a GraphQL server that creates records in a PostgreSQL database and allows retrieving the latest air quality data from the measurements recorded by an [IQAir](https://www.iqair.com) device

This is the origin of the data behind this API. So this API allows submitting data obtained from their API, and then retrieving it for further processing, e.g. display.

The device id used in the API requests would only be known to the owner. So this API allows such owners to publish the data recorded by their device.

# Sample Request to the manufacturer's API

The manufacturer provides access to the measurements through a JSON API by device id. The device id used would only be known to the owner. They can find this device id by logging into their account and navigating to their device page. On the right will be a list of API links.

![Screenshot of IQAir Device Page](images/iqair-device-page.png?raw=true "Screenshot of IQAir Device Page")


For example this curl command can be used to obtain the JSON of the measurements:

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

Project Setup
Environment Variables
Ensure to configure the following environment variables for database access and other configurations:

DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
Database Schema
The database uses the following schema:

sql

Copy code
CREATE TABLE air_quality_records (
  id SERIAL PRIMARY KEY,
  co2 INTEGER,
  pm25_conc INTEGER,
  pm25_aqius INTEGER,
  pm25_aqicn INTEGER,
  pm10_conc INTEGER,
  pm10_aqius INTEGER,
  pm10_aqicn INTEGER,
  pm1_conc INTEGER,
  pm1_aqius INTEGER,
  pm1_aqicn INTEGER,
  pr INTEGER,
  hm INTEGER,
  tp FLOAT,
  ts TIMESTAMP,
  mainus VARCHAR(10),
  maincn VARCHAR(10),
  aqius INTEGER,
  aqicn INTEGER
);
GraphQL Endpoints
Mutations
createRecord(input: AirQualityInput): AirQualityRecord
Queries
latestRecord: AirQualityRecord
Running the Server
To start the server, run:

sh

Copy code
npm install
npm start
Ensure that the PostgreSQL database is running and accessible with the provided environment variables.

Testing
Tests are written using Jest and Supertest. To run the tests, execute:

sh

Copy code
npm test


