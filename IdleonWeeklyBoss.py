import subprocess
import time

coords = {  
            "b1" : (3250, 850),
            #"b1" : (1625, 850),
            "b2" : (3250, 1000),
            #"b2" : (1625, 1000),
            "b3" : (3250, 1150),
            #"b3" : (1625, 1150),
        }

def tap(seq):
    for s in seq:
        s = 'b' + s
        subprocess.call(["xdotool", "mousemove", str(coords[s][0]), str(coords[s][1]), "click", "1"])
        time.sleep(.15)

def clean(seq):
    ret = []
    for i in seq:
        if i in [str(j + 1) for j in range(3)]:
            ret.append(i)
    return ret

seq = """
  3 3 3 - 3 2 3 - 1 3 3 - 2 (FR)
 3 3 3 - 1
 3 3 2 - 2 3 2
 3 3 3 - 3 (FR)
 3 3 1 - 1
 1 2 3 (FR)
 3 3 3 - 3 2 3 - 1 3 3*- 3
 """

seq = clean(seq)

#print (seq)
tap(seq)
