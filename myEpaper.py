#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd4in2
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
from getcal import getCal
from getcurr import getCurr
from bme280 import readBME280All


myCalUrl = "https://script.google.com/macros/s/AKfycbwY2YIhEJeJc3GbmubJ4diF-R8mYYCfEiHH49LnxS70AvGRPskt/exec"
myCurUrl = "http://data.fixer.io/api/latest?access_key=0a371f7901a6260a0ea11865f1ad98da&symbols=TWD,GBP&format=1"

epd = epd4in2.EPD()
epd.init()
epd.Clear(0xff)

# Drawing on the Vertical image
Limage = Image.new('1', (epd4in2.EPD_HEIGHT, epd4in2.EPD_WIDTH), 0)  # 0: blacken the frame
draw = ImageDraw.Draw(Limage)

font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48)
font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)



def drawRectRnd(x0, y0, x1, y1, r, fill):
    draw.rectangle((x0+r,y0,x1-r,y1), fill=fill)
    draw.rectangle((x0,y0+r,x1,y1-r), fill=fill)
    draw.ellipse((x0,y0,x0+2*r,y0+2*r), fill=fill)
    draw.ellipse((x1-2*r,y0,x1,y0+2*r), fill=fill)
    draw.ellipse((x0,y1-2*r,x0+2*r,y1), fill=fill)
    draw.ellipse((x1-2*r,y1-2*r,x1,y1), fill=fill)

def initDisplay():
 
    # draw background
    drawRectRnd(20, 30, 280, 100, 10, 255)
    drawRectRnd(20, 140, 280, 340, 10, 255)
    #epd.display(epd.getbuffer(Limage))
    rn = datetime.datetime.now()
    ltime = rn.strftime("%H:%M")
    daydate = rn.strftime("%A, %d %B %Y")  
    showTime(ltime, daydate)
    try:
        tdyStr, tomStr = getCal(myCalUrl)
        draw.text((30, 150), tdyStr + tomStr, font = font16, fill = 0)
    except:
        draw.text((30, 150), "No calendar data", font = font16, fill = 0)
    
    try:
        xrate = float(getCurr(myCurUrl))
        #print("xrate =", xrate)
        draw.text((70, 110), "1GBP = "+ str(xrate) + "NT$", font = font16, fill = 255)
    except:
        draw.text((70,110), "No exchange data", font=font16, fill=255)

    try:
        ltemp, lpres, lhum = readBME280All()
        draw.text((30, 360), b'%.2f'%ltemp + b'C  ' + b'%.2f'%lhum + b'%RH  ' + b'%.1f'%lpres + b'hPa', font = font16, fill=255)
    except:
        draw.text((30, 360), "No T, RH, pressure data", font = font16, fill=255)
    # send buffer to display
    epd.display(epd.getbuffer(Limage))    
    
def showTime(ltime, daydate):
    drawRectRnd(20, 30, 280, 100, 10, 255) # blank area
    draw.text((90, 40), ltime, font = font48, fill = 0)
    draw.rectangle((20,0,280,25), fill=0) # blank area
    draw.text((65, 5), daydate, font = font16, fill = 255)
    
    
try:
    initDisplay()
  
    t = time.time()
    time_now1 = t
    time_now2 = t
    time_now3 = t
    this_min = time.localtime().tm_min

######################## START LOOP ########################

    while True:
        
        if time.localtime().tm_min != this_min: #every minute
            #print("minute update")
            rn = datetime.datetime.now()
            ltime = rn.strftime("%H:%M")
            #print(ltime)
            daydate = rn.strftime("%A, %d %B %Y")  
            showTime(ltime, daydate)
            draw.rectangle((20,345,280,385), fill=0) # blank area
            try:
                ltemp, lpres, lhum = readBME280All()
                draw.text((30, 360), b'%.2f'%ltemp + b'C  ' + b'%.2f'%lhum + b'%RH  ' + b'%.1f'%lpres + b'hPa', font = font16, fill=255)

            except:
                draw.text((30, 360), "No T, R, P data", font = font16, fill = 0)
            #send buffer to display
            epd.display(epd.getbuffer(Limage))

            this_min = time.localtime().tm_min
 
        # Crude scheduler to get Google calendar every 30 mins
        if time.time() >= time_now1 + 1800:
            drawRectRnd(20, 140, 280, 340, 10, 255) # blank area
            try:
                tdyStr, tomStr = getCal(myCalUrl) 
                draw.text((30, 150), tdyStr + tomStr, font = font16, fill = 0)
            except:
                draw.text((30, 150), "No calendar data", font = font16, fill = 0)
            time_now1 = time.time()
            
         # Crude scheduler to get exchange rate every 60 mins
        if time.time() >= time_now2 + 3600:
            draw.rectangle((60,140,280,345), fill=255) # blank area
            try:
                xrate = float(getCurr(myCurUrl)) 
                draw.text((70, 110), str(xrate), font = font16, fill = 0)
            except:
                draw.text((70, 110), "1GBP = "+ str(xrate) + "NT$", font = font16, fill = 255)
            time_now2 = time.time()
        time.sleep(5) # don't hog cpu
        
                
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

