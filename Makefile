### Arduino RackTOR Makeile
PROJECT_DIR                 = /home/pi/RackTOR
ARDMK_DIR                   = $(PROJECT_DIR)/Arduino-Makefile
ARDUINO_DIR                 = /usr/share/arduino

USER_LIB_PATH              := $(PROJECT_DIR)/lib
BOARD_TAG                   = mega2560
ARDUINO_PORT			    = /dev/ttyACM0
MONITOR_BAUDRATE            = 9600
MONITOR_PORT 				= /dev/ttyACM0

AVR_TOOLS_DIR               = /usr

AVRDUDE                     = /usr/bin/avrdude
AVRDUDE_CONF				= /etc/avrdude.conf

CFLAGS_STD                  = -std=gnu11
CXXFLAGS_STD                = -std=gnu++11
CXXFLAGS                   += -pedantic -Wall -Wextra

CURRENT_DIR                 = $(shell basename $(CURDIR))
OBJDIR                      = $(PROJECT_DIR)/bin/$(BOARD_TAG)/$(CURRENT_DIR)

include $(ARDMK_DIR)/Arduino.mk
