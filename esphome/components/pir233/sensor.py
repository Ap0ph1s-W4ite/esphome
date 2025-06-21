from esphome import pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
    UNIT_EMPTY,
    CONF_PIN,
    CONF_ID,
    CONF_SENSITIVITY,
)
from esphome.cpp_helpers import gpio_pin_expression

pir233_component_ns = cg.esphome_ns.namespace("pir233_component")
PIR233Component = pir233_component_ns.class_("PIR233Component", cg.Component)

CONF_PERSISTENCE = "persistence"
CONF_DETECTION_INTERVAL = "detection_interval"
ICON_DETECTION_INTERVAL = "mdi:timer"
ICON_SENSITIVITY = "mdi:tune"
ICON_PERSISTENCE = "mdi:timer-sand"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PIR233Component),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
    }
    # TODO: Look if necessary to have cv.COMPONENT_SCHEMA here
    # TODO: Add the default, min and max values for the parameters. Look into the example ./esphome/components/bp1658cj/__init__.py 
).extend(
    {
        cv.Optional(CONF_DETECTION_INTERVAL): number.number_schema(
            PIR233Component,
            unit_of_measurement="s",
            entity_category=ENTITY_CATEGORY_CONFIG,
            icon=ICON_DETECTION_INTERVAL,
        ),
        cv.Optional(CONF_SENSITIVITY): number.number_schema(
            PIR233Component,
            unit_of_measurement=UNIT_EMPTY,
            entity_category=ENTITY_CATEGORY_CONFIG,
            icon=ICON_SENSITIVITY,
        ),
        cv.Optional(CONF_PERSISTENCE): number.number_schema(
            PIR233Component,
            unit_of_measurement=UNIT_EMPTY,
            entity_category=ENTITY_CATEGORY_CONFIG,
            icon=ICON_PERSISTENCE,
        ),
    }
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))
    if detection_interval := config.get(CONF_DETECTION_INTERVAL):
        delta = await number.new_number(detection_interval, min_value=1, max_value=60, step=1)
        await cg.register_parented(delta, var)
        cg.add(var.set_detection_interval(delta))
    if sensitivity := config.get(CONF_SENSITIVITY):
        delta = await number.new_number(sensitivity, min_value=1, max_value=10, step=1)
        await cg.register_parented(delta, var)
        cg.add(var.set_sensitivity(delta))
    if persistence := config.get(CONF_PERSISTENCE):
        delta = await number.new_number(persistence, min_value=1, max_value=60, step=1)
        await cg.register_parented(delta, var)
        cg.add(var.set_persistence(delta))
