import requests

def getCal(url):
    #e = serinit.e
    try:
        resp = requests.get(url)
    except:
        #draw.text((30, 150), "No calendar data", font = font24, fill = 0)
        #ser.write(b"cal.txt=\" ERROR: Could not get calendar data\""+e)
        exit
    #print("Response: "  + str(resp.status_code))
    if resp.status_code==200:
        #print(resp.content)
        root = resp.json()
        todayStr = "Today\n"
        for i in range(10):
            try:
                ttitle = root["eventsToday"][i]["title"]
            except:
                break
            ttime = root["eventsToday"][i]["time"]
            tevent = str("  ") + ttitle + str(" ") + ttime + str("\n")
            todayStr += tevent;
    
        #print(todayStr)

        tomorrowStr = "\nTomorrow\n"
        for j in range(10):
            try:
                mtitle = root["eventsTomro"][j]["title"]
            except:
                break
            mtime = root["eventsTomro"][j]["time"]
            mevent = str("  ") + mtitle + str(" ") + mtime + str("\n")
            tomorrowStr += mevent
    
        #print(tomorrowStr)
        #ser.write(b"cal.txt=\"" + todayStr.encode() + tomorrowStr.encode() + b"\""+e)
        return(todayStr, tomorrowStr)
    else:
        #ser.write(b"cal.txt=\" ERROR: Could not get calendar data\""+e)
        #draw.text((30, 150), "No calendar data", font = font24, fill = 0)
        exit
        
