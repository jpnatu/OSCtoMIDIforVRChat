import tkinter as tk
from tkinter import CENTER, NW, Button, ttk
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import logic

ip, port = "127.0.0.1", 9001


def main():
    th1 = threading.Thread(target=osc_serve)
    th1.start()
    win = tk.Tk()
    app = Frame1(master=win)
    app.mainloop()

# https://denno-sekai.com/tkinter-frame/
# Frame1クラスの作成


class Frame1(tk.Frame):
    def __init__(self, master):  # コンストラクタを定義
        super().__init__(master)  # 継承元クラス（tk.Frame）のコンストラクタを呼び出し

        # ウィンドウの設定
        master.title('OSCtoMIDIforVRC')
        master.geometry("800x500")

        # フレームの設定
        self.config(bg="#4682b4")  # 背景色を指定
        self.pack()

        keyframe = tk.Frame(master)
        keyframe.pack(fill=tk.BOTH, anchor=tk.CENTER)

        # keyBK = tk.Frame(keyframe, relief="ridge")
        # notelist = ("C", "D", "F", "G", "A")
        # for note in notelist:
        #     btn = tk.Button(keyBK, background="black", fg="White",
        #                     text=note, font=("MSゴシック", "20"))
        #     btn.pack(side=tk.LEFT)
        # keyBK.pack(anchor=tk.CENTER)

        # keyWH = tk.Frame(keyframe, relief="ridge")
        # notelist = ("C", "D", "E", "F", "G", "A", "B")
        # for note in notelist:
        #     btn = tk.Button(keyWH, text=note, font=("MSゴシック", "20"))
        #     btn.pack(side=tk.LEFT)
        # keyWH.pack(anchor=tk.CENTER)


def osc_serve():
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/GestureRight", logic.midiR)
    dispatcher.map("/avatar/parameters/GestureLeft", logic.midiL)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


if __name__ == "__main__":
    main()
