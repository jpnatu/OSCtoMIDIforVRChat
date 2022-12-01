import json
import threading
import tkinter as tk
import tkinter.ttk as ttk

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

import logic


def main():
    oscserver = threading.Thread(target=osc_serve,daemon=True)
    oscserver.start()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

# Tk.Frameを継承したApplicationクラスの作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # ウィンドウの設定
        self.master.minsize(width=500, height=300)
        self.master.title('OSCtoMIDIforVRC')
        self.pack(fill=tk.BOTH, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.widget_port()
        self.widget_left()
        self.widget_right()
        self.widget_channel()
        global keylist
        keylist = json.load(open("keylist.json", "r"))

    # ポート選択ウィジェット     
    def widget_port(self):
        frame1 = tk.Frame(self, bg="red", background="#61a4e0")
        frame1.pack(side=tk.LEFT, fill=tk.BOTH)
        label1 = tk.Label(frame1, text="Avalable Ports")
        label1.pack(side=tk.TOP, padx=10, pady=10)

        # ポート選択時のイベント
        def lb1select(self):
            # 選択インデックス取得
            selectedind = listbox1.curselection()
            # ポート変更
            logic.portschange(listbox1.index(selectedind))

        # listbox
        listvalue = logic.portscheck()
        var = tk.StringVar(value=listvalue)
        listbox1 = tk.Listbox(frame1, selectmode="single",
                              width=30, listvariable=var)

        listbox1.pack(side=tk.TOP, padx=10)
        listbox1.bind('<<ListboxSelect>>', lb1select)

    # 左手のトリガー設定
    def widget_left(self):
        frame2 = tk.Frame(self, bg="green")
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        label2 = tk.Label(frame2, text="Left hand settings")
        label2.pack(side=tk.TOP, padx=10,pady=10)      

    # 右手のトリガー設定
    def widget_right(self):
        handsign = ["default", "fist", "HandOpen","FingerPoint",
                    "Victory", "RocknRoll","Handgun", "ThumbsUp"]
        channelvalue=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16    
        # フレーム
        frame3 = tk.Frame(self, bg="orange")
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        label3 = tk.Label(frame3, text="Right hand settings")
        label3.pack(side=tk.TOP, padx=10,pady=10)
        labelframe1 = tk.LabelFrame(frame3, labelanchor="nw", text="Settings")
        labelframe1.pack(side=tk.BOTTOM, fill=tk.BOTH,
                         expand=True, padx=10, pady=10)

        # ハンドサイン選択
        label3_1 = tk.Label(labelframe1, text="割り当てるハンドサイン")
        label3_1.pack(side=tk.TOP, anchor=tk.W, padx=5)
        cb3_1 = ttk.Combobox(labelframe1, state="readonly",value=handsign)
        cb3_1.pack(side=tk.TOP, fill=tk.X)

        # # メッセージタイプ選択
        # label3_2 = tk.Label(labelframe1, text="Message Type")
        # label3_2.pack(side=tk.TOP, anchor=tk.W, padx=5)
        # cb3_3 = ttk.Comboboex(labelframe1, state="readonly")
        # cb3_3.pack(side=tk.TOP, fill=tk.X)

        # 送信チャンネル選択
        label3_3 = tk.Label(labelframe1, text="送るチャンネル")
        label3_3.pack(side=tk.TOP, anchor=tk.W, padx=5)
        cb3_2 = ttk.Combobox(labelframe1, state="readonly",value=channelvalue)
        cb3_2.pack(side=tk.TOP, fill=tk.X)

        # # メッセージタイプ選択
        # label3_3 = tk.Label(labelframe1, text="Message Type")
        # label3_3.pack(side=tk.TOP, anchor=tk.W, padx=5)
        # cb3_3 = ttk.Combobox(labelframe1, state="readonly")
        # cb3_3.pack(side=tk.TOP, fill=tk.X)

        # ノート選択
        label3_4 = tk.Label(labelframe1, text="ノート番号")
        label3_4.pack(side=tk.TOP, anchor=tk.W, padx=5)
        entNote_R = tk.Entry(labelframe1)
        entNote_R.pack(side=tk.TOP, fill=tk.X)
        
        # JSONかきこみ
        def Writetojson():
            keylist["Righthand"][cb3_1.current()] = \
            cb3_1.get(),"note_on",cb3_2.current(),int(entNote_R.get()),
            
            print(keylist["Righthand"][cb3_1.current()])
            with open("keylist.json", "w") as outfile:
                json.dump(keylist, outfile, indent=4)
            logic.json_reload()

        btn2 = tk.Button(labelframe1,text="Write and Reload",command=Writetojson)
        btn2.pack(side=tk.TOP)

    # チャンネルのトリガー設定
    def widget_channel(self):
        frame = tk.Frame(self, bg="gray")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        label = tk.Label(frame, text="Channel settings")
        label.pack(side=tk.TOP, padx=10,pady=10)
        labelframe = tk.LabelFrame(frame, labelanchor="nw", text="Settings")
        labelframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        # チャンネル選択
        label3_1 = tk.Label(labelframe, text="チャンネル番号")
        label3_1.pack(side=tk.TOP, anchor=tk.W, padx=5)
        cb1 = ttk.Combobox(labelframe, state="readonly",value=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        cb1.pack(side=tk.TOP, fill=tk.X)
        # プログラムチェンジ
        label3_4 = tk.Label(labelframe, text="プログラムチェンジ")
        label3_4.pack(side=tk.TOP, anchor=tk.W, padx=5)
        entPC = tk.Entry(labelframe)
        entPC.pack(side=tk.TOP, fill=tk.X)

        # JSON書き込み
        def Writetojson():
            keylist["Channel"][cb1.current()] = int(entPC.get())
            print(keylist["Channel"])
            with open("keylist.json", "w") as outfile:
                json.dump(keylist, outfile, indent=4)
            logic.channel_setting(int(cb1.current()))

        btn2 = tk.Button(labelframe,text="Reload",command=Writetojson)
        btn2.pack(side=tk.TOP)

    # 終了処理
    def delete_window(self):
        self.master.destroy()

# VRCからのOSCを受け取るサーバー
def osc_serve():
    ip, port, dispatcher= "127.0.0.1", 9001, Dispatcher()
    dispatcher.map("/avatar/parameters/GestureRight", logic.midiR)
    dispatcher.map("/avatar/parameters/GestureLeft", logic.midiL)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()

if __name__ == "__main__":
    main()