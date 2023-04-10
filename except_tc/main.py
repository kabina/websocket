import requests
import json
import datetime
import asyncio
import websockets
import uuid

wss_url = "wss://ws.devevspcharger.uplus.co.kr/ocpp16/ELA007C05/EVSCA050001"
rest_url = "https://rgw.devevspcharger.uplus.co.kr/ioc"
header = {'Content-Type': 'application/json', 'Accept': 'application/json',
              'X-EVC-RI':datetime.datetime.now().isoformat(sep='T', timespec='seconds')+'Z',
              'X-EVC-BOX':'115001514011A',
              'X-EVC-SN':'EVSCA050001',
              'X-EVC-MDL':'ELA007C05',
              'X-EVC-OS':'Linux'
          }
async def runcase():
    with open("02. CVT_EVSP_CS.json", "r", encoding='utf-8') as fd:
        cases = json.load(fd)["item"][0]["item"]
        # print(cases)
        try :
            ws = await websockets.connect(
                f'{wss_url}',
                subprotocols=["ocpp1.6"],
                extra_headers={"Authorization": 'Basic RVZBUjpFVkFSTEdV'}
            )
            for case in cases:
                messageid = case["name"]
                for c in case["item"] :
                    print(c["request"]["body"]["raw"])
                    sdata = [2, f'{str(uuid.uuid4())}', messageid, f'{c["request"]["body"]["raw"]}']
                    print(sdata)
                    await ws.send(json.dumps(sdata))
                    recv = await ws.recv()
                    print(recv)
        except Exception as err:
            print(err)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    async_loop.run_until_complete(runcase())
    async_loop.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
