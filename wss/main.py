import asyncio
import logging
import tkinter

import json
import props
import tkinter as tk
from Charger import Charger, TextHandler, Config

from async_tkinter_loop import async_handler, async_mainloop
#from tkinter import ttk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd
from datetime import datetime
import sys

class MyApp(tk.Tk):

    def __init__(self):
        self.window = tkinter.Tk()
        self.tabs = ttk.Notebook(self.window)
        s = ttk.Style()
        s.theme_use('default')
        s.configure('Tab', width=10)
        self.tabs.pack(fill=BOTH, expand=TRUE)
        self.tab1 = tkinter.ttk.Frame(self.tabs)
        self.tab2 = tkinter.ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="TC Run")
        self.tabs.add(self.tab2, text="TC Configure")
        self.TC = None
        self.TC_original = None
        self.TC_selected = {}
        self.TC_result = []
        self.initUI()
        self.ConfV = {}
        self.config = None
        self.charger = None
        self.status = None

    def init_result(self):
        self.TC_result = ['Not Tested' for _ in range(len(self.TC.keys()))]


    def initUI(self):
        def config_update():
            self.config = Config(wss_url=en_url.get(),
                            rest_url=en_rest_url.get(),
                            auth_token=en_token.get(),
                            en_status=en_status,
                            en_tr=en_tr,
                            en_tc=en_tc,
                            lst_cases=lst_cases,
                            txt_recv=txt_recv,
                            cid=en_cid.get(),
                            rcid = en_rcid.get(),
                            sno = en_sno.get(),
                            rsno = en_rsno.get(),
                            mdl = en_mdl.get(),
                            result=self.TC_result,
                            confV=self.ConfV,
                            en_reserve = en_reserve.get(),
                            lst_tc = lst_tc,
                            test_mode = vmode.get()
                            )
            self.ConfV = {'$idTag1': en_idtag1, '$idTag2': en_idtag2, '$idTag3': en_idtag3,
                          '$ctime': en_timestamp1, '$ctime+$interval1': en_timestamp2,
                          '$ctime+$interval2': en_timestamp3, '$crgr_mdl':en_mdl, '$crgr_sno':en_sno, '$crgr_rsno':en_rsno}

            #self.charger.update_config(self.config)
            self.status = 1

        ConfRV = {}
        def tc_render(adict, k):
            import datetime
            if isinstance(adict, dict):
                for key in adict.keys():
                    if adict[key] == k:
                        try:
                            adict[key] = ConfRV[k]
                        except ValueError:
                            pass  # do nothing if the timestamp is already in the correct format
                    elif isinstance(adict[key], (dict, list)):
                        tc_render(adict[key], k)
            elif isinstance(adict, list):
                for l in adict:
                    tc_render(l, k)

        import tkinter.ttk
        from tkinter import Label, Entry, Button, scrolledtext, Listbox, messagebox

        self.window.title("EV Charger Simulator (nheo.an@gmail.com)")
        self.window.geometry("1160x955+500+100")
        self.window.resizable(True, True)
        frameTop = LabelFrame(self.tab1, text="Configuration", padx=10, pady=5)
        frameTop.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        frameBot = LabelFrame(self.tab1, text="Log Output", padx=10, pady=5)
        frameBot.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)
        frameConfTop = LabelFrame(self.tab2, text="Basic Configuration", padx=10, pady=10)
        frameConfTop.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        frameConfBot = LabelFrame(self.tab2, text="Custom Configuration", padx=10, pady=10)
        frameConfBot.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

        lst_cases = Listbox(frameTop, height=7, selectmode="extended", activestyle="none")

        def tcload_callback():
            try :
                en_log.delete(0, END)
                self.TC = json.loads(open(fd.askopenfilename(initialdir=".",
                                         title="Select TC cases (json)",
                                         filetypes=(("Json files", "*.json"),
                                                    ("txt files", "*.txt"))),encoding="UTF-8").read())
                self.init_result()
            except Exception as err:
                en_log.insert(0, "Please Check your TC json file.")
                return

            lst_cases.delete(0,END)
            for item in self.TC.keys():
                lst_cases.insert(END, item )

        menubar = Menu(self.window)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Load TC (Json)", command=tcload_callback)
        menu1.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=menu1)
        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="About")
        menubar.add_cascade(label="About", menu=menu2)
        self.window.config(menu=menubar)



        txt_tc = scrolledtext.ScrolledText(frameTop, width=50, height=15)
        txt_schema = scrolledtext.ScrolledText(frameTop, width=50, height=15)
        lb_schema = Label(frameTop, text="OCPP Schema", width=10)
        lst_tc = Listbox(frameTop, height=7, selectmode="extended", activestyle="none", width=70)
        lb_txt_tc = Label(frameTop, text="OCPP Template", width=10)

        txt_log = scrolledtext.ScrolledText(frameBot, width=143, height=9)
        txt_recv = scrolledtext.ScrolledText(frameBot, width=143, height=15)
        txt_recv.tag_config('blue', foreground='blue')
        txt_recv.tag_config('green', foreground='green')
        txt_recv.tag_config('red', foreground='red')

        # Create textLogger
        text_handler = TextHandler(txt_log)

        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(text_handler)
        self.status = 0

        async def startEvent():
            # if self.status == 0:
            #     messagebox.showwarning(title="소켓연결", message="소켓 연결 후 시작 하십시오")
            #     #     messagebox.showwarning("소켓 연결 후 TC실행 해 주세요", "경고")
            #     return
            #
            # self.status=0
            bt_conn['state'] = tk.NORMAL

            config_update()
            TC_update()
            en_log.delete(0, END)
            en_status.delete(0, END)
            en_status.insert(0, "Running")
            self.charger = Charger(self.config)
            await self.charger.runcase(self.TC_selected if len(self.TC_selected.keys())>0 else self.TC)
            en_status.delete(0, END)
            en_status.insert(0, "Test Finished")
            bt_conn['state'] = tk.DISABLED

        async def closeEvent():
            if self.status == 0:
                messagebox.showwarning(title="소켓연결", message="소켓 연결 후 시작 하십시오")
                #     messagebox.showwarning("소켓 연결 후 TC실행 해 주세요", "경고")
                return
            await self.charger.close()
            status=0

        async def stopCharger():
            self.charger.stop()

        lb_log = Label(frameTop, text="로그", width=10)

        lb_url = Label(frameTop, text="WSS URL", width=10)
        lb_rest_url = Label(frameTop, text="REST URL", width=10)
        lb_cases = Label(frameTop, text="Test Case", width=10)


        en_url = Entry(frameTop, width=60)
        en_rest_url = Entry(frameTop, width=60)

        en_mdl = Entry(frameTop)
        en_mdl.insert(0, "ELA007C01")
        en_url.insert(0,"wss://ws.devevspcharger.uplus.co.kr/ocpp16")
        en_rest_url.insert(0, 'https://8b434254zg.execute-api.ap-northeast-2.amazonaws.com/dev/ioc')
        lb_case = Label(frameTop, text="TC Body")

       # txt_tc.config(state=tk.DISABLED)

        lb_sno = Label(frameTop, text="충전기ID(일반)")
        lb_rsno = Label(frameTop, text="충전기ID(예약)")
        lb_mdl = Label(frameTop, text="모델ID")
        lb_cid = Label(frameTop, text="충전기CID(일반)", width=13)
        lb_rcid = Label(frameTop, text="충전기CID(예약)", width=13)
        en_sno = Entry(frameTop)
        en_sno.insert(0, "EVSCA070007")
        en_rsno = Entry(frameTop)
        en_rsno.insert(0, "EVSCA070008")
        en_cid = Entry(frameTop)
        en_cid.insert(0, "115001513031A")
        en_rcid = Entry(frameTop)
        en_rcid.insert(0, "115001513041A")

        lb_url_comp = Label(frameTop, text=en_url.get()+"/"+en_mdl.get()+"/"+en_sno.get())

        en_log = Entry(frameTop)



        lb_token = Label(frameTop, text="Auth Token")
        lb_tr = Label(frameTop, text="transactionId", width=10)
        en_tr = Entry(frameTop)
        en_token = Entry(frameTop)
        en_token.insert(0, 'Basic RVZBUjpFVkFSTEdV')
        lb_reserve = Label(frameTop, text="reserveId", width=10)
        en_reserve = Entry(frameTop)
        lb_status = Label(frameTop, text="Status", width=10)

        en_status = Entry(frameTop)
        en_status.insert(0, 'Idle')

        lb_tc = Label(frameTop, text="Current TC", width=10)
        en_tc = Entry(frameTop)
        en_tc.config(state='disabled')

        lb_sno.grid(row=0, column=0, sticky="we")
        lb_rsno.grid(row=1, column=0, sticky="we")
        lb_mdl.grid(row=2, column=0, sticky="we")
        lb_url.grid(row=3, column=0, sticky="we")
        lb_rest_url.grid(row=5, column=0, sticky="we")


        lb_log.grid(row=7, column=0, sticky="we")

        en_sno.grid(row=0, column=1, sticky="we")
        en_rsno.grid(row=1, column=1, sticky="we")
        en_mdl.grid(row=2, column=1, sticky="we")
        en_url.grid(row=3, column=1, sticky="we")
        lb_url_comp.grid(row=4, column=1, sticky="w")
        en_rest_url.grid(row=5, column=1, sticky="we")
        lb_cases.grid(row=6, column=0, sticky="we")
        lst_cases.grid(row=6, column=1, sticky="we")
        en_log.grid(row=7, column=1, sticky="we")
        lb_schema.grid(row=8, column=0, sticky="we")
        txt_schema.grid(row=8, column=1, sticky="we")


        lb_cid.grid(row=0, column=2, sticky="we")
        en_cid.grid(row=0, column=3, sticky="we")
        lb_rcid.grid(row=1, column=2, sticky="we")
        en_rcid.grid(row=1, column=3, sticky="we")
        lb_token.grid(row=2, column=2, sticky="we")
        en_token.grid(row=2, column=3, sticky="we")
        lb_tr.grid(row=3, column=2, sticky="we")
        en_tr.grid(row=3, column=3, sticky="we")
        lb_reserve.grid(row=4, column=2, sticky="we")
        en_reserve.grid(row=4, column=3, sticky="we")
        lb_status.grid(row=5, column=2, sticky="we")
        en_status.grid(row=5, column=3, sticky="we")

        lb_case.grid(row=6, column=2)
        txt_tc.grid(row=8, column=3, rowspan=3, sticky="we")
        lb_txt_tc.grid(row=8, column=2, sticky="we")

        lst_tc.grid(row=6, column=3, sticky="we")

        lb_tc.grid(row=7, column=2, sticky="we")
        en_tc.grid(row=7, column=3, sticky="we")


        lb_txt = Label(frameBot, text="실행로그", width=10)
        lb_recv = Label(frameBot, text="송수신로그", width=10)

        lb_txt.grid(row=0, column=0)
        txt_log.grid(row=0, column=1, columnspan=3)
        s=tk.ttk.Separator(frameBot, orient="horizontal")
        s.grid(row=1, column=1, sticky='ew', columnspan=3)
        lb_recv.grid(row=2, column=0)
        txt_recv.grid(row=2, column=1, columnspan=3)


        """Configuration Tab"""
        """========================================================="""

        lb_idtag1 = Label(frameConfTop, text="idTag1", width=20)
        en_idtag1 = Entry(frameConfTop)
        lb_idtag2 = Label(frameConfTop, text="idTag2", width=20)
        en_idtag2 = Entry(frameConfTop)
        lb_idtag3 = Label(frameConfTop, text="idTag3", width=20)
        en_idtag3 = Entry(frameConfTop)

        lb_idtag1.grid(row=0, column=0)
        lb_idtag2.grid(row=1, column=0)
        lb_idtag3.grid(row=2, column=0)
        en_idtag1.grid(row=0, column=1)
        en_idtag1.insert(0, '1031040000069641')
        en_idtag2.grid(row=1, column=1)
        en_idtag3.grid(row=2, column=1)
        lb_timestamp1 = Label(frameConfTop, text="$ctime", width=25)
        en_timestamp1 = Entry(frameConfTop)
        lb_timestamp2 = Label(frameConfTop, text="($ctime+$interval1) - seconds", width=25)
        en_timestamp2 = Entry(frameConfTop)
        lb_timestamp3 = Label(frameConfTop, text="($ctime+$interval2) - seconds", width=25)
        en_timestamp3 = Entry(frameConfTop)
        lb_timestamp1.grid(row=0, column=2)
        lb_timestamp2.grid(row=1, column=2)
        lb_timestamp3.grid(row=2, column=2)
        en_timestamp1.grid(row=0, column=3)
        en_timestamp2.grid(row=1, column=3)
        en_timestamp3.grid(row=2, column=3)
        rdo_frame = Frame(frameTop)
        rdo_frame.grid(row=12, column=0, columnspan=4, sticky="W", padx=10, pady=10)
        bt_frame = Frame(frameTop)
        bt_frame.grid(row=13, column=0, columnspan=4, sticky="W", padx=10, pady=10)
        vmode = IntVar()
        lb_mode = Label(rdo_frame, text="Test Mode")
        lb_mode.grid(row=0, column=0)
        test_mode1 = Radiobutton(rdo_frame, text="Local", variable=vmode, value=1)
        test_mode2 = Radiobutton(rdo_frame, text="CSMS", variable=vmode, value=2)
        test_mode1.grid(row=0, column=1)
        test_mode2.grid(row=0, column=2)
        vmode.set(1)
        bt_conn = Button(bt_frame, text="일시중지", command=async_handler(stopCharger), state=DISABLED, width=15)
        bt_start = Button(bt_frame, text="TC 실행", command=async_handler(startEvent), width=15)
        bt_reload = Button(bt_frame, text="JsonReload", width=15)
        bt_close = Button(bt_frame, text="종료", command=async_handler(closeEvent), width=15)
        bt_conn.grid(row=1, column=0, ipady=3, pady=3, sticky="w")
        bt_start.grid(row=1, column=1, ipady=3, pady=3, sticky="w")
        bt_reload.grid(row=1, column=2, ipady=3, pady=3, sticky="w")
        bt_close.grid(row=1, column=3, ipady=3, pady=3, sticky="E")

        self.ConfV = {'$idTag1': en_idtag1, '$idTag2': en_idtag2, '$idTag3': en_idtag3,
                      '$ctime': en_timestamp1, '$ctime+$interval1': en_timestamp2,
                      '$ctime+$interval2': en_timestamp3, '$crgr_mdl': en_mdl, '$crgr_sno': en_sno,
                      '$crgr_rsno': en_rsno}


        def wssRenew(event):
            lb_url_comp.config(text=en_url.get()+'/'+en_mdl.get()+'/'+en_sno.get())

        def onSelect(event):
            w = event.widget
            self.TC_selected ={}
            for s in w.curselection():
                self.TC_selected[w.get(s).split()[0]] = self.TC[w.get(s).split()[0]]
                en_tc.config(state='normal')
                en_tc.delete(0,END)
                en_tc.insert(0,w.get(s).split())
                en_tc.config(state='disabled')
            if w.curselection() :
                index = int(w.curselection()[0])
                en_log.delete(0,END)
                en_log.insert(END, self.TC_result[index])
                lst_tc.delete(0,END)
                for c in self.TC_selected :
                    for tc in self.TC_original[c]:
                        lst_tc.insert(END, tc)

        def onSelectTcItem(event):
            w = event.widget

            items= [ w.get(s) for s in w.curselection() ]
            if not items :
                return

            text_item = {}
            for item in items :
                if item[0] == 'Wait' :
                    text_item[item[1]]=props.ocppDocs[item[1]]
                elif item[0] == 'Reply' :
                    text_item[item[1]+'Response']=props.ocppDocs[item[1]+'Response']
                else :
                    text_item[item[0]]=props.ocppDocs[item[0]]

            txt_tc.delete(1.0, END)
            txt_tc.insert(END, json.dumps(text_item, indent=2))

            schemas = ""
            for msgid in text_item.keys():
                schemas+=open(f"./schemas/{msgid}.json", encoding='utf-8').read()

            txt_schema.delete(1.0, END)
            txt_schema.insert(END, json.dumps(json.loads(schemas), indent=2))

        def TC_update():
            from datetime import timedelta
            ctime = datetime.now().isoformat(sep='T', timespec='seconds')+'Z'
            try :
                for v in self.ConfV.keys():
                    #print(self.ConfV[v].get())
                    if v == "$ctime" :

                        ConfRV[v] = ctime
                    elif v == "$ctime+$interval1" and len(self.ConfV[v].get()) > 0:
                        ConfRV[v] = (datetime.now() +
                                          timedelta(seconds=int(self.ConfV[v].get()))).isoformat(sep='T',
                                                                                            timespec='seconds')+'Z'
                    elif v == "$ctime+$interval2" and len(self.ConfV[v].get()) > 0:
                        ConfRV[v] = (datetime.now() +
                                         timedelta(seconds=int(self.ConfV[v].get()))).isoformat(sep='T',
                                                                                           timespec='seconds')+'Z"'
                    else:
                        ConfRV[v] = self.ConfV[v].get()
                    tc_render(self.TC, v)
            except ValueError as err:
                vtmp = ''.join(c for c in self.ConfV[v].get() if c.isdigit())
                self.ConfV[v].delete(0,END)
                self.ConfV[v].insert(0,vtmp)
        def load_default_tc():
            print("load_default_tc")
            try :
                en_log.delete(0, END)
                self.TC = json.loads(open("./props.json", encoding='utf-8').read())
                self.TC_original = self.TC
                self.init_result()
            except Exception as err:
                en_log.insert(0, "Please Check your TC json file.")
                return
            lst_cases.delete(0,END)
            for item in self.TC.keys():
                lst_cases.insert(END, item )

            self.init_result()
        # def onEnter(event):
        #     index = event.widget.index("%s, %s" %(event.x, event.y))

        """props.json 파일(기본TC파일) 로드"""
        def reload_tc(event) :
            load_default_tc()

        load_default_tc()

        en_sno.bind('<KeyRelease>', wssRenew)
        en_mdl.bind('<KeyRelease>', wssRenew)
        lst_cases.bind('<<ListboxSelect>>', onSelect)
        lst_tc.bind('<<ListboxSelect>>', onSelectTcItem)
        txt_schema.bind("<Key>", lambda e: "break")
        bt_reload.bind("<Button-1>", reload_tc)
        # lst_tc.bind('<Enter>', onEnter)
        # en_idtag1.bind('<KeyRelease>', onChangeConfig)
        # en_idtag2.bind('<KeyRelease>', onChangeConfig)
        # en_idtag3.bind('<KeyRelease>', onChangeConfig)
        # en_timestamp2.bind('<KeyRelease>', onChangeConfig)
        # en_timestamp3.bind('<KeyRelease>', onChangeConfig)

        def set_time_label():
            from datetime import datetime
            currentTime = datetime.now().isoformat(sep='T', timespec='seconds')+'Z'
            en_timestamp1.delete(0, END)
            en_timestamp1.insert(0, currentTime)
            self.window.after(1, set_time_label)


        set_time_label()
        async_mainloop(self.window)
def main(async_loop):
    import time
    me = MyApp()

if __name__ == "__main__":
    # async_loop = asyncio.get_event_loop()
    async_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(async_loop)
    main(async_loop)
