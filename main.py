#!/usr/bin/env python3

import argparse
import epd2in7
import subprocess
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def main():

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
    cmd = "tasky.py -l > wopwop.txt"

    if args.f:
        standardFile = args.f
    else:
        os.popen(cmd).read()

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

    epd = epd2in7.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    finalImage = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 0)    # 255: clear the image with white

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    counter = 0
    for inp in finalList:
        if inp[0] == False:
            draw.text((20, ((counter)*20)), inp[2], font = font, fill = 255)
            counter += 1

    image = image.rotate(90, expand=1)
    finalImage.paste(image, (0,0))

    epd.display_frame(epd.get_frame_buffer(finalImage))

if __name__ == '__main__':
    main()
