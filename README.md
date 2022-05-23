# Argus Controller Pico

Read your SFFPC watercooling loop temperature without a thermal sensor connector

> Have you build a small form factor PC with a custom watercooling loop? 
> Have you added a temperature sensor for your liquid only to find out that your mITX mainboard doesn't have the necessary connection?
> Have you wondered if there isn't another way?

There is! Argus Monitor is an excellent solution for controlling your fans based on any temperature and state of your system. That alone is cool and makes for much better fan control in small systems, but what makes it exceptional is the support for reading custom controllers. They also provide some basic instructions for Arduino, but their setup is a bit bulky for SFFPCs. 

Small content warning, lots of technical terms ahead. Feel free to glance over the details.

Meet the Raspberry Pi Pico! A tiny microcontroller board which has it all:

1. a Micro-USB port which can be used to attach it to an internal USB port and used as a COM device in Windows.
2. a small LED (no RGB though)
3. a built-in temperature sensor for reference
4. three analog input pins

The latter is what we need for our project. Most liquid temperature sensors which can be added to your watercooling loop are all things considered and speaking in electronical terms just simple thermistors with 10k Ohm resistance at 25°. This is great. We can use an analog input on the Pico to compare the actual thermistor value against a resistor and therefore read the actual loop temperature with the Pico and send the value to Argus Monitor through USB.

## What you'll need

1. A Raspberry Pi Pico
2. Some pin headers (L shaped ones work best)
3. 10K Ohm resistors (one per sensor)
4. Heatshrink
5. Soldering iron and solder 
6. An internal USB-Header plug to Micro-USB plug cable

## Building the controller

Make yourself familiar with the [Raspberry Pi Pico Pinout](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf). 

For a single sensor and to use the code from this repository as it is, find pins 32 (ADC1), 33 (AGND) and 36 (3V3 OUT). 

Solder L shaped pin headers to backs of pin 32 and 33, pointing the connecting side inwards. 
Solder a 10K Ohm resistor on to pin 36 connecting it pin 32 as well. 

Make sure the leads of the resistor do not touch pin 33. Just bend it a bit out of the way, making sure the bare metal parts do not touch any other bare metal parts on the board.

TODO: Add diagram and pictures here.

Wrap up the whole Pico in shrink wrap, cut the pin headers free afterwards. 

Connect the Pico to your PC using a Micro-USB cable, holding down the RESET button on the Pico while you do so. It doesn't have to be an internal one for testing everything, but once everything works you should consider getting one that attaches to the internal USB headers on your mainboard.

Connect your temperature sensor leads to the two pins.

## Software setup

1. Install [CircuitPython] on the Pico following the official instructions
2. This will make the Pico show up as a new USB drive on your PC.
3. Drag all files ending in .py from this repository to the drive created by the Pico

The code in this repository contains a debug function: If you attach the Pico to USB without the temperature sensor connected, it will show the USB drive with the code. If connect the sensor and restart the Pico, the drive will be hidden.

## Argus Monitor setup

Figure out COM ports. Use the Windows device manager. In most cases COM5 will be what you're looking for. COM4 is used to connect a serial Terminal to the Pico to run code and debug things. If you had COM4 and COM5 before plugging in the Pico, you probably know more about this than I do.

Enter "5" into the field in the Argus Monitor settings. 

TODO: add further instructions






