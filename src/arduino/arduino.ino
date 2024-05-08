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

//--------------------------------------------------------------------------------
// ALL THINGS REALTED TO THE LED RINGS

// led library initialization
Adafruit_NeoPixel led = Adafruit_NeoPixel(NUM_OF_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

// "map" of diode position used in the SW (accessed with index) to actual led position on the boards
int diodes[24] = {2, 3, 4, 5, 6, 7, 0, 1,
                  10, 11, 12, 13, 14, 15, 8, 9,
                  18, 19, 20, 21, 22, 23, 16, 17};

// colors:        red, orange, yellow, green, cyan, blue, indigo, magenta, white
int colorsR[9] = {255,    255,    255,     0,    0,    0,     75,     255,   255};
int colorsG[9] = {  0,     75,    255,   128,  206,    0,      0,       0,   255};
int colorsB[9] = {  0,      0,      0,     0,  209,  255,    130,     255,   255};

// turn off all the connected leds
void ledOff()
{
  for (int i = 0; i < NUM_OF_LEDS; i++)
  {
    led.setPixelColor(i, led.Color(0, 0, 0));
  }
  led.show();
}

// turns on the specified rings led to brightness
// if LOW_BRIGHTNESS is used, the led shines white else the led shines with a color from the colors array
void ledSet(int ring, int from, int to, int brightness)
{
  if (ring > 2 || ring < 0 || from > 7 || from < 0 || to > 7 || to < 0 || from > to)
    return; // invalid input handling - not necessary
  
  int rfrom = 0, rto = 0;
  int ringOffset = 2;

  // because the leds are chained together, the number must be incremented by the number of leds on the previous ring
  rfrom = ring*8 + from;
  rto = ring*8 + to;
  
  for (int i = rfrom; i < rto+1; i++)
  {
    if (brightness == LOW_BRIGHTNESS)
      led.setPixelColor(diodes[i], led.Color(brightness*colorsR[8]/MAX_BRIGHTNESS, brightness*colorsG[8]/MAX_BRIGHTNESS, brightness*colorsB[8]/MAX_BRIGHTNESS));
    else
      led.setPixelColor(diodes[i], led.Color(brightness*colorsR[i%8]/MAX_BRIGHTNESS, brightness*colorsG[i%8]/MAX_BRIGHTNESS, brightness*colorsB[i%8]/MAX_BRIGHTNESS));
  }
  led.show();
}

// set all leds on specified ring to red to indicate muted state
void muted(int ring)
{
  for (int i = 8*ring; i < 8*(ring+1); i++)
  {
    led.setPixelColor(diodes[i], led.Color(LOW_BRIGHTNESS*colorsR[0]/MAX_BRIGHTNESS, LOW_BRIGHTNESS*colorsG[0]/MAX_BRIGHTNESS, LOW_BRIGHTNESS*colorsB[0]/MAX_BRIGHTNESS));
  }
  led.show();
}

// turn off specified rings leds
void ledClear(int ring)
{
  for (int i = 8*ring; i < 8*(ring+1); i++)
  {
    led.setPixelColor(diodes[i], led.Color(0,0,0));
  }
  led.show();
}

// set leds accoring to the volume level on specified ring
void ledSetVolume(int ring, int volume)
{
  ledClear(ring);
  if (volume > 0 && volume <= 6)
  {
    ledSet(ring, 0, 0, LOW_BRIGHTNESS);
  }
  if (volume > 6 && volume <= 12)
  {
    ledSet(ring, 0, 0, HIGH_BRIGHTNESS);
  }
  if (volume > 12 && volume <= 18)
  {
    ledSet(ring, 0, 0, HIGH_BRIGHTNESS);
    ledSet(ring, 1, 1, LOW_BRIGHTNESS);
  }
  if (volume > 18 && volume <= 24)
  {
    ledSet(ring, 0, 1, HIGH_BRIGHTNESS);
  }
  if (volume > 24 && volume <= 30)
  {
    ledSet(ring, 0, 1, HIGH_BRIGHTNESS);
    ledSet(ring, 2, 2, LOW_BRIGHTNESS);
  }
  if (volume > 30 && volume <= 36)
  {
    ledSet(ring, 0, 2, HIGH_BRIGHTNESS);
  }
  if (volume > 36 && volume <= 42)
  {
    ledSet(ring, 0, 2, HIGH_BRIGHTNESS);
    ledSet(ring, 3, 3, LOW_BRIGHTNESS);
  }
  if (volume > 42 && volume <= 48)
  {
    ledSet(ring, 0, 3, HIGH_BRIGHTNESS);
  }
  if (volume > 48 && volume <= 54)
  {
    ledSet(ring, 0, 3, HIGH_BRIGHTNESS);
    ledSet(ring, 4, 4, LOW_BRIGHTNESS);
  }
  if (volume > 54 && volume <= 60)
  {
    ledSet(ring, 0, 4, HIGH_BRIGHTNESS);
  }
  if (volume > 60 && volume <= 66)
  {
    ledSet(ring, 0, 4, HIGH_BRIGHTNESS);
    ledSet(ring, 5, 5, LOW_BRIGHTNESS);
  }
  if (volume > 66 && volume <= 72)
  {
    ledSet(ring, 0, 5, HIGH_BRIGHTNESS);
  }
  if (volume > 72 && volume <= 78)
  {
    ledSet(ring, 0, 5, HIGH_BRIGHTNESS);
    ledSet(ring, 6, 6, LOW_BRIGHTNESS);
  }
  if (volume > 78 && volume <= 84)
  {
    ledSet(ring, 0, 6, HIGH_BRIGHTNESS);
  }
  if (volume > 84 && volume <= 90)
  {
    ledSet(ring, 0, 6, HIGH_BRIGHTNESS);
    ledSet(ring, 7, 7, LOW_BRIGHTNESS);
  }
  if (volume > 90 && volume <= 96)
  {
    ledSet(ring, 0, 7, HIGH_BRIGHTNESS);
  }
  if (volume > 96 && volume <= 100)
  {
    ledSet(ring, 0, 7, HIGH_BRIGHTNESS);
  }
}

void setup() {

}

void loop() {

}
