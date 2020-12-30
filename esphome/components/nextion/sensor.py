import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_COMPONENT_ID,
    CONF_PAGE_ID,
    CONF_ID,
    UNIT_EMPTY,
    ICON_EMPTY,
)
from . import nextion_ns, CONF_NEXTION_ID
from .display import Nextion
from .defines import CONF_VARIABLE_ID

DEPENDENCIES = ["display"]

NextionSensor = nextion_ns.class_("NextionSensor", sensor.Sensor, cg.PollingComponent)

CONFIG_SCHEMA = (
    sensor.sensor_schema(UNIT_EMPTY, ICON_EMPTY, 2)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NextionSensor),
            cv.GenerateID(CONF_NEXTION_ID): cv.use_id(Nextion),
            cv.Optional(CONF_PAGE_ID): cv.uint8_t,
            cv.Optional(CONF_COMPONENT_ID): cv.uint8_t,
            cv.Optional(CONF_VARIABLE_ID): cv.string,
        }
    )
    .extend(cv.polling_component_schema("60s"))
)


def to_code(config):
    if (
        not config.keys() >= {CONF_COMPONENT_ID, CONF_PAGE_ID}
        and CONF_VARIABLE_ID not in config
    ):
        raise cv.Invalid(
            "At least {CONF_COMPONENT_ID} and {CONF_PAGE_ID} or {CONF_VARIABLE_ID} needs to be set\n"
            + "{CONF_COMPONENT_ID} & {CONF_PAGE_ID} is used on data coming from the Nextion\n"
            + ", if you arent sending from the nextion this can be skipped\n"
            + "{CONF_VARIABLE_ID} is used to get/poll the data from the nextion"
        )

    # if CONFIG_RESTORE_FROM_NEXTION in config and config[CONFIG_RESTORE_FROM_NEXTION]:
    #     if CONF_VARIABLE_ID not in config:
    #         raise cv.Invalid(
    #             "{CONF_VARIABLE_ID} is required if {CONFIG_RESTORE_FROM_NEXTION} is set"
    #         )
    hub = yield cg.get_variable(config[CONF_NEXTION_ID])
    var = cg.new_Pvariable(config[CONF_ID], hub)
    yield cg.register_component(var, config)
    yield sensor.register_sensor(var, config)

    cg.add(hub.register_sensor_component(var))

    if CONF_COMPONENT_ID in config:
        cg.add(var.set_component_id(config[CONF_COMPONENT_ID]))
    else:
        cg.add(var.set_component_id(-1))

    if CONF_PAGE_ID in config:
        cg.add(var.set_page_id(config[CONF_PAGE_ID]))
    else:
        cg.add(var.set_page_id(-1))

    if CONF_VARIABLE_ID in config:
        cg.add(var.set_variable_id(config[CONF_VARIABLE_ID]))
