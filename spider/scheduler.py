from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
from time import sleep
from utils import saveData,loadHistory
import json,os

interval = 2*60*60
nextScheduleTime = 1*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'

def test():
    testList = {'吃穿': 1}
    with open("./spider/data/sum.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(testList,w,ensure_ascii=False)


if __name__=="__main__":
  
    try:
        sleep(nextScheduleTime)
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
            # save history
            saveData()
            # update every 2 hour
            sleep(interval)
    finally:
        saveData()

