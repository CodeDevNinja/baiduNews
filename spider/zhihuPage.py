from urllib import request
from lxml import etree
from MongoHelp import MongoHelper as SqlHelper

class Zhihuhomepage():
    def __init__(self):
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhihu')
        self.base_url = 'https://www.zhihu.com'

    def gethomepage(self,url,user_name):
        html=request.urlopen('https://www.zhihu.com/people/jade-85-35/followers',timeout=5).read().decode('utf-8')
        tree = etree.HTML(html)
        collecter = tree.xpath("//div[@class='Profile-sideColumnItemValue']/text()")
        # time.sleep(2)
        if collecter:
            print(collecter)
            save = collecter[0][:-3].strip()
        else:
            save = 0
        #print(html)
    def updateCollect(self,user_name,save):
        self.SqlH.update({'user_name': user_name}, {'collect': save})
    def fromdb(self):
        tottal_s=self.SqlH.count(conditions={'collect':'none'})
        for c_page in range(tottal_s):
            result=self.SqlH.select(conditions={'collect':'none'},page=c_page)
            gethomepage(result[c_page]['homepage']+self.base_url)
        print(result[1]['user_name'])
        pass
zhp = Zhihuhomepage()
zhp.fromdb()