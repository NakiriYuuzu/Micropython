# Run This script to run the program
# exec(open('main.py').read())

# This is for resetting the ESP8266 board
sudo esptool.py --port /dev/cu.usbserial-1120 erase_flash
esptool.py --port /dev/cu.usbserial-1120 --baud 1000000 write_flash --flash_size=4MB -fm dio 0 ESP8266_GENERIC-20231005-v1.21.0.bin

# this is for resetting the ESP32 board
esptool.py --chip esp32 --port /dev/cu.usbserial-1120 erase_flash
esptool.py --chip esp32 --port /dev/cu.usbserial-1120 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20231005-v1.21.0.bin
