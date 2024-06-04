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

### Setting Up a Telegram Bot

To create a Telegram bot and obtain the necessary credentials, follow these steps:

1. Open Telegram and search for the BotFather.

2. Start a chat with the BotFather and send `/start`.

3. Create a new bot by sending `/newbot` and follow the instructions to set the bot name and username.

4. After creating the bot, you will receive a token. Save this token as `telegram_token` in your `config.yaml`.

5. Get your chat ID by starting a chat with your bot and sending any message. Open the following URL in your browser: `https://api.telegram.org/bot<your-telegram-bot-token>/getUpdates`. Replace `<your-telegram-bot-token>` with your actual bot token. Look for the `chat` object in the response to find your chat ID.
For a more detailed tutorial on creating a Telegram bot and obtaining the token and chat ID, refer to [this tutorial](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

## Installation

### Clone the Repository
```sh
$ git clone https://github.com/yourusername/modbus-tcp-scanner.git
$ cd Modbus_scanner
```

### Creating a Python virtual environment
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


### Editing the Config file
```sh
ip_address: 'IP_of_mobdus_enabled_Device'   # for example: '192.168.40.110'             
telegram_token: 'your_telegram_bot_token'   # for example: '6357833747:AAG0fz5DvgyJRk6tGHpSpwxSfJktS2R_6W'
telegram_chat_id: 'your_telegram_chat_id'   # for example: '65442345'
```

### Running the Program
on the directory that contains register_checker.py
```sh
python register_checker.py
```


