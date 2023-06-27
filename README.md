# MiSTerRFID
Enables RFID card launching of games for MiSTer FPGA. Launches games without any menu being display using the MiSTer Game Launcher files (MGL) method. 

## Hardware Needed
- Raspberry Pi Pico 
- RC522 RFID Card Reader Module Board (3.3V)
- Mi-fare door access cards
- MiSTer FPGA with the extra USB ports board.

## Raspberry Pi Pico Hardware Setup
| RC522 Module Pin | Pico Pin|
|---|---|
|RST|34|
|SDA|22|
|MOSI|25|
|MISO|21|
|SCK|24|
|VCC|36|
|GRD|38|


## Raspberry Pi Pico Software Setup
- To be completed

## MiSTer Setup
Copy the files to your MiSTer SD card based on the structure of this repo. ATTENTION: Make sure you don't overwrite user-startup.sh if you have other services running like Favorites, Super Attract Mode or TTY2OLED. Instead, copy the contents into the file if it already exists.
  
## Use
To be completed
