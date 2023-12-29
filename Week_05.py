from machine import Pin, I2C, PWM
import urandom
import time
import utime
import dht
import ssd1306

# RGB_INIT
# whitePin = Pin(15, Pin.OUT)
redPin = Pin(14, Pin.OUT)
grnPin = Pin(12, Pin.OUT)
bluPin = Pin(13, Pin.OUT)
red_pwm = PWM(redPin)
grn_pwm = PWM(grnPin)
blu_pwm = PWM(bluPin)

# OLED_INIT
I2C_ADDRESS, RST_PIN = 0x3C, -1  # Unused Code.
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# DHT_INIT
DHT_PIN = 15
sensor = dht.DHT11(Pin(DHT_PIN))


def set_random_rgb():
    red_val = urandom.getrandbits(10)  # 隨機生成0-1023之間的數字
    green_val = urandom.getrandbits(10)
    blue_val = urandom.getrandbits(10)

    # 設置RGB LED的值
    red_pwm.duty(red_val)
    grn_pwm.duty(green_val)
    blu_pwm.duty(blue_val)


def oled_result(temperature, humidity):
    current_time = utime.localtime()
    hours = current_time[3]
    minutes = current_time[4]
    seconds = current_time[5]
    oled.fill(0)  # 清屏
    oled.text("Time: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
    oled.text("Temp: {} C".format(temperature), 0, 10)
    oled.text("Humid: {} %".format(humidity), 0, 20)
    oled.show()  # 刷新顯示


def dht_result():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def init():
    oled.fill(0)  # Clean the OLED screen.


# main
if __name__ == "__main__":
    time.sleep(1)
    init()
    time.sleep(5)

    while True:
        temp, humid = dht_result()
        oled_result(temp, humid)
        set_random_rgb()
        time.sleep(1)
