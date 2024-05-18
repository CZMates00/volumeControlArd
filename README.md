# PC volume control with Arduino

The aim of this project is to create a Arduino-powered controller used for controlling computer volume (either the default audio output or selected apps).

## Hardware needed

- Arduino Nano
- 3x rotary encoder such as the KY-040
- 3x Adafruit NeoPixel 8-ledRing
- soldering iron, wires
- time :)

## Computer app

Download the python [files](https://github.com/CZMates00/volumeControlArd/tree/main/src/App), install pycaw, pyserial, comtypes python modules and run the main.py file. The setup wizard will then walk you through all the steps to get the app running.

## Arduino app

Download the [arduino.ino](https://github.com/CZMates00/volumeControlArd/tree/main/src/arduino) sketch file, install the official Adafruit NeoPixel library and upload the file to your Arduino.

## Printable case

To accomodate 3 rotary encoders and 3 led rings, there is a 3D printable case, which can be found [here](https://www.printables.com/cs/model/873823-pc-audio-controller-with-arduino).


