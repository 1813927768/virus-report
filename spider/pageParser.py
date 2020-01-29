#coding:utf-8

from bs4 import BeautifulSoup
from abc import abstractmethod
import lxml
import re
import json

def findElement(array,func):
    for i in array:
        if func(i):
            return i
    return None

def findElementByProvinceName(array,name):
    def compareProvinceName(item):
        if item["provinceName"] == name or item["provinceShortName"] == name:
            return True
        return False
    return findElement(array,compareProvinceName)

def findElementByCityName(array,name):
    def compareCityName(item):
        if item["cityName"] == name:
            return True
        return False
    return findElement(array,compareCityName)

class HtmlParser(object):

    @abstractmethod
    def getSummary(self):
        pass

    @abstractmethod
    def getCitySummary(self,provinceName,cityName):
        pass

    @abstractmethod
    def getProvinceSummary(self,provinceName):
        pass

class DxyParser(HtmlParser):       

    def __init__(self,html):
        if not html is None:
            self.soup = BeautifulSoup(html,'lxml')
             
    def getSummary(self):             
        currentSum = self._get_current_status()
        return currentSum
    
    def getProvinceSummary(self,provinceName):
         provinceData = self._get_province_stats(provinceName)
         provinceSummary = {
             "确诊": provinceData['confirmedCount'],
             "疑似": provinceData['suspectedCount'],
             "治愈": provinceData['curedCount'],
             "死亡": provinceData['deadCount']
            }
         return provinceSummary
    
    def getCitySummary(self,provinceName,cityName):
        provinceData = self._get_province_stats(provinceName)
        cityData = self._get_city_stats(provinceData,cityName)
        citySummary = {
            "确诊": cityData['confirmedCount'],
            "疑似": cityData['suspectedCount'],
            "治愈": cityData['curedCount'],
            "死亡": cityData['deadCount']
        }
        return citySummary
    
    def test(self):
        self.soup = BeautifulSoup(open(r'./spider/data/page.html'),"lxml")
        province = self._get_province_stats("河南")
        city = self._get_city_stats(province,"信阳")
        print(city)
        print(self._get_current_status())
        
    # 查询某省数据
    def _get_province_stats(self,name):
        raw = self.soup.find(id="getAreaStat").text
        areaStatStr = re.search('(?<=getAreaStat\s=).*(?=}catch)',raw).group(0)
        areaStatArray = json.loads(areaStatStr)
        provinceData = findElementByProvinceName(areaStatArray,name)
        return provinceData
    
    # 查询城市数据
    def _get_city_stats(self,provinceData,cityName):
        return findElementByCityName(provinceData["cities"],cityName)
   
    # 查询当前时刻全国数据
    def _get_current_status(self):
        # 全国数据
        rawSummary = self.soup.find(id="getStatisticsService").text
        cure = re.search('(?<=\"curedCount\":).*?(?=,)',rawSummary).group(0)
        death = re.search('(?<=\"deadCount\":).*?(?=,)',rawSummary).group(0)
        suspected = re.search('(?<=\"suspectedCount\":).*?(?=,)',rawSummary).group(0)
        diagnosis = re.search('(?<=\"confirmedCount\":).*?(?=,)',rawSummary).group(0)
        summary = {}
        summary['确诊'] = int(diagnosis)
        summary['疑似'] = int(suspected)
        summary['治愈'] = int(cure)
        summary['死亡'] = int(death)
        return summary
    
    def _get_history_status(self):
        pass


if __name__=="__main__":
    parser = DxyParser(open(r'./spider/data/page.html'))
    print(parser.getSummary())
    print(parser.getCitySummary("河南","信阳"))
    print(parser.getProvinceSummary('湖北'))