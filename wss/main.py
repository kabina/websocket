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
sys.setrecursionlimit(10**6)

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
        self.tabs.add(self.tab2, text="TC Configuration")
        self.TC = None
        self.TC_selected = {}
        self.TC_result = []
        self.initUI()
        self.ConfV = {}

    def init_result(self):
        self.TC_result = ['Not Tested' for _ in range(len(self.TC.keys()))]

    def initUI(self):
        
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
        from tkinter import Label, Entry, Button, scrolledtext, Listbox

        self.window.title("EV Charger Simulator (nheo.an@gmail.com)")
        self.window.geometry("1024x768+800+800")
        self.window.resizable(True, True)
        frameTop = LabelFrame(self.tab1, text="Configuration", padx=20, pady=20)
        frameTop.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        frameBot = LabelFrame(self.tab1, text="Log Output", padx=20, pady=20)
        frameBot.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)
        frameConfTop = LabelFrame(self.tab2, text="Basic Configuration", padx=20, pady=20)
        frameConfTop.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        frameConfBot = LabelFrame(self.tab2, text="Custom Configuration", padx=20, pady=20)
        frameConfBot.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)
        lst_cases = Listbox(frameTop, height=10, selectmode="extended", activestyle="none")

        self.TC = props.TC
        self.init_result()
        def enter_only_digits(self, entry, action_type) -> bool:
            if action_type == '1' and not entry.isdigit():
                return False

            return True
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



        txt_tc = scrolledtext.ScrolledText(frameTop, width=50, height=12)
        txt_log = scrolledtext.ScrolledText(frameBot, width=127, height=9)
        txt_recv = scrolledtext.ScrolledText(frameBot, width=127, height=13)
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

        async def startEvent():

            config = Config(wss_url = lb_url_comp["text"],
                            rest_url = en_rest_url.get(),
                            auth_token=en_token.get(),
                            en_status=en_status,
                            en_tr = en_tr,
                            en_tc = en_tc,
                            lst_cases = lst_cases,
                            txt_recv=txt_recv,
                            cid=en_cid.get(),
                            result=self.TC_result,
                            )
            charger = Charger(config)
            await charger.conn()
            en_log.delete(0, END)
            en_status.delete(0, END)
            en_status.insert(0, "Running")
            #target_tc = {tc:self.TC[tc] for tc in self.TC_selected} if len(self.TC_selected)>0 else self.TC

            await charger.runcase(self.TC_selected if len(self.TC_selected.keys())>0 else self.TC)
            en_status.delete(0, END)
            en_status.insert(0, "Test Finished")


        for item in props.TC.keys():
            lst_cases.insert(END, item )



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
        lb_case.grid(row=5, column=2)
        txt_tc.grid(row=5, column=3)
       # txt_tc.config(state=tk.DISABLED)

        lb_cid = Label(frameTop, text="충전기ID")
        lb_mdl = Label(frameTop, text="모델ID")
        en_cid = Entry(frameTop)
        en_cid.insert(0, "EVSCA070007")

        lb_url_comp = Label(frameTop, text=en_url.get()+"/"+en_mdl.get()+"/"+en_cid.get())

        en_log = Entry(frameTop)

        bt_start = Button(frameTop, text="시작", command=async_handler(startEvent))
        lb_token = Label(frameTop, text="Auth Token")
        lb_tr = Label(frameTop, text="transactionId", width=10)
        en_tr = Entry(frameTop)
        en_token = Entry(frameTop)
        en_token.insert(0, 'Basic RVZBUjpFVkFSTEdV')
        lb_status = Label(frameTop, text="Status", width=10)
        en_status = Entry(frameTop)
        en_status.insert(0, 'Idle')

        lb_tc = Label(frameTop, text="Current TC", width=10)
        en_tc = Entry(frameTop)

        lb_cid.grid(row=0, column=0, sticky="we")
        lb_mdl.grid(row=1, column=0, sticky="we")
        lb_url.grid(row=2, column=0, sticky="we")
        lb_rest_url.grid(row=4, column=0, sticky="we")

        lb_cases.grid(row=5, column=0, sticky="we")
        lb_log.grid(row=6, column=0, sticky="we")

        en_cid.grid(row=0, column=1, sticky="we")
        en_mdl.grid(row=1, column=1, sticky="we")
        en_url.grid(row=2, column=1, sticky="we")
        lb_url_comp.grid(row=3, column=1, sticky="w")
        en_rest_url.grid(row=4, column=1, sticky="we")


        lst_cases.grid(row=5, column=1, sticky="we")
        en_log.grid(row=6, column=1, sticky="we")
        bt_start.grid(row=7, column=0, sticky="we")
        lb_token.grid(row=0, column=2, sticky="we")
        en_token.grid(row=0, column=3)
        lb_tr.grid(row=1, column=2, sticky="we")
        en_tr.grid(row=1, column=3)
        lb_tc.grid(row=2, column=2, sticky="we")
        en_tc.grid(row=2, column=3)
        lb_status.grid(row=3, column=2, sticky="we")
        en_status.grid(row=3, column=3)


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
        vcmd = (self.window.register(enter_only_digits), '%P', '%d')

        lb_idtag1.grid(row=0, column=0)
        lb_idtag2.grid(row=1, column=0)
        lb_idtag3.grid(row=2, column=0)
        en_idtag1.grid(row=0, column=1)
        en_idtag1.insert(0, '1031040000069641')
        en_idtag2.grid(row=1, column=1)
        en_idtag3.grid(row=2, column=1)
        lb_timestamp1 = Label(frameConfTop, text="$ctime", width=25)
        en_timestamp1 = Entry(frameConfTop)
        lb_timestamp2 = Label(frameConfTop, text="$ctime+$interval1) - seconds", width=25)
        en_timestamp2 = Entry(frameConfTop)
        lb_timestamp3 = Label(frameConfTop, text="$ctime+$interval2) - seconds", width=25)
        en_timestamp3 = Entry(frameConfTop)
        lb_timestamp1.grid(row=0, column=2)
        lb_timestamp2.grid(row=1, column=2)
        lb_timestamp3.grid(row=2, column=2)
        en_timestamp1.grid(row=0, column=3)
        en_timestamp2.grid(row=1, column=3)
        en_timestamp3.grid(row=2, column=3)

        self.ConfV = {'$idTag1':en_idtag1, '$idTag2':en_idtag2, '$idTag3':en_idtag3,
                      '$ctime':en_timestamp1, '$ctime+$interval1':en_timestamp2,
                      '$ctime+$interval2':en_timestamp3}


        def wssRenew(event):
            #text = event.widget.get()
            lb_url_comp.config(text=en_url.get()+'/'+en_mdl.get()+'/'+en_cid.get())
        def onSelect(event):
            w = event.widget
            self.TC_selected ={}
            for s in w.curselection():
                self.TC_selected[w.get(s).split()[0]] =self.TC[w.get(s).split()[0]]
            if w.curselection() :
                index = int(w.curselection()[0])
                en_log.delete(0,END)
                en_log.insert(END, self.TC_result[index])
                value = w.get(index)
                txt_tc.delete(1.0,END)
                text = self.TC[value.split()[0]]
                txt_tc.insert(END, json.dumps(text, indent=2))
        def onChangeConfig(event):
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

        en_cid.bind('<KeyRelease>', wssRenew)
        en_mdl.bind('<KeyRelease>', wssRenew)
        lst_cases.bind('<<ListboxSelect>>', onSelect)
        en_idtag1.bind('<KeyRelease>', onChangeConfig)
        en_idtag2.bind('<KeyRelease>', onChangeConfig)
        en_idtag3.bind('<KeyRelease>', onChangeConfig)
        def set_time_label():
            from datetime import datetime
            currentTime = datetime.now().isoformat(sep='T', timespec='seconds')+'Z'
            en_timestamp1.delete(0, END)
            en_timestamp1.insert(0, currentTime)
            self.window.after(1, set_time_label)

        en_timestamp2.bind('<KeyRelease>', onChangeConfig)
        en_timestamp3.bind('<KeyRelease>', onChangeConfig)
        set_time_label()
        async_mainloop(self.window)
def main(async_loop):
    import time
    me = MyApp()

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()
    main(async_loop)
