from urllib import request
from lxml import etree
from MongoHelp import MongoHelper as SqlHelper
import time
class Zhihuhomepage():
    def __init__(self):
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhihu')
        self.base_url = 'https://www.zhihu.com'

    def gethomepage(self,url,user_name):
        req = request.Request( url=url,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
        html=request.urlopen(req,timeout=5).read().decode('utf-8')
        tree = etree.HTML(html)
        collecter = tree.xpath("//div[@class='Profile-sideColumnItemValue']/text()")
        # time.sleep(2)
        if collecter:
            save = collecter[0][:-3].strip()
        else:
            save = 0
        print(user_name, collecter)
        self.updateCollect(user_name,save)
        #print(html)
    def updateCollect(self,user_name,save):
        self.SqlH.update({'user_name': user_name}, {'collect': save})
    def fromdb(self):
        tottal_s=self.SqlH.count(condition={'collect':'none'})
        print(tottal_s)
        for c_page in range(tottal_s):
            time.sleep(2)
            result=self.SqlH.select(conditions={'collect':'none'},count=1,page=c_page)
            self.gethomepage(self.base_url+result[0]['home_page'],result[0]['user_name'])
        pass
while True:
    try:
        zhp = Zhihuhomepage()
        zhp.fromdb()
        time.sleep(2 * 60 )
    except:
        pass