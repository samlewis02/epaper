import requests


def getCurr(url):
    try:
        resp = requests.get(url)
        #print(resp.status_code)
        if resp.status_code==200:
            #print(resp.content)
            root = resp.json()  
            GBPrate = root["rates"]["GBP"]
            TWDrate = root["rates"]["TWD"]
            xrate = TWDrate / GBPrate
            #ser.write(b"curr.txt=\"1GBP = " + b'%.2f'%xrate + b"NT$\"" + e )
            #print(b'%.2f'%xrate)
            return (b'%.2f'%xrate)
        else:
            #return("INCORRECT STATUS CODE")
            exit
    except:
        print("REQUEST ERROR")
        #ser.write(b"curr.txt=\"ERROR: No data\"" + e )
        exit
        #print("Response: "  + str(resp.status_code))
    
    
