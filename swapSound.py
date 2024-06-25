#!/bin/python3
import subprocess

sinkStr = subprocess.run(["pacmd", "list-sinks"], capture_output = True)
sinkStr = sinkStr.stdout.decode('ascii').split("\n")

#|grep \*|cut -c 12")

begin = end = cur = 0

sinks = []

for line in sinkStr:
    if "index" in line:
        end = cur
        if end != 0:
            sinks.append([sinkStr[i] for i in range(begin, end)])
        begin = cur
    cur += 1
end = cur

# Catch last sink
sinks.append([sinkStr[i] for i in range(begin, end)])

# Remove line with n sink(s) available
sinks = sinks[1:]
for i in range(len(sinks)):
    sinks[i] = "\n".join(sinks[i])

active = ''
indexes = []
names = []
# Find active index, make list of indexes and a list of names
for i in sinks:
    for line in i.split("\n"):
        if "index" in line:
            # Don't use HDMI
            #if line[-1] == '3':
            #    break
            if "*" in line:
                active = line.split(' ')[-1]
            print("line: ", line)
            indexes.append(line.split(' ')[-1])
        if "name:" in line:
            names.append(line[line.find('<') + 1:line.find('>')])

print("Indexes: ", indexes)
nextIndex = 0

# Chooses next index after active
for i in range(len(indexes)):
    if indexes[i] == active:
        nextIndex = (i + 1)%(len(indexes))

for i in range(len(names)):
    s = ""
    if active == indexes[i]:
        s += "*"
    s+= names[i]
    print(s)

print("Swapping to",names[nextIndex])

print(indexes[nextIndex], active)
print(" ".join(["pacmd", "set-default-sink", names[nextIndex]]))
subprocess.run(["pacmd", "set-default-sink", names[nextIndex]])
