import tkinter as tk
import threading
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import logic

def main():
    global oscserver
    oscserver = threading.Thread(target=osc_serve,daemon=True)
    oscserver.start()
    root = tk.Tk()
    root.minsize(width=500, height=300)
    app = Application(master=root)
    app.mainloop()

# Tk.Frameを継承したApplicationクラスの作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ウィンドウの設定
        self.master.title('OSCtoMIDIforVRC')
        # メインフレームの配置
        self.pack(fill=tk.BOTH, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.create_widget()

    # ウィジェットの作成
    def create_widget(self):

        # frame1
        frame1 = tk.Frame(self, bg="red",background="#61a4e0")
        frame1.pack(side=tk.LEFT, fill=tk.BOTH)

        label1 = tk.Label(frame1, text="Avalable Ports")
        label1.pack(side=tk.TOP, padx=10,pady=10)
        
        # ポート選択時のイベント
        def selected(self):
            # 選択インデックス取得
            selectedind = listbox1.curselection()
            # ポート変更
            logic.portschange(listbox1.index(selectedind))

        # listbox
        listvalue = logic.portscheck()
        var = tk.StringVar(value=listvalue)
        listbox1 = tk.Listbox(frame1, selectmode="single",
                              width=30, listvariable=var)

        listbox1.pack(side=tk.TOP,padx=10)
        listbox1.bind('<<ListboxSelect>>', selected)


        frame2 = tk.Frame(self, bg="green")
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        label2 = tk.Label(frame2, text="Left hand settings")
        label2.pack(side=tk.TOP, padx=10,pady=10)

        frame3 = tk.Frame(self, bg="orange")
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        label3 = tk.Label(frame3, text="Right hand settings")
        label3.pack(side=tk.TOP, padx=10,pady=10)

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