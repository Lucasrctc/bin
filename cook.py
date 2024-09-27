from gameLib import *

coords = {  
#        3320 - 500 4020 - 1070
            "inv_squares" : [(a, b) for b in [500 + j * (1070 - 500)//3 for j in range(4)] for a in [3320 + i * (4020 - 3320)//3 for i in range(4)]],
            #"upgrade" : [(a, b) for b in [330 + 150*j for j in range(3)] for a in [180 + 250 * i for i in range(4)]],
            "OK" : (3020, 600),
        }

if __name__ == "__main__":
    for i in coords["inv_squares"]:
        cmd = ("xdotool mousemove %s %s mousedown 1 sleep 0.1 mousemove %s %s mouseup 1 sleep 0.1"%(*coords["OK"], *i)).split()
        print(cmd)
        call(cmd)
        time.sleep(0.1)
