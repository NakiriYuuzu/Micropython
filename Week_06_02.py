from machine import Pin, time_pulse_us
from time import sleep_us, sleep_ms

# 初始化 pin
trig = Pin(3, Pin.OUT)  # D1
echo = Pin(1, Pin.IN)  # D2


def get_distance():
    # 發送高級信號到 Trig
    trig.value(1)
    sleep_us(10)
    trig.value(0)

    # 等待 Echo 的回聲，並計算其持續時間（微秒）
    duration = time_pulse_us(echo, 1)

    # 根據速度 = 距離 / 時間 計算距離
    # 聲音速度 = 34300 cm/s = 34300 * 10^-6 cm/μs
    # 距離 = (持續時間 * 聲音速度) / 2
    return (duration * 34300) / 2 / 1e6


# 主程式
if __name__ == "__main__":
    while True:
        distance = get_distance()
        print("Distance: {:.2f} cm".format(distance))
        sleep_ms(500)
