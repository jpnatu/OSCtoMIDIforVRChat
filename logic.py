import json
import mido
from mido import Message

keylist = json.load(open("keylist.json", "r"))
print("Module_Logic has connected")
ports = mido.get_output_names()
print(mido.get_output_names())
outport = mido.open_output(ports[0])

def channel_setting():
    for index in range(len(keylist["Channel"])):
        outport.send(Message("program_change",program=keylist["Channel"][index]))

def json_reload():
    loadedjson = json.load(open("keylist.json", "r"))
    print(loadedjson["Righthand"])

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
    print(path, lefthand)