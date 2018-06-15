4MICs HAT for Raspberry Pi
==========================

## Introduction

Les fichiers autres que **listeningSnipsEvents.py** sont repris du dépot [4mics_hat](https://github.com/respeaker/4mics_hat.git)

## Setup for LEDs
1. Use `raspi-config` to enable SPI.
2. Install `spidev` and `gpiozero` (`pip install spidev gpiozero`)
3. Run `python pixels_demo.py` to test LED animation example
