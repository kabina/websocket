import asyncio
import logging

import websockets
import json
import uuid
import jsonschema
from colorlog import ColoredFormatter
import urllib3
from datetime import datetime
import tkinter as tk
from tkinter import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

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

def change_text(obj, text):
    obj.delete(0, END)
    obj.insert(0, text)

class Config():
    def __init__(self, **kwargs):
        self.wss_url = kwargs["wss_url"]
        self.rest_url = kwargs["rest_url"]
        self.auth_token = kwargs["auth_token"]
        self.en_tr = kwargs["en_tr"]
        self.en_tc = kwargs["en_tc"]
        self.lst_cases = kwargs["lst_cases"]
        self.en_status = kwargs["en_status"]
        self.txt_recv = kwargs["txt_recv"]
        self.cid = kwargs["cid"]
        self.rcid = kwargs["rcid"]
        self.sno = kwargs["sno"]
        self.rsno  = kwargs["rsno"]
        self.mdl = kwargs["mdl"]
        self.result = kwargs["result"]
        self.confV = kwargs["confV"]
        self.en_reserve = kwargs["en_reserve"]
        self.lst_tc = kwargs["lst_tc"]
        self.test_mode = kwargs["test_mode"]
        self.ocppdocs = kwargs["ocppdocs"]
        self.txt_tc = kwargs["txt_tc"]

class Charger() :
    _transactionId: int

    def __init__(self, config):
        self.ws = None
        self._transactionId = 0
        self.rmessageId = None
        self.logger = logger
        self.config = config
        self.en_tr = config.en_tr
        self.en_tc = config.en_tc
        self.lst_cases = config.lst_cases
        self.en_status = config.en_status
        self.txt_recv = config.txt_recv
        self.cid = config.cid
        self.rcid = config.rcid
        self.mdl = config.mdl
        self.result = config.result
        self.status = 0
        self.confV = config.confV
        self.en_reserve = config.en_reserve
        self.lst_tc = config.lst_tc
        self.test_mode = config.test_mode
        self.ocppdocs = config.ocppdocs
        self.txt_tc = config.txt_tc

        self.arr_messageid = {
            "$uuid":str(uuid.uuid4()),
            "$timestamp":datetime.now().isoformat(sep="T", timespec="seconds")
        }
    def log(self, log, attr=None):
        from datetime import datetime
        if attr:
            self.txt_recv.tag_config(attr, foreground=attr)
        self.txt_recv.insert(END, datetime.now().isoformat() +' '+ log + '\n', attr)
        self.txt_recv.see("insert")
    def tc_render(self, adict, k):
        import datetime
        if isinstance(adict, dict):
            for key in adict.keys():
                if adict[key] == k:
                    try:
                        adict[key] = self.confV[k]
                    except ValueError:
                        pass  # do nothing if the timestamp is already in the correct format
                elif isinstance(adict[key], (dict, list)):
                    self.tc_render(adict[key], k)
        elif isinstance(adict, list):
            for l in adict:
                self.tc_render(l, k)
    def change_result(self, idx, res):
        self.result[idx] = res

    def stop(self):
        self.status = -1

    def update_config(self, config):
        self.config = config
        self.config = config
        self.en_tr = config.en_tr
        self.en_tc = config.en_tc
        self.lst_cases = config.lst_cases
        self.en_status = config.en_status
        self.txt_recv = config.txt_recv
        self.cid = config.cid
        self.rcid = config.rcid
        self.mdl = config.mdl
        self.confV = config.confV
        self.en_reserve = config.en_reserve
        self.lst_tc = config.lst_tc
        self.test_mode = config.test_mode
        self.ocppdocs = config.ocppdocs

    def change_list(self, case, text, attr=None, log=None):
        # idx = obj.get(0, "end").index(case.split()[0])
        try:
            idx = self.lst_cases.get(0, "end").index(case.split()[0])
            self.lst_cases.delete(idx)
            self.lst_cases.insert(idx, text)
            if attr:
                self.lst_cases.itemconfig(idx, attr)
            if log:
                self.result[idx] = log
        except Exception as e:
            pass

    async def conn(self, case):

        if len(case.split('_')) > 1 and 46 <= int(case.split('_')[1]) <= 53 :
            wss_url = f'{self.config.wss_url}/{self.mdl}/{self.config.rsno}'
        else:
            wss_url = f'{self.config.wss_url}/{self.mdl}/{self.config.sno}'
        try :
            self.ws = await websockets.connect(
                f'{wss_url}',
                subprotocols=["ocpp1.6"],
                extra_headers={"Authorization": self.config.auth_token}
            )
        except Exception as err:
            self.log(" 연결에 실패했습니다", attr="red")

        self.en_tr.delete(0, END)
        self.en_tr.insert(0,"Not In Transaction")

    async def close(self):
        await self.ws.close()

    async def waitMessages(self):

        try :
            while True:
                message = await asyncio.wait_for(self.ws.recv(), 600)
                message = json.loads(message)
                self.log(f" << {message[2]}:{message}", attr='blue')
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
        if "transactionId" in ocpp[2] and self._transactionId > 0:
            ocpp[2]["transactionId"] = self._transactionId
        elif "reservationId" in ocpp[2] :
            ocpp[2]["reservationId"]=self.en_reserve
        await self.ws.send(json.dumps(ocpp))
        self.log(f" >> Reply {ocpp}", attr='blue')
        noused = await self.ws.recv()
        self.log(f" << Check Response for Reply |{noused}|")

    def convertDocs(self, doc):
        for k in self.confV.keys():
            self.tc_render(doc, k)

        # confVkey = self.confV.keys()
        # print(doc, confVkey)
        # for k in doc[3].keys():
        #     if isinstance(doc[3][k], (dict,list)) :
        #         continue
        #     elif doc[3][k] in confVkey:
        #         doc[3][k] = self.confV[doc[3][k]]

    def convertSendDoc(self, ocpp) -> dict:

        doc = self.ocppdocs[ocpp[0]]
        """전문 템플릿 변환"""
        self.convertDocs(doc[3])

        """TC내 지정 전문 변환"""
        self.convertDocs(ocpp[1])
        import uuid
        for c in ocpp[1].keys():
            doc[3][c] = ocpp[1][c]

        """messageId 처리"""
        if doc[1] in self.arr_messageid.keys() :
            doc[1] = self.arr_messageid[doc[1]]
        else :
            doc[1] = f'{str(uuid.uuid4())}'

        return doc

    async def sendDocs(self, doc):


        await self.ws.send(json.dumps(doc))

        self.log(f' >> {doc[2]}:{doc}', attr='blue')
        recv = await self.ws.recv()
        self.log(f' << {doc[2]}:{recv}', attr='blue')
        recv = json.loads(recv)
        # 후처리
        if doc[2]=="StartTransaction" and recv[0] == 3:
            self._transactionId = recv[2]["transactionId"]
            self.confV["$transactionId"] = recv[2]["transactionId"]
            self.en_tr.delete(0,END)
            self.en_tr.insert(0,recv[2]["transactionId"])
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
            return False, e.message
        return True,None

    async def callbackRequest(self, msgType, doc):
        rest_url = self.config.rest_url
        import requests, uuid
        if "transactionId" in doc[3] :
            doc[3]["transactionId"] = self._transactionId
        doc[1] = f'{str(uuid.uuid4())}'
        self.convertDocs(doc)
        reqdoc = {
            "crgrMid":self.config.rcid[:11] if doc[2].startswith("Reserve") else self.config.cid[:11],
            "data": doc
        }
        header = {
            "Accept":"*/*",
            "Content-Type":"application/json",
            "Cache-Control":"no-cache",
        }
        self.log(f" DATA To Server >> {reqdoc} ...", attr='green')
        response = requests.post(rest_url, headers=header, data= json.dumps(reqdoc), verify=False, timeout=5).json()

    def recv_check(self, recv, target):
        for t in target.keys():
            if isinstance(target[t], dict) :
                return self.recv_check(recv[t], target[t])
            elif t in recv.keys() and target[t] != recv[t]:
                return (False, target)
        return (True, None)

    async def runcase(self, cases):

        import time
        scases = []
        step_count = 0
        self.status = 0
        self.txt_recv.see(END)
        for idx, case in enumerate(cases.keys()):

            await self.conn(case)
            if self.status == -1 :
                break
            self.log("+===========================================================", attr='green')
            self.log(f"Testing... [{case}]", attr='green')
            self.log("+===========================================================", attr='green')
            change_text(self.en_tc, case)
            self.lst_cases.see(idx)
            ilen = len(cases[case])
            for idx2, c in enumerate(cases[case]):

                self.lst_tc.selection_clear(0, 'end')
                self.lst_tc.select_set(step_count)
                self.lst_tc.itemconfig(step_count, {'fg': 'green'})

                step_count += 1
                self.lst_tc.see(step_count)
                if c[0] == "Wait" :
                    self.log(f" Waiting message from CSMS [{c[1]}] ...", attr='green')
                    if self.test_mode == 1:
                        doc = self.ocppdocs[c[1]]
                        if len(c) > 2:
                            for d in c[2].keys():
                                doc[3][d] = c[2][d]
                        await self.callbackRequest(c[1], doc)
                elif c[0] == "Reply":
                    recv = await self.waitMessages()
                    if recv == None :
                        scases.append(case)
                        result = " None response from server. test case failed"
                        self.log(result , attr='red')
                        self.change_list(case, f"{case} (Fail)", attr={'fg': 'red'}, log=result)

                        break
                    schema_check = self.checkSchema(c[1], recv[3])
                    if not schema_check[0]:
                        result = f" Fail ( Invalid testcase message from server, expected ({schema_check[1]})"
                        self.log(result, attr='red')
                        scases.append(case)
                        self.change_list(case, f"{case} (Fail)", attr={'fg':'red'}, log=result)
                        break
                    else:
                        senddoc = self.ocppdocs[f"{recv[2]}Response"]
                        senddoc[1] = recv[1]
                        if len(c)>2 :
                            for d in c[2].keys() :
                                senddoc[2][d]=c[2][d]
                        await self.sendReply(senddoc)
                else :

                    doc = self.convertSendDoc(c)
                    self.txt_tc.delete(1.0, END)
                    self.txt_tc.insert(END, json.dumps(doc, indent=2))

                    schema_check = self.checkSchema(f"{c[0]}", doc[3])
                    if not schema_check[0] :
                        result = f" Fail ( Invalid testcase sending message from server. {schema_check[1]} )"
                        self.log(result , attr='red')
                        scases.append(case)
                        self.change_list(case, f"{case} (Fail)", attr={'fg':'red'}, log=result)
                        break
                    recv = await self.sendDocs(doc)
                    schema_check = self.checkSchema(f"{c[0]}Response", recv[2])
                    if not schema_check[0]:
                        result = f" Fail ( Invalid testcase recv message from server. {schema_check[1]} )"
                        self.log(result , attr='red')
                        scases.append(case)
                        self.change_list(case, f"{case} (Fail)", attr={'fg':'red'}, log=result)
                        break
                    if len(c)>2 and recv[0]==3:
                        chk = self.recv_check(recv[2], c[2])
                        if not chk[0]:
                            result = f" Fail ( Not expected response from server(expected: {chk[1]}. ))"
                            self.log(result, attr='red')
                            scases.append(case)
                            self.change_list(case, f"{case} (Fail)", attr={'fg': 'red'}, log=result)
                            break

                if idx2 == (ilen-1) :
                    self.change_list(case, f"{case} (Pass)", attr={'fg':'blue'}, log="Passed")

            await self.close()

        self.log(f" Total {len(cases)} cases tested and {len(cases)-len(scases)} cases succeed. Failed cases are as follows", attr='green')
        self.log(" ==========================================================================", attr='green')
        for c in scases:
            self.log(f" {c}", attr='green')

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
