import threading
import tkinter as tk

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

import logic

def main():
    th1 = threading.Thread(target=osc_serve)
    th1.start()
    root = tk.Tk()
    root.minsize(height=300, width=500)
    app = Application(master=root)
    app.mainloop()

# Tk.Frameを継承したApplicationクラスの作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=300)

        #ウィンドウの設定
        self.master.title('OSCtoMIDIforVRC')
        self.pack(fill=tk.BOTH) # メインフレームの配置
        self.create_widget()

    #ウィジェットの作成
    def create_widget(self):
        
        # listboxの親としてframe1
        frame1 = tk.Frame(self, bg="red")
        
        # ラベル
        label1 = tk.Label(frame1, text="Avalable Ports")

        # ポート選択時のイベント
        def selected(self):
            # 選択インデックス取得
            selectedind = listbox1.curselection()
            # ポート変更
            logic.portschange(listbox1.index(selectedind))

        # listboxの中身（ポート一覧）
        listvalue = logic.portscheck()
        var = tk.StringVar(value = listvalue)
        listbox1 = tk.Listbox(frame1, selectmode="single", width=30, listvariable=var)
        

        frame2 = tk.Frame(self, bg="green")
        label2 = tk.Label(frame2, text="Apple")


        # 配置
        frame1.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        label1.pack(side=tk.TOP)
        listbox1.pack(side=tk.TOP)
        listbox1.bind('<<ListboxSelect>>', selected)
        frame2.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y)
        label2.pack(side=tk.TOP)
        
# VRCからのOSCを受け取るサーバー
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