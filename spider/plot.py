import matplotlib.pyplot as plot
from utils import loadHistory

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

def getLast(list):
    return list[len(list)-1]

def makePlot(x,y,title="national",ignore=['治愈','死亡','疑似']):
    if len(x) <= 1:
        return
    plot.ylabel('people')
    plot.xlabel("time")
    for key in y[0].keys():
        if key in ignore:
            continue
        plot.plot(x, list(map(lambda x:x[key],y)), color=colorStyle[key], marker=markerStyle[key], linestyle=lineStyle[key],label=ch2en[key])
    plot.title('2019-nConv Report')
    # plot.legend(shadow=True,loc="upper left")
    plot.savefig("./spider/image/2019-nConv_report_%s_%s.jpg"%(title,getLast(x)))

if __name__ == '__main__':
    sumList,timeList = loadHistory()
    makePlot(timeList,sumList)
    