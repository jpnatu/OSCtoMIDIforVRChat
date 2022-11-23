import json
import mido
from mido import Message

json_open = open("keylist.json", "r")
json_load = json.load(json_open)
print("Module_Logic has connected")
ports = mido.get_output_names()
print(mido.get_output_names())
outport = mido.open_output(ports[0])

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
    channel=json_load["Righthand"][righthand][3],
    note=json_load["Righthand"][righthand][2]))
    
def midiL(path, lefthand=0):
    print(path, lefthand)