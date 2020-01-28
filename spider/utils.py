import os,json,time

def loadHistory(sumPath,timePath):
    sumList = []
    timeList = []
    if os.path.exists(sumPath) and os.path.exists(timePath):
        with open(sumPath,"r",errors='ignore',encoding='utf-8') as w:
            sumList = json.load(w)
        with open(timePath,"r",errors='ignore') as w:
            timeList = json.load(w)   
    return sumList,timeList

def saveData(sumList,sumPath,timeList,timePath):
    with open(sumPath,"w",errors='ignore',encoding='utf-8') as w:
        json.dump(sumList,w,ensure_ascii=False)
    with open(timePath,"w",errors='ignore') as w:
        json.dump(timeList,w)

def getLocalTime():
    return time.strftime('%m-%d %Hh',time.localtime(time.time()))    

def backup():
    os.system('/bin/cp -f ./spider/data/*.json ./spider/data/backup/')
    # update images for html
    os.system('rm -f ./web/image/*')
    os.system('/bin/cp -f image/*.jpg web/image/')
    # update config.js
    with open("./config.json","r",errors='ignore',encoding='utf-8') as w:
        configJson = json.load(w)
        configStr = json.dumps(configJson,ensure_ascii=False)
    with open("./web/config.js","w",errors='ignore',encoding='utf-8') as w:
        w.write("var config = %s"%(configStr))

def test():
    testList = {'吃穿': 1}
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(testList,w,ensure_ascii=False)

if __name__ == '__main__':
    backup()