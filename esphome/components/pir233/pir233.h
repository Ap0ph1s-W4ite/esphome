#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/core/gpio.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace pir233 {

static const uint32_t VALIDATION_MASK = 0x30001;
static const uint32_t EXPECTED_VALID_MASK = 0x20000;

class PIR233Component : public Component, public binary_sensor::BinarySensor {
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

  uint8_t read_bit_pattern_();
  uint32_t motion_data_();
  bool validate_data_(uint32_t data);

  bool validation_result_{false};

  GPIOPin *pin_;
};

}  // namespace pir233
}  // namespace esphome