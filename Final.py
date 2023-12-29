from wifi_manager import WifiManager
from machine import Pin
import time
import urequests
import mfrc522

# SETUP PORT AND PIN
RED_PIN = Pin(0, Pin.OUT)
GREEN_PIN = Pin(2, Pin.OUT)
BLUE_PIN = Pin(15, Pin.OUT)
RFID = mfrc522.MFRC522(14, 13, 12, 16, 4)


# SETUP FUNCTIONS
def rgb_light(light):
    lights = {
        'RED': (1, 0, 0),
        'GREEN': (0, 1, 0),
        'BLUE': (0, 0, 1),
        'NONE': (0, 0, 0)
    }
    RED_PIN.value(lights[light][0])
    GREEN_PIN.value(lights[light][1])
    BLUE_PIN.value(lights[light][2])
    time.sleep(0.5)


# MAIN PROGRAM
rgb_light('NONE')
vm = WifiManager(ssid="YuuzuDevice")
vm.connect()

if not vm.is_connected():
    print("Unable to connect to WiFi")
else:
    print(vm.get_address())
    rgb_light('GREEN')
    rgb_light('NONE')
    while True:
        stat, tag_type = RFID.request(RFID.REQIDL)
        if stat == RFID.OK:
            stat2, raw_uid = RFID.anticoll()
            if stat2 == RFID.OK:
                rgb_light('BLUE')
                card_id = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                try:
                    response = urequests.get(f'https://120.110.115.127:8000/api/Card?card_id={card_id}')
                    if response.status_code == 200:
                        data = response.json()
                        print(data)
                        if data.get('result', '') == 'Success':
                            rgb_light('GREEN')
                            rgb_light('NONE')
                        else:
                            rgb_light('RED')
                            rgb_light('NONE')
                    else:
                        print("Error in API response:", response.status_code)
                        rgb_light('NONE')
                except Exception as e:
                    print("API request failed:", e)
                    rgb_light('NONE')
