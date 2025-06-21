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
        cv.Required(CONF_PIN): pins.gpio_pin_schema,
        cv.Optional(CONF_DETECTION_INTERVAL, default=15): number.NUMBER_SCHEMA.extend(
            icon=ICON_DETECTION_INTERVAL,
            unit_of_measurement="s",
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_SENSITIVITY, default=3): number.NUMBER_SCHEMA.extend(
            icon=ICON_SENSITIVITY,
            unit_of_measurement=UNIT_EMPTY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_PERSISTENCE, default=1): number.NUMBER_SCHEMA.extend(
            icon=ICON_PERSISTENCE,
            unit_of_measurement=UNIT_EMPTY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))
    sensitivity = await number.new_number(
        config[CONF_SENSITIVITY], min_value=1, max_value=10, step=1
    )
    await cg.register_parented(sensitivity, var)
    cg.add(var.set_sensitivity(sensitivity))
    persistence = await number.new_number(
        config[CONF_PERSISTENCE], min_value=1, max_value=10, step=1
    )
    await cg.register_parented(persistence, var)
    cg.add(var.set_persistence(persistence))
    detection_interval = await number.new_number(
        config[CONF_DETECTION_INTERVAL], min_value=1, max_value=60, step=1
    )
    await cg.register_parented(detection_interval, var)
    cg.add(var.set_detection_interval(detection_interval))
