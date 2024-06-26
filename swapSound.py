#!/bin/python3

#IMPORTANT: For this setup to work, you need automute on alsamixer disabled. just run 'alsamixer' then scroll right until you find the automute option.

import subprocess

ports = subprocess.run(["pactl", "list", "sinks"], capture_output = True)

ports = ports.stdout.decode('ascii').split("\n")

sinkName = ""

begin = 0
end = 0

for i, txt in enumerate(ports):
    #print(txt)
    # Find sink name
    if "Name:" in txt and sinkName == "":
        sinkName = txt[txt.find(": ") + 2:]
        #print(sinkName)
    # Find substring with port, active port info
    if "Ports" in txt and begin == 0:
        begin = i + 1
    if "Active Port" in txt and end == 0:
        end = i + 1

ports = ports[begin:end]

# Active port line is the last, so remove from ports list (active port is still in the list after)
activePort = ports[-1]
activePort = activePort[activePort.find(":") + 2:]
ports = ports[:-1]

# Select text after : and remove whitespaces
ports = [''.join(i[:i.find(":")]).split()[0] for i in ports if ":" in i]


#print("Active: ", activePort)
#print("Ports: ", ports)

# Select index of port after active port
for i, port in enumerate(ports):
    if port == activePort:
        i = (i + 1) % len(ports)
        break

#print(i, len(ports), ports[i], activePort)

# Change port
cmd = ["pactl", "set-sink-port", sinkName, ports[i]]
#print(cmd)
subprocess.run(cmd)

# Lower and raise volume to trigger gnome sound osd
cmd = "xdotool key XF86AudioLowerVolume XF86AudioRaiseVolume".split()
subprocess.run(cmd)

#|grep \*|cut -c 12")

#begin = end = cur = 0
#
#sinks = []
#
#for line in ports:
#    if "index" in line:
#        end = cur
#        if end != 0:
#            sinks.append([ports[i] for i in range(begin, end)])
#        begin = cur
#    cur += 1
#end = cur
#
## Catch last sink
#sinks.append([ports[i] for i in range(begin, end)])
#
## Remove line with n sink(s) available
#sinks = sinks[1:]
#for i in range(len(sinks)):
#    sinks[i] = "\n".join(sinks[i])
#
#active = ''
#indexes = []
#names = []
## Find active index, make list of indexes and a list of names
#for i in sinks:
#    for line in i.split("\n"):
#        if "index" in line:
#            # Don't use HDMI
#            #if line[-1] == '3':
#            #    break
#            if "*" in line:
#                active = line.split(' ')[-1]
#            print("line: ", line)
#            indexes.append(line.split(' ')[-1])
#        if "name:" in line:
#            names.append(line[line.find('<') + 1:line.find('>')])
#
#print("Indexes: ", indexes)
#nextIndex = 0
#
## Chooses next index after active
#for i in range(len(indexes)):
#    if indexes[i] == active:
#        nextIndex = (i + 1)%(len(indexes))
#
#for i in range(len(names)):
#    s = ""
#    if active == indexes[i]:
#        s += "*"
#    s+= names[i]
#    print(s)
#
#print("Swapping to",names[nextIndex])
#
#print(indexes[nextIndex], active)
#print(" ".join(["pacmd", "set-default-sink", names[nextIndex]]))
#subprocess.run(["pacmd", "set-default-sink", names[nextIndex]])
