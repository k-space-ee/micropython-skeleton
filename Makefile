# Makefile for the board

NAME=esp32-20180222-v1.9.3-347-g6e675c1b.bin

all: flash console

flash:
	esptool.py -p /dev/ttyUSB0 -b 921600 erase_flash
	esptool.py -p /dev/ttyUSB0 -b 921600 write_flash --flash_mode dio 0x1000 bin/${NAME}
	sleep 5
	ampy -p /dev/ttyUSB0 put ssd1306.py

console:
	echo "Ctrl-A + Ctrl-Q to close Picocom"
	picocom -b115200 /dev/ttyUSB0
