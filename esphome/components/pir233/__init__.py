from esphome import pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_PIN,
    CONF_ID,
    CONF_SENSITIVITY,
)
from esphome.cpp_helpers import gpio_pin_expression

CODEOWNERS = ["@Ap0ph1s-W4ite"]

CONF_PIR233_ID = "pir233_id"

pir233_component_ns = cg.esphome_ns.namespace("pir233_component")
PIR233Component = pir233_component_ns.class_("PIR233Component", cg.Component)

CONF_PERSISTENCE = "persistence"
CONF_DETECTION_INTERVAL = "detection_interval"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PIR233Component),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_DETECTION_INTERVAL, default=15): cv.int_range(min=1, max=60),
        cv.Optional(CONF_SENSITIVITY, default=1): cv.int_range(min=1, max=10),
        cv.Optional(CONF_PERSISTENCE, default=2): cv.int_range(min=1, max=10),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    pin = await gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))

    cg.add(var.set_detection_interval(config[CONF_DETECTION_INTERVAL]))
    cg.add(var.set_sensitivity(config[CONF_SENSITIVITY]))
    cg.add(var.set_persistence(config[CONF_PERSISTENCE]))
