import machine
import neopixel
import time
from machine import Pin, I2C, ADC
import ssd1306

NUM_LEDS = 12
PIN_NUM = 13
BRIGHTNESS = 0.2

def apply_brightness(color):
    r, g, b = color
    return (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))

led_ring = neopixel.NeoPixel(machine.Pin(PIN_NUM), NUM_LEDS)

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

buzzer = Pin(22, Pin.OUT)

pot = ADC(2)

big_button = Pin(12, Pin.IN, Pin.PULL_UP)

def get_time_from_pot(min_val, max_val):
    raw = pot.read_u16()
    minutes = round(min_val + (raw / 65535) * (max_val - min_val))
    minutes = max(min_val, min(max_val, minutes))
    return minutes

def wait_for_button_press():
    while big_button.value() == 1:
        time.sleep(0.05)
    while big_button.value() == 0:
        time.sleep(0.01)

def show_time_select(title, minutes):
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text("{} min".format(minutes), 0, 16)
    oled.text("Press to confirm", 0, 40)
    oled.show()

def show_timer(title, minutes, seconds):
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text("{:02d}:{:02d}".format(minutes, seconds), 0, 16)
    oled.show()

def show_pause_icon():
    oled.fill(0)
    oled.text("PAUSED", 0, 0)
    x = 54
    y = 24
    w = 6
    h = 24
    gap = 6
    oled.fill_rect(x, y, w, h, 1)
    oled.fill_rect(x + w + gap, y, w, h, 1)
    oled.show()


def cool_colour_pattern(np, delay=0.05, t_override=None):
    t = time.ticks_ms() // 10 if t_override is None else t_override
    for i in range(NUM_LEDS):
        phase = (t + i * 20) % 200
        if phase < 100:
            frac = phase / 100
        else:
            frac = (200 - phase) / 100
        g = int(255 * (1 - frac))
        b = int(255 * frac)
        np[i] = apply_brightness((0, g, b))
    np.write()
    time.sleep(delay)

def quiet_beep(duration=0.05):
    buzzer.value(1)
    time.sleep(duration)
    buzzer.value(0)

def run_timer(duration_sec, title, break_mode=False):
    start_time = time.time()
    end_time = start_time + duration_sec
    paused = False
    pause_time = 0

    while True:
        if not paused:
            now = time.time()
            remaining = int(end_time - now)
            if remaining < 0:
                break
            minutes = remaining // 60
            seconds = remaining % 60
            show_timer(title, minutes, seconds)
            if break_mode:
                elapsed = duration_sec - (end_time - now)
                led_float = NUM_LEDS * (1 - elapsed / duration_sec)
                for i in range(NUM_LEDS):
                    if i < int(led_float):
                        np[i] = apply_brightness((128, 0, 128))
                    elif i == int(led_float):
                        frac_led = led_float - int(led_float)
                        brightness = int(128 * frac_led)
                        np[i] = apply_brightness((brightness, 0, brightness))
                    else:
                        np[i] = (0, 0, 0)
                np.write()
            else:
                elapsed = duration_sec - (end_time - now)
                led_float = NUM_LEDS * (1 - elapsed / duration_sec)
                t = int(time.ticks_ms() // 10)
                for i in range(NUM_LEDS):
                    if i < int(led_float):
                        phase = (t + i * 20) % 200
                        if phase < 100:
                            frac = phase / 100
                        else:
                            frac = (200 - phase) / 100
                        g = int(255 * (1 - frac))
                        b = int(255 * frac)
                        np[i] = apply_brightness((0, g, b))
                    elif i == int(led_float):
                        frac_led = led_float - int(led_float)
                        brightness = int(255 * frac_led)
                        phase = (t + i * 20) % 200
                        if phase < 100:
                            frac = phase / 100
                        else:
                            frac = (200 - phase) / 100
                        g = int(brightness * (1 - frac))
                        b = int(brightness * frac)
                        np[i] = apply_brightness((0, g, b))
                    else:
                        np[i] = (0, 0, 0)
                np.write()
            time.sleep(0.05)
            if button.value() == 0:
                pause_time = time.time()
                paused = True
                show_pause_icon()
                np.fill((0, 0, 0))
                np.write()
                quiet_beep(0.03)
        else:
            while button.value() == 0:
                time.sleep(0.01)
            while button.value() == 1:
                time.sleep(0.01)
            end_time += time.time() - pause_time
            paused = False
            quiet_beep(0.03)

    quiet_beep(0.08)
    np.fill((0, 0, 0))
    np.write()

def rainbow_bootup(np, buzzer):
    np.fill((0, 0, 0))
    np.write()
    quiet_beep(0.05)
    for j in range(NUM_LEDS * 4):
        for i in range(NUM_LEDS):
            color = wheel((int(i * 256 / NUM_LEDS) + j * 8) % 256)
            np[i] = apply_brightness(color)
        np.write()
        time.sleep(0.05)
    for fade in range(255, -1, -15):
        for i in range(NUM_LEDS):
            r, g, b = np[i]
            np[i] = (int(r * fade // 255), int(g * fade // 255), int(b * fade // 255))
        np.write()
        time.sleep(0.03)
    np.fill((0, 0, 0))
    np.write()

def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

rainbow_bootup(np, buzzer)

while True:
    while True:
        work_time = get_time_from_pot(5, 60)
        show_time_select("Set WORK time", work_time)
        cool_colour_pattern(np, delay=0.05)
        if button.value() == 0:
            wait_for_button_press()
            break

    while True:
        break_time = get_time_from_pot(1, 30)
        show_time_select("Set BREAK time", break_time)
        cool_colour_pattern(np, delay=0.05)
        if button.value() == 0:
            wait_for_button_press()
            break

    while True:
        oled.fill(0)
        oled.text("Ready for WORK?", 0, 0)
        oled.text("Press to start", 0, 16)
        oled.show()
        while button.value() == 1:
            cool_colour_pattern(np, delay=0.05)
        wait_for_button_press()
        run_timer(work_time * 60, "Work", break_mode=False)

        oled.fill(0)
        oled.text("Ready for BREAK?", 0, 0)
        oled.text("Press to start", 0, 16)
        oled.show()
        while button.value() == 1:
            cool_colour_pattern(np, delay=0.05)
        wait_for_button_press()
        run_timer(break_time * 60, "Break", break_mode=True)