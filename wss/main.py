import asyncio
import logging
import websockets
from datetime import datetime
import json
import props
import jsonschema
import colorlog

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(CustomFormatter())
logger.addHandler(stream_handler)

# timestamp= datetime.utcnow().isoformat()

class Charger :
    def __init__(self):
        self.ws = None
        self.transactionId = None

    async def conn(self):
        self.ws = await websockets.connect(
            # "wss://dbtrjhrz7uk2r.cloudfront.net/ELA007C01/EVSCA070007",
            "wss://ws.devevspcharger.uplus.co.kr/ocpp16/ELA007C01/EVSCA070007",
            subprotocols=["ocpp1.6"],
            extra_headers={"Authorization": "Basic RVZBUjpFVkFSTEdV"}
        )

    async def waitMessages(self):
        while True:
            message = await self.ws.recv()
            logger.info(f"<< {json.loads(message)[2]}:{message}")

            """ToDo: 이 위치에 서버의 명령에 따른 처리 추가 필요
            """
            return message

    async def sendReply(self, ocpp):
        """
        응답전문 발송
        :param ocpp: 응답전문 본체
        :return: None
        """
        ocpp[1] = datetime.utcnow().isoformat()
        await self.ws.send(json.dumps(ocpp))
        logger.info(f">> Reply {ocpp}")


    async def sendDocs(self, ocpp):
        doc = props.ocppDocs[ocpp[0]]
        """ocpp 전문 실 데이터로 변환
        """
        import uuid
        for c in ocpp[1].keys():
            if c == "transactionId":
                doc[3]["transactionId"]=self.transactionId
            else :
                doc[3][c] = ocpp[1][c]

        doc[1] = uuid.uuid4().hex
        await self.ws.send(json.dumps(doc))
        logger.info(f">> {doc[2]}:{doc}")
        recv = await self.ws.recv()
        logger.info(f"<< {doc[2]}:{recv}")
        recv = json.loads(recv)

        # 후처리
        if ocpp[0]=="StartTransaction" and recv[0] == 3:
            self.transactionId = recv[2]["transactionId"]
        return recv

    def checkSchema(self, original, target):
        """
        OCPP 규격과 다른지 체크, 다를 경우 False Return
        :param original: 점검 대상 스키마 명
        :param target: 점검 대상 Json 본체
        :return: True : 규격 동일, False: 규격 다름
        """
        try :
            schema = open("./schemas/"+original+".json").read().encode('utf-8')
            jsonschema.validate(instance=target, schema=json.loads(schema))
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            return False
        return True

    async def runcase(self, cases):
        import time
        for case in cases.keys():
            logger.info(f"Testing... [{case}]")
            for c in cases[case] :
                if c[0] == "Wait" :
                    time.sleep(1)
                    print(f"Waiting message from CSMS [{c[1]}] ...")
                    recv = await self.waitMessages()
                    recv = json.loads(recv)
                    if self.checkSchema(c[1], recv[3]) == False and recv[2] != c[1]:
                        logger.error(f"Fail ( Invalid testcase message from server, expected ({c[1]}) received ({recv[2]})")
                    else:
                        await self.sendReply(props.ocppDocs[f"{recv[2]}Response"])
                else :
                    recv = await self.sendDocs(c)
                    if self.checkSchema(f"{c[0]}Response", recv[2]) == False:
                        logger.error(f"Fail ( Invalid testcase message from server )")

async def main() :

    c = Charger()
    await c.conn()
    await c.runcase(props.TC)

if __name__ == "__main__":
    asyncio.run(main())
