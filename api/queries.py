from .models import AirVisualDeviceMeasurement
from ariadne import convert_kwargs_to_snake_case
from sqlalchemy import text

def listAirVisualDeviceMeasurements_resolver(obj, info):
    try:
        air_visual_device_measurements = [air_visual_device_measurement.to_dict() for air_visual_device_measurement in AirVisualDeviceMeasurement.query.all()]
        payload = {
            "success": True,
            "air_visual_device_measurements": air_visual_device_measurements
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def getLatestAirVisualDeviceMeasurement_resolver(obj, info):
    try:
        print(str(info))
        air_visual_device_measurement = AirVisualDeviceMeasurement.query.order_by(text('id desc')).limit(1).first()
        payload = {
            "success": True,
            "air_visual_device_measurement": air_visual_device_measurement.to_dict()
        }

    except Exception as err :
        payload = {
            "success": False,
            "errors": [f"Error: {err}"]
        }

    return payload
@convert_kwargs_to_snake_case
def getAirVisualDeviceMeasurement_resolver(obj, info, id):
    try:
        air_visual_device_measurement = AirVisualDeviceMeasurement.query.get(id)
        payload = {
            "success": True,
            "air_visual_device_measurement": air_visual_device_measurement.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {id} not found"]
        }

    return payload
