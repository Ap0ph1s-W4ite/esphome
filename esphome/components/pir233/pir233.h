#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace pir233 {

static const uint16_t FIRST_TWO_BITS = 0x8000;
static const uint16_t LAST_BIT = 0x0000;

class PIR233Component : public Component, public BinarySensor {
 public:
  void set_pin(GPIOPin *pin) { pin_ = pin; }
  void set_detection_interval(uint8_t detection_interval) { detection_interval_ = detection_interval; }
  void set_sensitivity(uint8_t sensitivity) { sensitivity_ = sensitivity; }
  void set_persistence(uint8_t persistence) { persistence_ = persistence; }

  void setup() override;
  void dump_config() override;
  void loop() override;

 protected:
  uint8_t detection_interval_{15};
  uint8_t sensitivity_{1};
  uint8_t persistence_{2};

  uint16_t read_bit_pattern_();

  GPIOPin *pin_;
};

}  // namespace pir233
}  // namespace esphome