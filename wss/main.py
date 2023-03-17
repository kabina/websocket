import asyncio
import logging
import websockets
from datetime import datetime
import json
import props
import jsonschema
from colorlog import ColoredFormatter
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# wss_url = "wss://dbtrjhrz7uk2r.cloudfront.net/ELA007C01/EVSCA070007",
wss_url = "wss://ws.devevspcharger.uplus.co.kr/ocpp16/ELA007C01/EVSCA070007"


rest_url =""
formatter = ColoredFormatter(
    "%(log_color)s[%(asctime)s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white,bold',
        'INFOV':    'cyan,bold',
        'WARNING':  'yellow',
        'ERROR':    'red,bold',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
ch.setFormatter(formatter)

logger = logging.getLogger('attcap')
logger.setLevel(logging.DEBUG)
logger.handlers = []       # No duplicated handlers
logger.propagate = False   # workaround for duplicated logs in ipython
logger.addHandler(ch)

logging.addLevelName(logging.INFO + 1, 'INFOV')

# timestamp= datetime.utcnow().isoformat()

class Charger :
    def __init__(self):
        self.ws = None
        self.transactionId = 0
        self.rmessageId = None

    async def conn(self):
        self.ws = await websockets.connect(
            wss_url,
            subprotocols=["ocpp1.6"],
            extra_headers={"Authorization": "Basic RVZBUjpFVkFSTEdV"}
        )

    async def waitMessages(self):

        try :
            while True:
                message = await asyncio.wait_for(self.ws.recv(), 5)
                message = json.loads(message)
                logger.info(f"<< {message[2]}:{message}")
                self.rmessageId = message[1]

                """ToDo: 이 위치에 서버의 명령에 따른 처리 추가 필요
                """
                return message
        except Exception as e:
            return

    async def sendReply(self, ocpp):
        """
        응답전문 발송
        :param ocpp: 응답전문 본체
        :return: None
        """
        ocpp[1] = self.rmessageId
        if "transactionId" in ocpp[2] and self.transactionId > 0:
            ocpp[2]["transactionId"] = self.transactionId
        await self.ws.send(json.dumps(ocpp))
        logger.info(f">> Reply {ocpp}")
        noused = await self.ws.recv()
        logger.info(f"<< Check Response for Reply |{noused}|")


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

        doc[1] = f'{uuid.uuid4()}'
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

    async def callbackRequest(self, msgType, doc):
        rest_url = 'https://8b434254zg.execute-api.ap-northeast-2.amazonaws.com/dev/ioc'
        import requests
        if "transactionId" in doc[3] :
            doc[3]["transactionId"] = self.transactionId

        reqdoc = {
            "crgrMid":"11500151303",
            "data": doc
        }
        header = {
            "Accept":"*/*",
            "Content-Type":"application/json",
            "Cache-Control":"no-cache",
        }
        response = requests.post(rest_url, headers=header, data= json.dumps(reqdoc), verify=False, timeout=5).json()

    async def runcase(self, cases):

        import time
        scases = []
        failed = 0
        for case in cases.keys():
            logger.debug("+===========================================================")
            logger.info(f"Testing... [{case}]")
            logger.debug("+===========================================================")
            for c in cases[case] :

                if c[0] == "Wait" :
                    print(f"Waiting message from CSMS [{c[1]}] ...")
                    doc = props.ocppDocs[c[1]]
                    if len(c) > 2:
                        for d in c[2].keys():
                            doc[3][d] = c[2][d]
                    await self.callbackRequest(c[1], doc)
                elif c[0] == "Reply":
                    recv = await self.waitMessages()
                    if recv == None :
                        scases.append(case)
                        logger.error("None response from server. test case failed")
                        continue
                    if self.checkSchema(c[1], recv[3]) == False:
                        logger.error(f"Fail ( Invalid testcase message from server, expected ({c[1]}) received ({recv[2]})")
                        scases.append(case)
                    else:
                        senddoc = props.ocppDocs[f"{recv[2]}Response"]
                        senddoc[1] = recv[1]
                        if len(c)>2 :
                            for d in c[2].keys() :
                                senddoc[2][d]=c[2][d]
                        await self.sendReply(senddoc)
                else :
                    recv = await self.sendDocs(c)
                    if self.checkSchema(f"{c[0]}Response", recv[2]) == False:
                        logger.error(f"Fail ( Invalid testcase message from server )")
                        scases.append(case)

        logger.debug(f"Total {len(cases)} cases tested and {len(cases)-len(scases)} cases succeed. Failed cases are as follows")
        logger.debug("==========================================================================")
        for c in scases:
            logger.debug(f"{c}")

async def main() :

    c = Charger()
    await c.conn()
    await c.runcase(props.TC)

if __name__ == "__main__":
    asyncio.run(main())
