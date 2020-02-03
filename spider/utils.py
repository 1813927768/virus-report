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

def getLocalTime(format="%m-%d %Hh"):
    return time.strftime(format,time.localtime(time.time()))    

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

def dataFormat(fileName,oldInterval=12,newInterval=24,testMode=False):
    sumPath = "./spider/data/sum_%s.json"%(fileName)
    timePath = "./spider/data/time_%s.json"%(fileName)
    sumJson, timeJson = loadHistory(sumPath,timePath)
    if newInterval == 24:
        # if interval is one day, hide `hour` format
        timeJson = list(map(lambda x:x.split(" ")[0],timeJson))
    reduceScale = int(-(newInterval/oldInterval))
    timeJson = timeJson[::reduceScale][::-1]
    sumJson = sumJson[::reduceScale][::-1]
    if testMode:
        print(timeJson)
        print(sumJson)
        return
    saveData(sumJson,sumPath,timeJson,timePath)


if __name__ == '__main__':
    backup()