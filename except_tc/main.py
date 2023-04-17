from tqdm import tqdm
import timeit
import json
import datetime
import asyncio
import websockets
import uuid
import pandas as pd

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
    ws = await websockets.connect(
        f'{wss_url}',
        subprotocols=["ocpp1.6"],
        extra_headers={"Authorization": 'Basic RVZBUjpFVkFSTEdV'}
    )
    total_count, failed_count, success_count = 0, 0, 0
    tc_name, tc_elapsed, send_data, recv_data = [], [], [], []

    with open("02. CVT_EVSP_CS.json", "r", encoding='utf-8') as fd:
        cases = json.load(fd)["item"][0]["item"]
        print(f'총 {len(cases)}개의 테스트 시나리오')
        for case in tqdm(cases, desc="Processing", unit="case"):
            for c in case["item"]:
                tc_name.append(c["name"])
                body = c["request"]["body"]["raw"].replace("\n", "")
                sdata = [2, f'{str(uuid.uuid4())}', case["name"], body]
                send_data.append(sdata)
                start = timeit.default_timer()
                await ws.send(json.dumps(sdata))
                recv = await ws.recv()
                elapsed = timeit.default_timer() - start
                tc_elapsed.append(elapsed)
                recv_data.append(json.loads(recv))
                recv = json.loads(recv)
                total_count += 1
                success_count += 1 if recv[0]==3 else 0
                failed_count += 1 if recv[0]==4 else 0
    print(f"Total: {total_count}, Success: {success_count}, Failed:{failed_count}")
    result_dict = {"TC명":tc_name, "수행시간":tc_elapsed, "요청 데이터": send_data, "응답 데이터": recv_data}
    import datetime
    pd.DataFrame(result_dict).to_csv(f'웹소켓_예외시험결과_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', encoding='utf-8-sig', index=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    async_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(async_loop)
    try :
        asyncio.run(runcase())
    except KeyboardInterrupt:
        pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
