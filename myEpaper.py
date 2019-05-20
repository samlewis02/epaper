#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd4in2
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
from getcal import getCal
from getcurr import getCurr


myCalUrl = "https://script.google.com/macros/s/AKfycbwY2YIhEJeJc3GbmubJ4diF-R8mYYCfEiHH49LnxS70AvGRPskt/exec"
myCurUrl = "http://data.fixer.io/api/latest?access_key=0a371f7901a6260a0ea11865f1ad98da&symbols=TWD,GBP&format=1"

def drawRectRnd(x0, y0, x1, y1, r, fill):
    draw.rectangle((x0+r,y0,x1-r,y1), fill=fill)
    draw.rectangle((x0,y0+r,x1,y1-r), fill=fill)
    draw.ellipse((x0,y0,x0+2*r,y0+2*r), fill=fill)
    draw.ellipse((x1-2*r,y0,x1,y0+2*r), fill=fill)
    draw.ellipse((x0,y1-2*r,x0+2*r,y1), fill=fill)
    draw.ellipse((x1-2*r,y1-2*r,x1,y1), fill=fill)

def initDisplay():
    drawRectRnd(20, 30, 280, 100, 10, 255)
    drawRectRnd(20, 140, 280, 380, 10, 255)
    epd.display(epd.getbuffer(Limage))
    
    
def showTime(ltime, daydate):
    drawRectRnd(20, 30, 280, 100, 10, 255)
    draw.text((50, 40), ltime, font = font48, fill = 0)
    draw.text((65, 5), daydate, font = font16, fill = 255)
    epd.display(epd.getbuffer(Limage))
    
try:
    epd = epd4in2.EPD()
    epd.init()
    epd.Clear(0xFF)
    

    # Drawing on the Vertical image
    Limage = Image.new('1', (epd4in2.EPD_HEIGHT, epd4in2.EPD_WIDTH), 0)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)

    t = time.time()
    time_now1 = t
    time_now2 = t
    initDisplay()
    try:
        tdyStr, tomStr = getCal(myCalUrl)
        draw.text((30, 150), tdyStr + tomStr, font = font24, fill = 0)
    except:
        draw.text((30, 150), "No calendar data", font = font24, fill = 0)
    
    xrate = float(getCurr(myCurUrl))
    print("xrate =", xrate)
    draw.text((70, 110), "1GBP = "+ str(xrate) + "NT$", font = font16, fill = 255)
      

######################## START LOOP ########################
    while True:
        if time.time() >= t+ 10: #every 10 seconds
            rn = datetime.datetime.now()
            ltime = rn.strftime("%H:%M:%S")
            daydate = rn.strftime("%A, %d %B %Y")  
            showTime(ltime, daydate)
            t = time.time()
        # Crude scheduler to get Google calendar every 30 mins
        if time.time() >= time_now1 + 1800:
            try:
                tdyStr, tomStr = getCal(myCalUrl) 
                draw.text((30, 150), tdyStr + tomStr, font = font24, fill = 0)
            except:
                draw.text((30, 150), "No calendar data", font = font24, fill = 0)
            time_now1 = time.time()
         # Crude scheduler to get exchange rate every 60 mins
        if time.time() >= time_now2 + 3600:
            try:
                xrate = float(getCurr(myCurUrl)) 
                draw.text((70, 110), str(xrate), font = font16, fill = 255)
            except:
                draw.text((70, 110), "1GBP = "+ str(xrate) + "NT$", font = font16, fill = 255)
            time_now2 = time.time()
   
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

