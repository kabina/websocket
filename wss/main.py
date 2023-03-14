import asyncio
import logging
import websockets
from datetime import datetime
import json
import props

global transactionId

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# timestamp= datetime.utcnow().isoformat()

class Charger :
    def __init__(self):
        self.ws = None
        self.transactionId = None

    async def conn(self):
        self.ws = await websockets.connect(
            "wss://dbtrjhrz7uk2r.cloudfront.net/ELA007C01/EVSCA070007",
            subprotocols=["ocpp1.6"],
            extra_headers={"Authorization": "Basic RVZBUjpFVkFSTEdV"}
        )
    async def sendDocs(self, ocpp):
        doc = props.ocppDocs[ocpp[0]]
        """ocpp 전문 실 데이터로 변환
        """
        for c in ocpp[1].keys():
            if c == "transactionId":
                doc[3]["transactionId"]=self.transactionId
            else :
                doc[3][c] = ocpp[1][c]

        await self.ws.send(json.dumps(doc))
        logger.info(f"{doc[2]}:{doc}")
        recv = await self.ws.recv()
        logger.info(f"{doc[2]}:{recv}")
        recv = json.loads(recv)
        # 후처리
        if ocpp[0]=="StartTransaction" and recv[0] == 3:
            self.transactionId = recv[2]["transactionId"]
        return recv

    async def runcase(self, cases):
        for c in cases :
            await self.sendDocs(c)

async def main() :

    idtag = "1031040000069641"
    c = Charger()
    await c.conn()
    await c.runcase(props.cases_normal_charge_with_boot)

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
