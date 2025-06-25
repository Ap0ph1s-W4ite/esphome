#include "esphome/core/log.h"
#include "pir233.h"

namespace esphome {
namespace pir233 {

static const char *const TAG = "pir233";

uint8_t PIR233Component::read_bit_pattern_() {
  this->pin_->pin_mode(gpio::FLAG_OUTPUT);
  this->pin_->digital_write(false);
  delayMicroseconds(4);
  this->pin_->digital_write(true);
  delayMicroseconds(4);
  this->pin_->pin_mode(gpio::FLAG_INPUT);
  delayMicroseconds(5);
  int value = this->pin_->digital_read();

  delayMicroseconds(4);
  return value;
}

uint32_t PIR233Component::motion_data_() {
  uint32_t data = 0;
  for (int i = 0; i < 20; i++) {
    data <<= 1;
    data |= this->read_bit_pattern_();
  }
  return data;
}

bool PIR233Component::validate_data_(uint32_t data) {
  if ((data & VALIDATION_MASK) == EXPECTED_VALID_MASK) {
    return true;
  } else {
    return false;
  }
}

void PIR233Component::setup() {
  ESP_LOGCONFIG(TAG, "Setting up PIR233 Component");
  uint32_t data = this->motion_data_();
  bool is_valid = this->validate_data_(data);

  uint8_t first_bit = (data >> 19) & 0x01;
  uint8_t second_bit = (data >> 18) & 0x01;
  uint8_t last_bit = data & 0x01;

  // TODO: Repeat one more time if the result is not valid
  if (is_valid) {
    ESP_LOGD(TAG, "PIR233 sensor is working correctly. First bits: %d%d, Last bit: %d", first_bit, second_bit,
             last_bit);
  } else {
    ESP_LOGE(TAG, "PIR233 sensor validation failed. First bits: %d%d, Last bit: %d. Check wiring or sensor status.",
             first_bit, second_bit, last_bit);
  }
}

void PIR233Component::dump_config() {
  ESP_LOGCONFIG(TAG, "PIR233:");
  LOG_BINARY_SENSOR("  ", "Motion Detected", this);
}

void PIR233Component::loop() {
  // This is where you would handle the PIR sensor logic.
  // For example, you might read from a GPIO pin to check for motion.
  // If motion is detected, you can call this->publish_state(true);
  // and if no motion is detected, call this->publish_state(false);
}

}  // namespace pir233
}  // namespace esphome