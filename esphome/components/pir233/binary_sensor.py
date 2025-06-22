import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_MOTION, DEVICE_CLASS_MOTION, ICON_MOTION_SENSOR

from . import PIR233Component, CONF_PIR233_ID

DEPENDENCIES = ["pir233"]

CONFIG_SCHEMA = {
    cv.GenerateID(): cv.use_id(PIR233Component),
    cv.Optional(CONF_MOTION): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_MOTION, icon=ICON_MOTION_SENSOR
    ),
}


async def to_code(config):
    pir233_component = await cg.get_variable(config[CONF_PIR233_ID])
    if CONF_MOTION in config:
        motion = await binary_sensor.new_binary_sensor(config[CONF_MOTION])
        cg.add(pir233_component.set_motion_binary_sensor(motion))
