from wifi_manager import WifiManager
from machine import Pin
import socket
import json
import urequests
import mfrc522
import asyncio

# SETUP PORT AND PIN
PORT = 80
RED_PIN = Pin(0, Pin.OUT)
GREEN_PIN = Pin(2, Pin.OUT)
BLUE_PIN = Pin(15, Pin.OUT)
RFID = mfrc522.MFRC522(14, 13, 12, 16, 4)


# SETUP FUNCTIONS
async def handle_rfid_reading():
    while True:
        stat, tag_type = RFID.request(RFID.REQIDL)
        if stat == RFID.OK:
            stat2, raw_uid = RFID.anticoll()
            if stat2 == RFID.OK:
                await rgb_light('BLUE')
                card_id = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                try:
                    response = urequests.get(f'https://120.110.115.127:8000/api/Card?card_id={card_id}')
                    if response.status_code == 200:
                        data = response.json()
                        print(data)
                        if data.get('Success', False):
                            await rgb_light('GREEN')
                            await rgb_light('NONE')
                        else:
                            await rgb_light('RED')
                            await rgb_light('NONE')
                    else:
                        print("Error in API response:", response.status_code)
                except Exception as e:
                    print("API request failed:", e)
        await asyncio.sleep(0.5)


async def rgb_light(light):
    lights = {
        'RED': (1, 0, 0),
        'GREEN': (0, 1, 0),
        'BLUE': (0, 0, 1),
        'NONE': (0, 0, 0)
    }
    RED_PIN.value(lights[light][0])
    GREEN_PIN.value(lights[light][1])
    BLUE_PIN.value(lights[light][2])
    await asyncio.sleep(0.5)


async def handle_network_requests():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(5)
    print("Server started")
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request_str = request.decode("utf-8")
        print('Content =', request_str)
        response_dict = {"status": "", "message": ""}
        if '/open' in request_str or '/close' in request_str:
            response_dict["status"] = "success"
            response_dict["message"] = "Door Opened" if '/open' in request_str else "Door Closed"
        else:
            response_dict["status"] = "error"
            response_dict["message"] = "Invalid URL"

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(json.dumps(response_dict))
        conn.close()


# MAIN PROGRAM
async def main():
    rgb_light('NONE')
    vm = WifiManager(ssid="YuuzuDevice")
    vm.connect()

    if vm.is_connected():
        print(vm.get_address())
        await rgb_light('GREEN')
        await rgb_light('NONE')
    else:
        print("Unable to connect to WiFi")

    # Start the asynchronous tasks
    task1 = asyncio.create_task(handle_rfid_reading())
    task2 = asyncio.create_task(handle_network_requests())

    # Wait for both tasks to complete (if ever)
    await asyncio.gather(task1, task2)


asyncio.run(main())
