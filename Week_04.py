from machine import Pin
import time

led = machine.Pin(2, machine.Pin.OUT)  # GPIO 2


def blink_led(pin, value):
    if value == 1:
        pin.on()
    else:
        pin.off()


if __name__ == '__main__':
    for i in range(10):
        blink_led(led, 1)
        time.sleep(0.5)
        blink_led(led, 0)
        time.sleep(0.5)
