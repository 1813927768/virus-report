from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
from time import sleep
import json,os

sleepTime = 12*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'

def saveData():
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(sumList,w,ensure_ascii=False)
    with open("./spider/data/time.json","w",errors='ignore') as w:
        json.dump(timeList,w)

def test():
    testList = {'吃穿': 1}
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(testList,w,ensure_ascii=False)

def loadHistory():
    sumPath = "./spider/data/sum.json"
    timePath = "./spider/data/time.json"
    sumList = []
    timeList = []
    if os.path.exists(sumPath) and os.path.exists(timePath):
        with open(sumPath,"r",errors='ignore',encoding='utf-8') as w:
            sumList = json.load(w)
        with open(timePath,"r",errors='ignore') as w:
            timeList = json.load(w)   
        # adjust time span
        sumList = sumList[:1]
        timeList = timeList[:1]
    return sumList,timeList

if __name__=="__main__":
  
    try:
        sumList, timeList = loadHistory()
        while True:
            # download page
            hd =  HtmlDownloader()
            html = hd.download(dingxiangyuanURL)      
            # parse page     
            hp = HtmlParser()
            currentTime,summary = hp.parser(html)
            # make plot
            sumList.append(summary)
            timeList.append(currentTime)
            makePlot(timeList,sumList)
            # update every 12 hour
            sleep(sleepTime)
    finally:
        saveData()

