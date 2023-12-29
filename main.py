from wifi_manager import WifiManager
from machine import Pin
import urequests
import socket
import json


# TODO: NFC 模块， 驗證身份

wm = WifiManager(ssid="YuuzuDevice")
wm.connect()


def check_permissions():
    pass


if not wm.is_connected():
    print("Unable to connect to WiFi")
else:
    print(f"Connected to Wifi {wm.get_address()}")
    try:
        response = urequests.post('http://120.110.115.127:8000/api/login', json={"ip": wm.get_address()})
        print("Response from backend:", response.text)
        response.close()
    except Exception as e:
        print("Send to backend failed:", e)

    print("Starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("Server started")

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)

        # 初始化响应字典
        response_dict = {"status": "", "message": ""}

        # 根据请求的 URL 控制门
        if '/open' in request:
            if check_permissions():
                response_dict["status"] = "success"
                response_dict["message"] = "Door Opened"
                print(response_dict["status"], response_dict["message"])
            else:
                response_dict["status"] = "error"
                response_dict["message"] = "Permission Denied"
                print(response_dict["status"], response_dict["message"])
        elif '/close' in request:
            if check_permissions():
                response_dict["status"] = "success"
                response_dict["message"] = "Door Closed"
                print(response_dict["status"], response_dict["message"])
            else:
                response_dict["status"] = "error"
                response_dict["message"] = "Permission Denied"
                print(response_dict["status"], response_dict["message"])
        else:
            response_dict["status"] = "error"
            response_dict["message"] = "Invalid URL"
            print(response_dict["status"], response_dict["message"])

        # 发送 JSON 格式的 HTTP 响应
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(json.dumps(response_dict))
        conn.close()
