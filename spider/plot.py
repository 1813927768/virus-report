import matplotlib.pyplot as plot
from utils import loadHistory
import os

colorStyle = {
    '确诊': 'red',
    '死亡': 'black',
    '治愈': 'green',
    '疑似': 'blue'
}

markerStyle = {
    '确诊': 'o',
    '死亡': 'x',
    '治愈': '*',
    '疑似': '.'
}

lineStyle = {
    '确诊': '-',
    '死亡': '--',
    '治愈': '--',
    '疑似': '--'
}

ch2en = {
    '确诊': 'Diagnosis',
    '死亡': 'Death',
    '治愈': 'Cure',
    '疑似': 'Suspected'
}

# 防止x轴label过于密集（label最大数目7）
def adjustXAxies(xArray):
    maxLabelNum = 6
    
    def replaceInterval(xArray,interval):
        # 防止plot函数自动合并相同的x值（""）
        resArray = [" "*i for i in range(len(xArray))]
        for i in range(maxLabelNum):
            loc = i*(interval+1)
            if loc < len(xArray):
                resArray[loc] = xArray[loc]
        return resArray
            
    if len(xArray) <= maxLabelNum:
        return xArray
    else:
        times = len(xArray)//maxLabelNum
        return replaceInterval(xArray,times)

def makePlot(x,y,title="national",ignore=['治愈','死亡','疑似']):
    if len(x) <= 1:
        return
    plot.ylabel('people')
    plot.xlabel("time")
    for key in y[0].keys():
        if key in ignore:
            continue
        plot.plot(adjustXAxies(x), list(map(lambda x:x[key],y)), color=colorStyle[key], marker=markerStyle[key], linestyle=lineStyle[key],label=ch2en[key])
    # plot.xticks(range(1,len(x)+1),)
    plot.title('2019-nConv Report %s'%(title))
    # plot.legend(shadow=True,loc="upper left")
    plot.savefig("./image/2019-nConv_report_%s_%s.jpg"%(title,x[-1]))
    plot.close('all')
    if len(x) > 2:
        try:
            os.remove("./image/2019-nConv_report_%s_%s.jpg"%(title,x[-2]))
        except:
            print("remove error")
    

def makeGrowthPlot():
    # get nation data
    sumPath = "./spider/data/sum_nation_全国.json"
    timePath = "./spider/data/time_nation_全国.json"
    nationList,_ = loadHistory(sumPath,timePath)
    # adjust nation data interval to 24 hour
    nationList = nationList[::2]
    # get hubei data
    sumPath = "./spider/data/sum_province_湖北.json"
    timePath = "./spider/data/time_province_湖北.json"
    hubeiList,timeList = loadHistory(sumPath,timePath)
    # get diagnosis data from list
    nationList = list(map(lambda x:x["确诊"],nationList))
    hubeiList = list(map(lambda x:x["确诊"],hubeiList))
    # get growth data from raw
    nationGrowthList = [nationList[i]-nationList[i-1] for i in range(1,len(timeList))]
    hubeiGrowthList = [hubeiList[i]-hubeiList[i-1] for i in range(1,len(timeList))]
    # get outside hubei data
    outHubeiGrowthList = [nationGrowthList[i]-hubeiGrowthList[i] for i in range(len(nationGrowthList))]
    timeList = timeList[1:]
    # make plot 
    plot.ylabel('growth')
    plot.xlabel("time")
    plot.plot(adjustXAxies(timeList), nationGrowthList, color=colorStyle["确诊"], marker=markerStyle["确诊"], linestyle=lineStyle["确诊"],label="China")
    plot.plot(adjustXAxies(timeList), hubeiGrowthList, color=colorStyle["疑似"], marker=markerStyle["确诊"], linestyle=lineStyle["确诊"],label="inside Hubei")
    plot.plot(adjustXAxies(timeList), outHubeiGrowthList, color=colorStyle["治愈"], marker=markerStyle["确诊"], linestyle=lineStyle["确诊"],label="outside Hubei")
    plot.title('2019-nConv Growth Report')
    plot.legend(shadow=True,loc="upper left")
    plot.savefig("./image/2019-nConv_growth_report")
    plot.close('all')


def updateAllPlot():
    # loda config
    with open("./config.json","r",errors='ignore',encoding='utf-8') as w:
        config = json.load(w) 
    for item in config['monitorList']:
        name,level,_,_ = item.values()
        fileName = "%s_%s"%(level,name)
        sumPath = "./spider/data/sum_%s.json"%(fileName)
        timePath = "./spider/data/time_%s.json"%(fileName)

        sumList,timeList = loadHistory(sumPath,timePath) 
        makePlot(timeList,sumList,fileName)

if __name__ == '__main__':
    # sumPath = "./spider/data/sum_nation_全国.json"
    # timePath = "./spider/data/time_nation_全国.json"
    # sumList,timeList = loadHistory(sumPath,timePath)
    # makePlot(timeList,sumList)
    makeGrowthPlot()
    