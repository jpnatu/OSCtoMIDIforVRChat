import mido
from mido import Message

ports = mido.get_output_names()
outport = mido.open_output(ports[0])
print(ports)

notenum = 36

# ポート管理


def main():
    print("Module_Logic has connected")


def portscheck():
    foundports = mido.get_output_names()
    return(foundports)


def portschange(portnum):
    mido.open_output(ports[portnum])
    print(f"Succesfully opened port[{ports[portnum]}]")

# 押されたときの処理関数


def midiR(path, righthand=0):
    print(path, righthand)
    if righthand == 1:
        outport.send(Message('note_on', note=notenum + 0))
    elif righthand == 2:
        outport.send(Message('note_on', note=notenum + 2))
    elif righthand == 3:
        outport.send(Message('note_on', note=notenum + 4))
    elif righthand == 4:
        outport.send(Message('note_on', note=notenum + 5))
    elif righthand == 5:
        outport.send(Message('note_on', note=notenum + 7))
    elif righthand == 6:
        outport.send(Message('note_on', note=notenum + 9))
    elif righthand == 7:
        outport.send(Message('note_on', note=notenum + 11))
    pass


def midiL(path, lefthand=0):
    print(path, lefthand)
    global notenum
    if lefthand == 0:
        notenum = 36
    elif lefthand == 1:
        notenum = 48
    elif lefthand == 2:
        notenum = 60
    pass
