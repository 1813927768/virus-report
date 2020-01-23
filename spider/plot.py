import matplotlib.pyplot as plot

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

def makePlot(x,y):
    plot.ylabel('people')
    plot.xlabel("time")
    for key in y[0].keys():
        plot.plot(x, list(map(lambda x:x[key],y)), color=colorStyle[key], marker=markerStyle[key], linestyle=lineStyle[key],label=ch2en[key])
    plot.title('2019-nConv Report')
    plot.legend()
    plot.savefig("./spider/data/2019-nConv_report_%s.jpg"%(getLast(x)))

if __name__ == '__main__':
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    nums = [256, 289, 302, 356, 389, 400, 402, 436]
    gdps = []
    for i in range(len(nums)):
        gdps.append({'确诊': nums[i], '死亡': nums[i]-100})
    makePlot(years,gdps)
    