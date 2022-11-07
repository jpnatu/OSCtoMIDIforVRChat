from modulefinder import Module
import tkinter as tk
from tkinter import CENTER, NW, RIGHT, Button, ttk
from tkinter.messagebox import showinfo
from unittest import mock
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import logic

def main():
    # いったんOSC無効化
    # th1 = threading.Thread(target=osc_serve)
    # th1.start()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

# Tk.Frameを継承したApplicationクラスの作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=300)

        #ウィンドウの設定
        self.master.title('OSCtoMIDIforVRC')
        self.pack()
        self.create_widget()

    #ウィジェットの作成
    def create_widget(self):
        
        # ポート選択時のイベント
        def selected(self):
            # 選択インデックス取得
            num = lb1.curselection()
            # ポート変更
            logic.portschange(lb1.index(num))
            # デバッグ
            print(lb1.get(num))
        
        # frame1と出力先選択用のlistbox作成
        frame1 = tk.Frame(self.master)

        # listboxの中身（ポート一覧）
        listvalue = logic.portscheck()
        var = tk.StringVar(value=listvalue)
        lb1 = tk.Listbox(frame1,width=30,listvariable=var)
        
        lb1.pack()
        frame1.pack()
        lb1.bind('<<ListboxSelect>>', selected)
        

        
# VRCからのOSCを受け取る
def osc_serve():
    ip, port = "127.0.0.1", 9001
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/GestureRight", logic.midiR)
    dispatcher.map("/avatar/parameters/GestureLeft", logic.midiL)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == "__main__":
    main()