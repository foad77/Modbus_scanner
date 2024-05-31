#!/usr/bin/env python3

import asyncio
from pymodbus.client.tcp import AsyncModbusTcpClient as ModbusClient
import pandas as pd
from datetime import datetime
import aiohttp
import subprocess
from tqdm import tqdm  # Import tqdm for the progress bar functionality
import os
import logging
import yaml

# Load configuration from config.yaml
with open('Config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Extract configuration values
IP_ADDRESS = config['ip_address']
TELEGRAM_TOKEN = config['telegram_token']
TELEGRAM_CHAT_ID = config['telegram_chat_id']

# Setup logging
logging.basicConfig(filename='client_log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Configuration
PORT = 502
NUM_REGISTERS = 100000  # Maximum value, adjusted for the example

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    logging.info("Screen cleared")

def check_port(ip, port):
    """Check if a specific port is open using nc (Netcat)."""
    try:
        result = subprocess.run(['nc', '-zv', ip, str(port)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Port check passed for {ip}:{port}")
        return True
    except subprocess.CalledProcessError:
        logging.error(f"Port check failed for {ip}:{port}")
        return False

async def read_registers(client, read_function, start_address, num_registers, unit_id=0x02, register_type=""):
    """Generic function to read Modbus registers and return results with a progress bar."""
    results = []
    success_registers = []
    end_address = min(start_address + num_registers, 65536)  # Ensure we do not exceed the Modbus limit
    for address in tqdm(range(start_address, end_address), desc=f"Scanning {register_type}"):
        response = await read_function(address, 1, unit=unit_id)
        if not response.isError():
            results.append((address, response.registers))
            success_registers.append((address, register_type))
            logging.info(f"Read successful for {register_type} at address {address}")
        else:
            error_detail = str(response)
            results.append((address, error_detail))
            logging.error(f"Error scanning {register_type} at address {address}: {error_detail}")
    return results, success_registers

async def send_telegram_document(file_path, token, chat_id):
    """Send a document via Telegram bot asynchronously and delete the file locally if sent successfully."""
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    data = aiohttp.FormData()
    data.add_field('chat_id', chat_id)
    data.add_field('document', open(file_path, 'rb'))
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            if response_data.get("ok"):  # Check if the response from Telegram is ok
                try:
                    os.remove(file_path)  # Delete the file after successful transmission
                    logging.info("File sent and deleted locally.")
                except Exception as e:
                    logging.error(f"Error deleting the file: {e}")
            else:
                logging.error("Failed to send the document to Telegram.")

async def main():
    clear_screen()  # Clear the screen before starting the scan
    if not check_port(IP_ADDRESS, PORT):
        print("Modbus Port (502) is blocked! Register Scan End Now!")
        return

    client = ModbusClient(host=IP_ADDRESS, port=PORT)
    await client.connect()

    coils, success_coils = await read_registers(client, client.read_coils, 0, NUM_REGISTERS, register_type="Coil")
    discrete_inputs, success_discrete = await read_registers(client, client.read_discrete_inputs, 0, NUM_REGISTERS, register_type="Discrete Input")
    input_registers, success_inputs = await read_registers(client, client.read_input_registers, 0, NUM_REGISTERS, register_type="Input Register")
    holding_registers, success_holdings = await read_registers(client, client.read_holding_registers, 0, NUM_REGISTERS, register_type="Holding Register")

    client.close()

    all_successes = success_coils + success_discrete + success_inputs + success_holdings
    date_time = datetime.now().strftime("D_%m_%d_T_%H_%M")
    excel_file_path = f"Modbus_Scan_{date_time}.xlsx"
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        pd.DataFrame(coils, columns=['Address', 'Value']).to_excel(writer, sheet_name='Coils', index=False)
        pd.DataFrame(discrete_inputs, columns=['Address', 'Value']).to_excel(writer, sheet_name='Discrete Inputs', index=False)
        pd.DataFrame(input_registers, columns=['Address', 'Value']).to_excel(writer, sheet_name='Input Registers', index=False)
        pd.DataFrame(holding_registers, columns=['Address', 'Value']).to_excel(writer, sheet_name='Holding Registers', index=False)
        if all_successes:
            pd.DataFrame(all_successes, columns=['Address', 'Type']).to_excel(writer, sheet_name='Successful Reads', index=False)

    await send_telegram_document(excel_file_path, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    print("Modbus register scan finished and saved to Excel. File sent to Telegram.")
    if not all_successes:
        print("No Open Registers were found in this scan!")

if __name__ == "__main__":
    asyncio.run(main())
