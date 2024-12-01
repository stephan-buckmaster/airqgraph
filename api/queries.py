from .models import AirvisualDeviceMeasurement
from ariadne import convert_kwargs_to_snake_case

def listAirvisualDeviceMeasurements_resolver(obj, info):
    try:
        airvisual_device_measurements = [airvisual_device_measurement.to_dict() for airvisual_device_measurement in AirvisualDeviceMeasurement.query.all()]
        payload = {
            "success": True,
            "airvisual_device_measurements": airvisual_device_measurements
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def getAirvisualDeviceMeasurement_resolver(obj, info, id):
    try:
        airvisual_device_measurement = AirvisualDeviceMeasurement.query.get(id)
        payload = {
            "success": True,
            "airvisual_device_measurement": airvisual_device_measurement.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {id} not found"]
        }

    return payload
