import asyncio
import codecs
from bleak import BleakScanner
from bleak import BleakClient
import bleak;
from bleak import BleakGATTCharacteristic;
import chardet


async def main():
    devices = []
    async with BleakScanner() as scanner:
        print("Scanning...")

        async for bd, ad in scanner.advertisement_data():
            if bd.name != None and devices.count(bd.name + ": " + bd.address) == 0:
                devices.append(bd.name + ": " + bd.address)
                print(bd.name + ": " + bd.address)
                try:
                    async with BleakClient(bd.address) as client:
                        if client.is_connected:
                            for characteristic in client.services.characteristics:
                                try:
                                    char = await client.read_gatt_char(characteristic)
                                    type = chardet.detect(char)
                                    if type["encoding"] != None:
                                        print(client.services.get_characteristic(characteristic).description + ": " + char.decode(type["encoding"]))
                                    else:
                                        print(client.services.get_characteristic(characteristic).description + ": ".join(map(chr, char)))
                                except Exception as f:
                                    await client.start_notify(client.services.get_characteristic(characteristic), callback)
                                    print(f)
                                    client.stop_notify(client.services.get_characteristic(characteristic))
                except Exception as e:
                    print(e)

def callback(sender: BleakGATTCharacteristic, data: bytearray):
    type = chardet.detect(data)
    print(f"{sender.description}: {data.decode(type['encoding'])}")
         

asyncio.run(main())