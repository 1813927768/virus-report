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

def test():
    testList = {'吃穿': 1}
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(testList,w,ensure_ascii=False)