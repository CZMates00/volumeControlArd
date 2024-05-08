// library for one-wire led ring control
#include <Adafruit_NeoPixel.h>

//--------------------------------------------------------------------------------

// all of the led rings are chained together using DI and DO pins and thus controlled by just one wire
#define LED_PIN 9
#define NUM_OF_LEDS 24
#define MAX_BRIGHTNESS 255 // brightness on a scale 0-255
#define LOW_BRIGHTNESS 2
#define HIGH_BRIGHTNESS 5

// rotary encoder 0 (left)
#define R0_CLK 2 // pin A
#define R0_DT 5 // pin B
#define R0_SW 7 // pin 4

// rotary encoder 1 (middle)
#define R1_CLK 3 // pin A
#define R1_DT 6 // pin B
#define R1_SW 8 // pin 4

// rotary encoder 2 (right)
#define R2_CLK 4 // pin A
#define R2_DT 10 // pin B
#define R2_SW 12 // pin 4

#define DELAY 500 // push button delay

void setup() {

}

void loop() {

}
