from machine import Pin
from time import sleep

# 初始化LED pin
pins = {
    "white": Pin(0, Pin.OUT),
    "red": Pin(14, Pin.OUT),
    "green": Pin(12, Pin.OUT),
    "blue": Pin(13, Pin.OUT)
}


# 通用函數來控制LED
def control_led(led_pin, status):
    led_pin.value(status)


if __name__ == '__main__':
    white_status = False
    rgb_status = True
    while True:
        # 切換LED狀態
        white_status ^= True
        rgb_status ^= True

        control_led(pins["white"], white_status)
        control_led(pins["red"], rgb_status)
        control_led(pins["green"], rgb_status)
        control_led(pins["blue"], rgb_status)
        sleep(1)
        control_led(pins["white"], white_status)
        control_led(pins["red"], rgb_status)
        control_led(pins["green"], rgb_status)
        control_led(pins["blue"], rgb_status)
