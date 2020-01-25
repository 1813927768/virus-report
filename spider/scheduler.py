from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
from time import sleep
from utils import saveData,loadHistory
import json,os

interval = 2*60*60
nextScheduleTime = 0*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'


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
            saveData(sumList,timeList)
            # update every 2 hour
            sleep(interval)
    finally:
        saveData(sumList,timeList)

