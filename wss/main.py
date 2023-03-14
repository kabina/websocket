import asyncio
import logging
import websockets
from datetime import datetime
from props import meter
import json


global ws, transactionId

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

BootNotification = [2,
"19223201",
"BootNotification",
  {
    "chargePointModel": "ELA007C01",
    "chargePointVendor": "EVAR",
    "chargePointSerialNumber": "EVSCA070007",
    "firmwareVersion": "0.0.13",
    "imsi": "450061222990181"
  }
]
StatusNotification = [2,
"19223201",
"StatusNotification",
  {
    "connectorId": 1,
    "errorCode": "NoError",
    "status": "Available"
  }
]

HeartBeat = [2,
"19223201",
"DataTransfer",
  {
    "vendorId": "EVAR",
    "messageId": "heartbeat",
    "data": {}
  }
]

Authorize = [2,
"19223201",
"Authorize",
  {
    "idTag": None
  }
]

StartTransaction = [
  2,
  "1677223618",
  "StartTransaction",
  {
    "connectorId": 1,
    "idTag": None,
    "meterStart": 24000,
    "timestamp": "2023-02-24T07:26:57.512Z"
  }
]

MeterValues = [
  2,
  "1677228049",
  "MeterValues",
  {
    "connectorId": 1,
    "transactionId": 120532006,
    "meterValue": [
      {
        "timestamp": "2023-02-24T08:40:48.839Z",
        "sampledValue": [
          {
            "value": "25000",
            "measurand": "Energy.Active.Import.Register",
            "unit": "Wh"
          }
        ]
      }
    ]
  }
]

StopTransaction = [
  2,
  "1677228103",
  "StopTransaction",
  {
    "meterStop": 29000,
    "timestamp": "2023-02-24T08:41:42.615Z",
    "transactionId": 120532006
  }
]
async def sendDocs(doc):
    await ws.send(doc)
    logger.info(f"{json.loads(doc)[2]}:{doc}")
    recv = await ws.recv()
    logger.info(f"{json.loads(doc)[2]}:{recv}")
    return recv

async def sendBootNotification(reason=None) :
    doc = json.dumps(BootNotification)
    await sendDocs(doc)

async def sendStatusNotification(status=None) :
    doc = StatusNotification
    doc[3]["status"] = status
    await sendDocs(json.dumps(doc))


async def sendHeartBeat() :
    doc = HeartBeat
    await sendDocs(json.dumps(doc))

async def sendAuthorize(idTag=None) :
    doc = Authorize
    doc[3]["idTag"] = idTag
    await sendDocs(json.dumps(doc))

async def sendStartTransaction(idTag=None) :
    global transactionId
    doc = StartTransaction
    doc[3]["idTag"] = idTag
    recv = await sendDocs(json.dumps(doc))
    transactionId = json.loads(recv)[2]["transactionId"]

async def sendMeterValues() :
    doc = MeterValues
    doc[3]["transactionId"] = transactionId
    await sendDocs(json.dumps(doc))

async def sendStopTransaction() :
    doc = StopTransaction
    doc[3]["transactionId"] = transactionId
    await sendDocs(json.dumps(doc))


from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call, call_result
from ocpp.v16.enums import RegistrationStatus, ChargePointStatus, ChargePointErrorCode

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout)
        self.transaction_id = 0

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
        return response

    async def send_status_notification(self, status):
        request = call.StatusNotificationPayload(
            connector_id= 1,
            error_code= ChargePointErrorCode.noError,
            status= status,
            timestamp = datetime.utcnow().isoformat()
            #info = "test"
            #vendor_id: Optional[str] = None
            #vendor_error_code: Optional[str]
        )
        response = await self.call(request)
        return response

    async def send_Authorize(self):
        request = call.AuthorizePayload(
            id_tag= "1031040000069641"
        )
        response = await self.call(request)
        return response

    async def send_StartTransaction(self, reservation_id=None):
        request = call.StartTransactionPayload(
            connector_id= 1,
            id_tag= "1031040000069641",
            meter_start= 0,
            timestamp= datetime.utcnow().isoformat()#,
            #reservation_id=reservation_id
        )
        response = await self.call(request)
        self.transaction_id = response.transaction_id

        # return response
        return self.transaction_id

    async def send_MeterValues(self):
        print(f"METER{self.get_transaction_id()}")
        request = call.MeterValuesPayload(
            connector_id= 1,
            meter_value= meter,
            transaction_id= self.get_transaction_id()
        )
        response = await self.call(request)
        return response

    async def send_StopTransaction(self):
        request = call.StopTransactionPayload(
            meter_stop= 100000,
            timestamp= datetime.utcnow().isoformat(),
            transaction_id= self.get_transaction_id()
            # self.get_transaction_id()
            # self.transaction_id
            # reason: Optional[Reason] = None
            # id_tag: Optional[str] = None
            # transaction_data: Optional[List] = None
        )
        response = await self.call(request)
        return response

    def get_transaction_id(self):
        return self.transaction_id


async def main() :
    global ws
    ws = await websockets.connect(
            "wss://dbtrjhrz7uk2r.cloudfront.net/ELA007C01/EVSCA070007",
            subprotocols=["ocpp1.6"],
            extra_headers={"Authorization":"Basic RVZBUjpFVkFSTEdV"}
            )

    idtag = "1031040000069641"
    await sendBootNotification()
    await sendStatusNotification(status="Available")
    await sendHeartBeat()
    await sendAuthorize(idTag=idtag)
    await sendStatusNotification(status="Preparing")
    await sendStartTransaction(idTag=idtag)
    await sendStatusNotification(status="Charging")
    await sendMeterValues()
    await sendStopTransaction()
    await sendStatusNotification(status="Finishing")
    await sendStatusNotification(status="Available")

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
