#coding:utf-8

from bs4 import BeautifulSoup
import lxml
import re
import time

def getLocalTime():
    return time.strftime('%Y-%m-%d %Hh',time.localtime(time.time()))

class HtmlParser(object):
    
    def parser(self,html):
        if  html is None:
            return
        soup = BeautifulSoup(html,'lxml')
        currentSum = self._get_current_status(soup)
        return getLocalTime(),  currentSum
    
    def test(self):
        soup = BeautifulSoup(open(r'./spider/data/page.html'),"lxml")
        rawSum = soup.find(id="getStatisticsService").text
        res = re.search('(?<=\"countRemark\":).*?,',rawSum).group(0)
        r = re.search('(?<=治愈\s)\d+',res)
        print(r)
          
    # 查询当前时刻疫情
    def _get_current_status(self,soup):
        rawSummary = soup.find(id="getStatisticsService").text
        res = re.search('(?<=\"countRemark\":).*?,',rawSummary).group(0)
        cure = re.search('(?<=治愈\s)\d+',res).group(0)
        death = re.search('(?<=死亡\s)\d+',res).group(0)
        suspected = re.search('(?<=疑似\s)\d+',res).group(0)
        diagnosis = re.search('(?<=确诊\s)\d+',res).group(0)
        # nums = re.findall('\d+',res)
        # if len(nums) != 4:
        #     raise Exception("Parse page fail!")
        summary = {}
        summary['确诊'] = int(diagnosis)
        summary['疑似'] = int(suspected)
        summary['治愈'] = int(cure)
        summary['死亡'] = int(death)
        return summary
    
    def _get_history_status(self,soup):
        pass


if __name__=="__main__":
    hp =  HtmlParser()
    hp.test()
    # with open("test.txt","w",errors='ignore') as w:
    #     w.write(html)
    # hp.parser(url,html)