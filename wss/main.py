import asyncio
import logging

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)


from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="ELA007C01",
            charge_point_vendor="EVAR",
            charge_point_serial_number="EVSCA070007",
            firmware_version="0.0.13",
            imsi="450061222990181",
            meter_serial_number="M3123",
            meter_type="MT"
        )
        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    async def send_status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id= 1,
            error_code= None,
            status= "Available"
            #timestamp: Optional[str] = None
            #info: Optional[str] = None
            #vendor_id: Optional[str] = None
            #vendor_error_code: Optional[str]
        )
        response = await self.call(request)
        print(response)

async def main():
    async with websockets.connect(
        "wss://4pt7sawhd9.execute-api.ap-northeast-2.amazonaws.com/demo", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("CP_1", ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())
        await asyncio.gather(cp.send_status_notification())

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())