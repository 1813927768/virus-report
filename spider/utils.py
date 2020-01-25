sumPath = "./spider/data/sum.json"
timePath = "./spider/data/time.json"

def loadHistory():
    sumList = []
    timeList = []
    if os.path.exists(sumPath) and os.path.exists(timePath):
        with open(sumPath,"r",errors='ignore',encoding='utf-8') as w:
            sumList = json.load(w)
        with open(timePath,"r",errors='ignore') as w:
            timeList = json.load(w)   
    return sumList,timeList

def saveData():
    with open(sumPath,"w",errors='ignore',encoding='utf-8') as w:
        json.dump(sumList,w,ensure_ascii=False)
    with open(timePath,"w",errors='ignore') as w:
        json.dump(timeList,w)