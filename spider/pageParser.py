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
        r = re.search('\d+',res)
        print(r)
          
    # 查询当前时刻疫情
    def _get_current_status(self,soup):
        rawSummary = soup.find(id="getStatisticsService").text
        res = re.search('(?<=\"countRemark\":).*?,',rawSummary).group(0)
        nums = re.findall('\d+',res)
        if len(nums) != 4:
            raise Exception("Parse page fail!")
        summary = {}
        summary['确诊'] = int(nums[0])
        summary['疑似'] = int(nums[1])
        summary['治愈'] = int(nums[2])
        summary['死亡'] = int(nums[3])
        return summary
    
    def _get_history_status(self,soup):
        pass


if __name__=="__main__":
    hp =  HtmlParser()
    hp.test()
    # with open("test.txt","w",errors='ignore') as w:
    #     w.write(html)
    # hp.parser(url,html)