import json
import mido
from mido import Message

keylist = json.load(open("keylist.json", "r"))
ports = mido.get_output_names()
outport = mido.open_output(ports[0])
number = 0
while number <=16:
    outport.send(Message("program_change",
    channel=number,
    program=keylist["Channel"][number]))
    

def channel_setting(ch):
    pg=keylist["Channel"][ch]
    outport.send(Message("program_change",channel=ch,program=pg))

def json_reload():
    json.load(open("keylist.json", "r"))

# ポート管理
def portscheck():
    gotports = mido.get_output_names()
    return(gotports)

# ポート変更
def portschange(portnum):
    global outport
    outport.close()
    outport = mido.open_output(ports[portnum])
    print(f"Succesfully opened port[{ports[portnum]}]")

# 押されたときの処理関数
def midiR(path, righthand=0):
    print(path, righthand, keylist["Righthand"][righthand])
    outport.send(Message(keylist["Righthand"][righthand][1],
    channel=keylist["Righthand"][righthand][2],
    note   =keylist["Righthand"][righthand][3]))
    
def midiL(path, lefthand=0):
    print(path, lefthand, keylist["Lefthand"][lefthand])
    outport.send(Message(keylist["Lefthand"][lefthand][1],
    channel=keylist["Lefthand"][lefthand][2],
    note   =keylist["Lefthand"][lefthand][3]))