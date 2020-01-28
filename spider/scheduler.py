from pageDownloader import HtmlDownloader
from pageParser import HtmlParser
from plot import makePlot
import time, json
from utils import saveData,loadHistory,getLocalTime,backup

currentTick = 0
config = {}
sleepInterval = 3600
nextScheduleTime = 0*60*60
dingxiangyuanURL = 'https://3g.dxy.cn/newh5/view/pneumonia'

def getCurrentTick():
    startTime = time.mktime(time.strptime(config['startTime'], "%Y-%m-%d %Hh"))
    currentTime = time.time()
    return int((currentTime-startTime)//3600)

def loadConfig():
    with open("./config.json","r",errors='ignore',encoding='utf-8') as w:
        global config
        config = json.load(w)  

def updateConfig(name,level):
    # change the 'lastUpdate' property of the specific item in monitorList
    for item in config['monitorList']:
        if item['level'] == level and item['name'] == name:
            item['lastUpdate'] = getLocalTime()
            break

def checkConfig(name,level):
    # check if this item in monitorList has been updated
    for item in config['monitorList']:
        if item['level'] == level and item['name'] == name and item['lastUpdate'] == getLocalTime():
            return True
    return False


def saveConfig():
    with open("./config.json","w",errors='ignore',encoding='utf-8') as w:
        json.dump(config, w, ensure_ascii=False)

def schedulePlot(parser, name="全国",level="nation",interval=3):
    """schedule a plot of any scope for any area(city or province)

    :param parser: a HtmlParser Object
    :param name: city name or province name
    :param level: nation, province, city
    :param interval: set by hour
    """

    if currentTick % interval == 0 and not checkConfig(name,level):

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

        updateConfig(name,level)


if __name__=="__main__":
  
    loadConfig()
    currentTick = getCurrentTick()
    time.sleep(nextScheduleTime)
    while True:
        # download page
        hd =  HtmlDownloader()
        html = hd.download(dingxiangyuanURL)      
        # parse page     
        hp = HtmlParser(html)
        for item in config['monitorList']:
            name,level,interval,_ = item.values()
            schedulePlot(hp,name,level,interval)
        # update config
        config['currentTime'] = getLocalTime()
        saveConfig()
        backup()
        # update every hour
        currentTick += 1
        time.sleep(sleepInterval)

