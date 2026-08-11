cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(bledev_firmware C)

target_sources(app PRIVATE
  src/capture.c
  src/main.c
  src/protocol.c
  src/radio.c
  src/timestamp.c
  src/usb.c
)

target_include_directories(app PRIVATE src)

