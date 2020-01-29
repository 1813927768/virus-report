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
    maxLabelNum = 7
    
    def replaceInterval(xArray,interval):
        # 防止plot函数自动合并相同的x值（""）
        resArray = [" "*i for i in range(len(xArray))]
        for i in range(maxLabelNum):
            loc = i*(interval+1)
            if loc < len(xArray):
                resArray[loc] = xArray[loc]
        return resArray
            
    if len(xArray) <= 7:
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
    plot.title('2019-nConv Report')
    # plot.legend(shadow=True,loc="upper left")
    plot.savefig("./image/2019-nConv_report_%s_%s.jpg"%(title,x[-1]))
    plot.close('all')
    if len(x) > 2:
        try:
            os.remove("./image/2019-nConv_report_%s_%s.jpg"%(title,x[-2]))
        except:
            print("remove error")
    

if __name__ == '__main__':
    sumPath = "./spider/data/sum_nation_nation.json"
    timePath = "./spider/data/time_nation_nation.json"
    sumList,timeList = loadHistory(sumPath,timePath)
    makePlot(timeList,sumList)
    