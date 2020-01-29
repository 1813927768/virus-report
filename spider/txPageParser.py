import re
import json
import requests
import datetime
from pageParser import HtmlParser

baseURL = 'https://view.inews.qq.com/g2/getOnsInfo?name='

def getAreaStats():
    areaURL = baseURL + 'wuwei_ww_area_counts'
    data = json.loads(requests.get(areaURL).json()['data'])
    # print(data)
    return data

def findCity(provinceName,cityName,list):
    for item in list:
        if item['city'] == cityName and item['area'] == provinceName:
            return item
    return None

class TxParser(HtmlParser):

    def getSummary(self):
        countryURL = baseURL + 'wuwei_ww_global_vars'
        data = json.loads(requests.get(countryURL).json()['data'])[0]
        summary = {}
        summary['确诊'] = data['confirmCount']
        summary['疑似'] = data['suspectCount']
        summary['治愈'] = data['cure']
        summary['死亡'] = data['deadCount']
        return summary
    
    def getProvinceSummary(self,provinceName):
        raw = getAreaStats()
        summary = {
            '确诊': 0,
            '疑似': 0,
            '治愈': 0,
            '死亡': 0
        }
        for item in raw:
            if item['area'] == provinceName:
                summary['确诊'] += item['confirm']
                summary['疑似'] += item['suspect']
                summary['治愈'] += item['heal']
                summary['死亡'] += item['dead']
        return summary

    def getCitySummary(self,provinceName,cityName):
        raw = getAreaStats()
        cityRaw = findCity(provinceName,cityName,raw)
        summary = {}
        summary['确诊'] = cityRaw['confirm']
        summary['疑似'] = cityRaw['suspect']
        summary['治愈'] = cityRaw['heal']
        summary['死亡'] = cityRaw['dead']
        return summary





if __name__ == "__main__":
    parser = TxParser()
    print(parser.getSummary())
    print(parser.getCitySummary("河南","信阳"))
    print(parser.getProvinceSummary('湖北'))

