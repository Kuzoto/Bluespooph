import asyncio
import json
from bleak import BleakScanner
from bleak import BleakClient

async def scan_and_connect():
    device = await BleakScanner.find_device_by_name("My Device")
    if not device:
        print("Device not found")
        return
    
    async with BleakClient(device) as client:
        data = await client.read_gatt_char(device)
        print("received: " + data)

# Do have one async main function that does everything.
async def main():
    while True:
        await scan_and_connect()
        # Do use asyncio.sleep() in an asyncio program.
        await asyncio.sleep(5)

asyncio.run(main())
