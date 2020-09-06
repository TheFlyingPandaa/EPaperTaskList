#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f')
args = parser.parse_args()

standardFile = "wopwop.txt"
lineSize = 14
HEADERNAME = "\x1b[1;38;5;218m"
TASKNAME   = "\x1b[1;38;5;195m"
NOTENAME   = "\x1b[1;38;5;252m"
LINEEND    = "\x1b[0m"
TASKEND    = "[ ]"

if args.f:
    standardFile = args.f

taskyRawOutput = open(standardFile, "r")

finalList = [(False,False, "false")]
finalList.pop(0)


for currentLine in taskyRawOutput:
    foundHead = currentLine.find(HEADERNAME)
    foundTask = currentLine.find(TASKNAME)
    foundNote = currentLine.find(NOTENAME)
    finalLine = ""
    head = False
    note = False

    if foundHead != -1:
        currentLine = currentLine.split(HEADERNAME,1)
        currentLine.pop(0)
        head = True
    elif foundTask != -1:
        currentLine = currentLine.split(TASKNAME,1)
        currentLine.pop(0)
        foundTaskEnd = currentLine[0].find(TASKEND)
        currentLine[0] = currentLine[0][foundTaskEnd+4 : len(currentLine[0])]
    elif foundNote != -1:
        currentLine = currentLine.split(NOTENAME,1)
        currentLine.pop(0)
        note = True
    else:
        continue

    if len(currentLine) > 0:
        finalLine = currentLine[0].split(LINEEND)[0]
    
    finalList.append((head, note, finalLine))

taskyRawOutput.close()
