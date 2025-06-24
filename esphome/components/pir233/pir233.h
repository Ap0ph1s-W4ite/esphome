#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace pir233 {

static const uint8_t FIRST_TWO_BITS = 0x8000;
static const uint8_t LAST_BIT = 0x0000;

class PIR233Component : public Component, public BinarySensor {
 public:
  void set_pin(GPIOPin *pin) { pin_ = pin; }

  void setup() override;
  void dump_config() override;
  void loop() override;

 protected:
};

}  // namespace pir233
}  // namespace esphome