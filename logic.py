import json
import mido
from mido import Message

keylist = json.load(open("keylist.json", "r"))
ports = mido.get_output_names()
outport = mido.open_output(ports[0])

def channel_setting(ch):
    pg=keylist["Channel"][ch]
    outport.send(Message("program_change",channel=ch,program=pg))

def json_reload():
    json_open = open("keylist.json", "r")
    global json_load
    json_load = json.load(json_open)
    print(json_load["Righthand"])

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
    print(path, righthand, json_load["Righthand"][righthand])
    outport.send(Message(json_load["Righthand"][righthand][1],
    channel=json_load["Righthand"][righthand][2],
    note   =json_load["Righthand"][righthand][3]))
    
def midiL(path, lefthand=0):
    print(path, lefthand, json_load["Lefthand"][lefthand])
    outport.send(Message(json_load["Lefthand"][lefthand][1],
    channel=json_load["Lefthand"][lefthand][2],
    note   =json_load["Lefthand"][lefthand][3]))