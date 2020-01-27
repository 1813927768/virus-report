from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
import time
from utils import saveData,loadHistory,getLocalTime

currentTick = 0
interval = 1*60*60
nextScheduleTime = 0*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'

def getCurrentTick():
    startTime = time.mktime(time.strptime("2020-01-26 23", "%Y-%m-%d %H"))
    currentTime = time.time()
    return (currentTime-startTime)//interval

def schedulePlot(parser, name="nation",level="nation",interval=3):
    """schedule a plot of any scope for any area(city or province)

    :param parser: a HtmlParser Object
    :param name: city name or province name
    :param level: nation, province, city
    :param interval: set by hour
    """

    if currentTick % interval == 0:

        fileName = "%s_%s"%(level,name)
        sumPath = "./spider/data/sum_%s.json"%(fileName)
        timePath = "./spider/data/time_%s.json"%(fileName)

        sumList,timeList = loadHistory(sumPath,timePath)  

        if level == "nation":
            summary = parser.getSummary()
        elif level == "province":
            summary = parser.getProvinceSummary(name)
        elif level == "city":
            [province,city] = name.split('-')
            summary = parser.getCitySummary(province,city)
        else:
            raise Exception("scheuler args error")
        currentTime = getLocalTime()

        sumList.append(summary)
        timeList.append(currentTime)
        makePlot(timeList,sumList,fileName)
        saveData(sumList,sumPath,timeList,timePath)

    
if __name__=="__main__":
  
    currentTick = getCurrentTick()
    time.sleep(nextScheduleTime)
    while True:
        # download page
        hd =  HtmlDownloader()
        html = hd.download(dingxiangyuanURL)      
        # parse page     
        hp = HtmlParser(html)
        schedulePlot(hp)
        schedulePlot(hp,"湖北","province",6)
        schedulePlot(hp,"河南","province",6)
        schedulePlot(hp,"河南-信阳","city",12)
        schedulePlot(hp,"湖北-武汉","city",12)
        # update every hour
        currentTick += 1
        time.sleep(interval)

