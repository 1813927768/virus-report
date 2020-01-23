from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
from time import sleep
import json

# 每3h更新一次
sleepTime = 3*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'
sumList = []
timeList = []

def saveData():
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(sumList,w,ensure_ascii=False)
    with open("./spider/data/time.json","w",errors='ignore') as w:
        json.dump(timeList,w)

def test():
    testList = {'吃穿': 1}
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(testList,w,ensure_ascii=False)

if __name__=="__main__":
  
    try:
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
            # update every 3 hour
            sleep(sleepTime)
    finally:
        saveData()

