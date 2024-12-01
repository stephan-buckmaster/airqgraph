from datetime import date

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import AirvisualDeviceMeasurement

def set_attr_from_subfield(target, name):
    if name not in target:
        return
    prefix = name.replace('_', '')
    subfield = target.pop(name)
    target[prefix + '_conc'] = subfield.get('conc')
    target[prefix + '_aqius'] = subfield.get('aqius')
    target[prefix + '_aqicn'] = subfield.get('aqicn')

# Todo : add authentication
@convert_kwargs_to_snake_case
def create_airvisual_device_measurement_resolver(_, info, input: dict):
    try:
        input['co2'] = input.pop('co_2') # undo what the snake_case_fallback_resolvers does
        set_attr_from_subfield(input, 'pm_25')
        set_attr_from_subfield(input, 'pm_10')
        set_attr_from_subfield(input, 'pm_1')
        air_visual_device_measurement = AirvisualDeviceMeasurement(**input)
        air_visual_device_measurement.created_at = db.func.now()
        db.session.add(air_visual_device_measurement)
        db.session.commit()
        payload = {
            "success": True,
            "airvisual_device_measurement": air_visual_device_measurement.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload
