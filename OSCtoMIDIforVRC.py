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
        self.create_widget()

    #======================================
    #  ウィジェットの作成
    #======================================
    def create_widget(self):
        
        json_data = json.load(open("keylist.json", "r"))

        handsign = ["default", "fist", "HandOpen","FingerPoint",
                    "Victory", "RocknRoll","Handgun", "ThumbsUp"]
        channelvalue=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
        #-------------------------------------
        # frame1(ポート選択)
        #-------------------------------------
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
  
        #-------------------------------------
        # frame2(左手のトリガー)
        #-------------------------------------
        frame2 = tk.Frame(self, bg="green")
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        label2 = tk.Label(frame2, text="Left hand settings")
        label2.pack(side=tk.TOP, padx=10,pady=10)

        #-------------------------------------
        # frame3(右手のトリガー)
        #-------------------------------------     
        # フレーム
        frame3 = tk.Frame(self, bg="orange")
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        label3 = tk.Label(frame3, text="Right hand settings")
        label3.pack(side=tk.TOP, padx=10,pady=10)
        labelframe1 = tk.LabelFrame(frame3, labelanchor="nw", text="Settings")
        labelframe1.pack(side=tk.BOTTOM, fill=tk.BOTH,
                         expand=True, padx=10, pady=10)

        # ハンドサイン選択
        label3_1 = tk.Label(labelframe1, text="Whitch handsign to assign")
        label3_1.pack(side=tk.TOP, anchor=tk.W, padx=5)
        cb3_1 = ttk.Combobox(labelframe1, state="readonly",value=handsign)
        cb3_1.pack(side=tk.TOP, fill=tk.X)

        # 送信チャンネル選択
        label3_2 = tk.Label(labelframe1, text="To send channel")
        label3_2.pack(side=tk.TOP, anchor=tk.W, padx=5)
        cb3_2 = ttk.Combobox(labelframe1, state="readonly",value=channelvalue)
        cb3_2.pack(side=tk.TOP, fill=tk.X)

        # # メッセージタイプ選択
        # label3_3 = tk.Label(labelframe1, text="Message Type")
        # label3_3.pack(side=tk.TOP, anchor=tk.W, padx=5)
        # cb3_3 = ttk.Combobox(labelframe1, state="readonly")
        # cb3_3.pack(side=tk.TOP, fill=tk.X)

        # ノート選択
        label3_4 = tk.Label(labelframe1, text="Note number")
        label3_4.pack(side=tk.TOP, anchor=tk.W, padx=5)
        ent1 = tk.Entry(labelframe1)
        ent1.pack(side=tk.TOP, fill=tk.X)

        # プログラムチェンジ
        label3_5 = tk.Label(labelframe1, text="プログラムチェンジ")
        label3_5.pack(side=tk.TOP, anchor=tk.W, padx=5)
        entry_prgcng_R = tk.Entry(labelframe1)
        entry_prgcng_R.pack(side=tk.TOP, fill=tk.X)

        # JSONかきこみ
        def Writetojson():
            json_data = json.load(open("keylist.json", "r"))
            json_data["Righthand"][cb3_1.current()] = \
            cb3_1.get(),"note_on",cb3_2.current(), \
            int(entry_prgcng_R.get()),int(ent1.get()),
            
            print(json_data["Righthand"][cb3_1.current()])
            with open("keylist.json", "w") as outfile:
                json.dump(json_data, outfile, indent=4)

        btn2 = tk.Button(labelframe1,text="Write to JSON",command=Writetojson)
        btn2.pack(side=tk.TOP)
        btn3 = tk.Button(labelframe1,text="Reload JSON",command=logic.json_reload)
        btn3.pack(side=tk.TOP)

    # 終了処理
    def delete_window(self):
        self.master.destroy()

#======================================
# VRCからのOSCを受け取るサーバー
#======================================
def osc_serve():
    ip, port, dispatcher= "127.0.0.1", 9001, Dispatcher()
    dispatcher.map("/avatar/parameters/GestureRight", logic.midiR)
    dispatcher.map("/avatar/parameters/GestureLeft", logic.midiL)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()

if __name__ == "__main__":
    main()