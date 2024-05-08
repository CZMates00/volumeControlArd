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

//--------------------------------------------------------------------------------
// ALL THINGS RELATED TO THE ENCODERS

unsigned long last_SW0 = 0, last_SW1 = 0, last_SW2 = 0; // time of the last switch press
int last_CLK0 = 0, last_CLK1 = 0, last_CLK2 = 0; // last clk state
int state_CLK0 = 0, state_CLK1 = 0, state_CLK2 = 0; // current clk state
bool EN0 = false, EN1 = false, EN2 = false; // encoder enabled = true; encoder disabled = false

//--------------------------------------------------------------------------------
// global variables
bool connected = false; // signals whether a connection with computer was initialized
bool mute_R0 = false, mute_R1 = false, mute_R2 = false; // signals the muted state
int volume0 = 0, volume1 = 0, volume2 = 0; // volume values for each encoder
bool change0 = true, change1 = true, change2 = true; // signals whether a change has occured

//--------------------------------------------------------------------------------

void setup()
{
  Serial.begin(9600); // initialization of the serial communication

  led.begin(); // initialize the leds
  ledOff(); // clear all the leds

  // encoder 0 pin initialization
  pinMode(R0_CLK, INPUT_PULLUP);
  pinMode(R0_DT, INPUT_PULLUP);
  pinMode(R0_SW, INPUT_PULLUP);
  
  // encoder 1 pin initialization
  pinMode(R1_CLK, INPUT_PULLUP);
  pinMode(R1_DT, INPUT_PULLUP);
  pinMode(R1_SW, INPUT_PULLUP);

  // encoder 2 pin initialization
  pinMode(R2_CLK, INPUT_PULLUP);
  pinMode(R2_DT, INPUT_PULLUP);
  pinMode(R2_SW, INPUT_PULLUP);

  Serial.println("READY");
}

void loop()
{
  if (!connected)
  {
    while (1) // wait for connection with the computer
    {
      String msg = Serial.readString();
      msg.trim();
      if (msg == "CONNECTED")
      {
        connected = true;
        break;
      }
    }
    while (1) // wait for the initialization data
    {
      while (Serial.peek() == -1) {} // wait until data is recieved
      String setMsg = Serial.readString();
      setMsg.trim(); // remove all whitespace characters just in case
      if (setMsg == "DONE") // signals that the initialization is done
        break;
      if (setMsg.length() == 11) // accept only the correct message lenght
      {
        // parse the data
        int enc0 = setMsg.substring(0,3).toInt();
        int enc1 = setMsg.substring(4,7).toInt();
        int enc2 = setMsg.substring(8,11).toInt();
        if (enc0 != 999)
        {
          EN0 = true;
          volume0 = enc0;
        }
        if (enc1 != 999)
        {
          EN1 = true;
          volume1 = enc1;
        }
        if (enc2 != 999)
        {
          EN2 = true;
          volume2 = enc2;
        }
      }
    }
  }

  if (!mute_R0 && change0 && EN0) // display the volume only if not in muted state, if change has occured and if the encoder is enabled
    ledSetVolume(0, volume0);
  if (!mute_R1 && change1 && EN1) // display the volume only if not in muted state, if change has occured and if the encoder is enabled
    ledSetVolume(1, volume1);
  if (!mute_R2 && change2 && EN2) // display the volume only if not in muted state, if change has occured and if the encoder is enabled
    ledSetVolume(2, volume2);

  change0 = false;
  change1 = false;
  change2 = false;
  
  if (EN0) // dont do anything if the encoder is not enabled
  {
    state_CLK0 = digitalRead(R0_CLK);
    if (state_CLK0 != last_CLK0) // the CLK pin is pulled down when a rotation occurs so the current state is different from the previous state
    {
      if (digitalRead(R0_DT) != state_CLK0) // clockwise rotation is signaled by the DT pin being in a complementary state to the CLK pin
      {
        Serial.println("0:+:0"); // send a message to increment the volume
        volume0++;
        if (volume0 > 100)
          volume0 = 100;
        change0 = true; // singnals that a change has occured
      }
      else // counter-clockwise rotation
      {
        Serial.println("0:-:0"); // send a message to decrement the volume
        volume0--;
        if (volume0 < 0)
          volume0 = 0;
        change0 = true; // signals that a change has occured
      }
    }
    last_CLK0 = state_CLK0;
  }

  if (EN1) // dont do anything if the encoder is not enabled
  {
    state_CLK1 = digitalRead(R1_CLK);
    if (state_CLK1 != last_CLK1) // the CLK pin is pulled down when a rotation occurs so the current state is different from the previous state
    {
      if (digitalRead(R1_DT) != state_CLK1) // clockwise rotation is signaled by the DT pin being in a complementary state to the CLK pin
      {
        Serial.println("1:+:0"); // send a message to increment the volume
        volume1++;
        if (volume1 > 100)
          volume1 = 100;
        change1 = true; // singnals that a change has occured
      }
      else // counter-clockwise rotation
      {
        Serial.println("1:-:0"); // send a message to decrement the volume
        volume1--;
        if (volume1 < 0)
          volume1 = 0;
        change1 = true; // signals that a change has occured
      }
    }
    last_CLK1 = state_CLK1;
  }

  if (EN2) // dont do anything if the encoder is not enabled
  {
    state_CLK2 = digitalRead(R2_CLK);
    if (state_CLK2 != last_CLK2) // the CLK pin is pulled down when a rotation occurs so the current state is different from the previous state
    {
      if (digitalRead(R2_DT) != state_CLK2) // clockwise rotation is signaled by the DT pin being in a complementary state to the CLK pin
      {
        Serial.println("2:+:0"); // send a message to increment the volume
        volume2++;
        if (volume2 > 100)
          volume2 = 100;
        change2 = true; // singnals that a change has occured
      }
      else // counter-clockwise rotation
      {
        Serial.println("2:-:0"); // send a message to decrement the volume
        volume2--;
        if (volume2 < 0)
          volume2 = 0;
        change2 = true; // signals that a change has occured
      }
    }
    last_CLK2 = state_CLK2;
  }

  int btnr0 = !digitalRead(R0_SW);
  if (btnr0 && EN0) // dont do anything if the encoder is not enabled
  {
    if (millis() - last_SW0 > DELAY) // button debounce
    {
      Serial.println("0:0:1"); // send the correct message according to the encoder
      last_SW0 = millis();
      mute_R0 = !mute_R0;
      // toggle between muted and unmuted state
      if (mute_R0)
        muted(0);
      if (!mute_R0)
      {
        ledClear(0);
        change0 = true; // signal that a change has occured
      }
    }
  }

  int btnr1 = !digitalRead(R1_SW);
  if (btnr1 && EN1) // dont do anything if the encoder is not enabled
  {
    if (millis() - last_SW1 > DELAY) // button debounce
    {
      Serial.println("1:0:1"); // send the correct message according to the encoder
      last_SW1 = millis();
      mute_R1 = !mute_R1;
      // toggle between muted and unmuted state
      if (mute_R1)
        muted(1);
      if (!mute_R1)
      {
        ledClear(1);
        change1 = true; // signal that a change has occured
      }
    }
  }

  int btnr2 = !digitalRead(R2_SW);
  if (btnr2 && EN2) // dont do anything if the encoder is not enabled
  {
    if (millis() - last_SW2 > DELAY) // button debounce
    {
      Serial.println("2:0:1"); // send the correct message according to the encoder
      last_SW2 = millis();
      mute_R2 = !mute_R2;
      // toggle between muted and unmuted state
      if (mute_R2)
        muted(2);
      if (!mute_R2)
      {
        ledClear(2);
        change2 = true; // signal that a change has occured
      }
    }
  }
}
