#!/usr/bin/python

import sys
import os

nameFile = ""
count = 0

for arg in sys.argv:
    if arg == "-f":
        index = sys.argv.index(arg)
        nameFile = os.path.splitext(sys.argv[index+1])[0]
    elif arg == "-l":
        index = sys.argv.index(arg)
        count = int(sys.argv[index+1])


file = open(nameFile + ".ttl", "r")

# List
lineList = []

# Save all lines into a list
for line in file:
    lineList.append(line.strip())


initCount = 0
endCount = count

endList = []


while initCount < len(lineList):
    if endCount > len(lineList):
        endCount = len(lineList) - 1
    
    if lineList[endCount].endswith('.'):

        writer = open(nameFile + "_" + str(initCount) + ".ttl", "w")
        writer.write("\n".join(str(item) for item in lineList[initCount:endCount+1]))
        writer.close()

        initCount = endCount+1
        endCount += count

    else:
        endCount += 1