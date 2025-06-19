from esphome import pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
    UNIT_EMPTY,
    CONF_PIN,
    CONF_INITIAL_VALUE,
    CONF_MIN_VALUE,
    CONF_MAX_VALUE,
    CONF_ID,
    CONF_SENSITIVITY,
)
from esphome.cpp_helpers import gpio_pin_expression

pir233_component_ns = cg.esphome_ns.namespace("pir233_component")
PIR233Component = pir233_component_ns.class_("PIR233Component", cg.Component)
PIR233Gain = pir233_component_ns.class_("PIR233Gain", cg.Component)
PIR233Persistence = pir233_component_ns.class_("PIR233Persistence", cg.Component)

CONF_PERSISTENCE = "persistence"
ICON_SENSITIVITY = "mdi:tune"
ICON_PERSISTENCE = "mdi:timer-sand"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PIR233Component),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_SENSITIVITY, default=3): number.number_schema(
            PIR233Gain,
            icon=ICON_SENSITIVITY,
            unit_of_measurement=UNIT_EMPTY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_PERSISTENCE, default=1): number.number_schema(
            PIR233Persistence,
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
