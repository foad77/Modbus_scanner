# Modbus_scanner
It scans all the registers of a Modbus-TCP-enabled IP on your network and sends the report through the Telegram Bot

## Overview
Have you ever had to work with Modbus TCP-enabled devices through the command line but couldn't perform Modbus polling effectively? Were you wondering if the Modbus register map you have is correct? One way to verify this is by polling each register individually, but there are over 65,536 registers for each of the four types, making this process time-consuming.

Reading reports through the command line is also not the most convenient way to review results. Given these problems, I created this program, which scans the entire range of Modbus registers (over 65,536 registers for each of the four types), polls them, and then sends the report via a Telegram Bot. The report file is an Excel spreadsheet containing the status (open or closed) of each register type (coil, discrete inputs, input registers, holding registers) and a consolidated list of all open registers.

## Features
- Scans all Modbus registers for four types: coils, discrete inputs, input registers, and holding registers.
- Generates an Excel report with the status of each register.
- Sends the report through a Telegram Bot for easy access and review.

## Requirements
- Python 3.10.10
- Virtual environment with necessary Python packages installed (see `requirements.txt`)

## Installation

### Clone the Repository
```sh
git clone https://github.com/yourusername/modbus-tcp-scanner.git
cd Modbus_scanner


python -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
pip install --upgrade pip
pip install -r requirements.txt


## Editing the Config file
ip_address: 'IP_of_mobdus_enabled_Device'   # for example: '192.168.40.110'             
telegram_token: 'your_telegram_bot_token'   # for example: '6357833747:AAG0fz5DvgyJRk6tGHpSpwxSfJktS2R_6W'
telegram_chat_id: 'your_telegram_chat_id'   # for example: '65442345'


## Running the Program
on the directory that contains register_scanner.py
python register_scanner.py


