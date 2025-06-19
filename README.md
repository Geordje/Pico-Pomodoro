# Pomodoro Timer (for Raspberry Pi Pico)

## What is this?

This is a fun, simple Pomodoro timer you can build with a Raspberry Pi Pico, a ring of NeoPixel LEDs, a buzzer, a potentiometer (knob), a button, and an SSD1306 OLED display. It helps you focus by timing your work and break sessions, with colorful lights and a little beep to keep you on track.

## Features

- **Set your own work and break times** using the knob (potentiometer)
- **Big friendly button** to start, pause, and confirm things
- **Colorful LED ring** shows your progress
- **OLED screen** displays what’s happening and how much time is left
- **Buzzer** gives a little beep when it’s time to switch
- **Pause and resume** your timer if you need a break

## How to wire it up

- **NeoPixel Ring**: Data pin to GP13 (physical pin 17), power to 3V3, ground to GND
- **Potentiometer**: Middle pin to GP28 (ADC2, physical pin 34), sides to 3V3 and GND
- **Button**: One side to GP12 (physical pin 16), other side to GND
- **Buzzer**: Positive to GP22 (physical pin 29), negative to GND
- **OLED Display (SSD1306, I2C)**: SDA to GP16 (pin 21), SCL to GP17 (pin 22), VCC to 3V3, GND to GND
> [Wokwi Diagram with all components!](https://wokwi.com/projects/434216732358817793)  
> **Tip:** Double-check your Pico pinout!  
> [Pico pinout diagram](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)

## How to flash the code

1. **Open a Python IDE of your choice, eg Thonny, VSCode, etc.** For this short guide, I will describe using Thonny.
2. **Download MicroPython firmware** for the Pico from [here](https://micropython.org/download/rp2-pico/).
3. **Hold the BOOTSEL button** on your Pico and plug it into your computer.
4. **Copy the MicroPython .uf2 file** to the new USB drive that appears.
5. **Restart the Pico** (unplug and plug back in).
6. **Open Thonny**, select the Pico as your interpreter.
7. **Copy the `main.py` code** from this repo into Thonny and save it as `main.py` on the Pico.
8. **Reboot the Pico** and you’re good to go!

## How to use

1. **Turn the knob** to set your work time, then press the button.
2. **Turn the knob** to set your break time, then press the button.
3. **Press the button** to start your work session.
4. **Watch the lights and screen** as you work. The buzzer will beep when time’s up!
5. **Press the button** to start your break, and repeat.

## Notes

- If you want to pause, just press the button during a session.
- The timer and lights will reset after each session.
- You can tweak the code to change colors, times, or add more features!

---

**Happy focusing!**
