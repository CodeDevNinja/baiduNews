#!/usr/bin/env python
# coding:utf-8
import time,random
from lxml import etree
from selenium import webdriver
import config
from MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from spider.Zhihulogin import ZhihuLogin


class ZHSpider():
    def __init__(self):
        self.black_page = 'https://www.zhihu.com/account/unhuman?type=unhuman&message=%E7%B3%BB%E7%BB%9F%E6%A3%80%E6%B5%8B%E5%88%B0%E6%82%A8%E7%9A%84%E5%B8%90%E5%8F%B7%E6%88%96IP%E5%AD%98%E5%9C%A8%E5%BC%82%E5%B8%B8%E6%B5%81%E9%87%8F%EF%BC%8C%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BB%A5%E4%B8%8B%E5%AD%97%E7%AC%A6%E7%94%A8%E4%BA%8E%E7%A1%AE%E8%AE%A4%E8%BF%99%E4%BA%9B%E8%AF%B7%E6%B1%82%E4%B8%8D%E6%98%AF%E8%87%AA%E5%8A%A8%E7%A8%8B%E5%BA%8F%E5%8F%91%E5%87%BA%E7%9A%84'
        self.start_url = 'https://www.zhihu.com/people/kaifulee/followers?page=25583'
        #self.start_url = 'https://www.zhihu.com/people/ji-da-fa-37/activities'
        self.base_url = 'https://www.zhihu.com'
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhihu','zhihu_48000')
        #self.browser = webdriver.PhantomJS()
        # proxy = {'address': '60.168.104.30:3128',
        #          'username': 'user11',
        #          'password': '123'
        #           }
        # capabilities = dict(DesiredCapabilities.CHROME)
        # capabilities['proxy'] = {'proxyType': 'MANUAL',
        #                          'httpProxy': proxy['address'],
        #                          'ftpProxy': proxy['address'],
        #                          'sslProxy': proxy['address'],
        #                          'noProxy': '',
        #                          'class': "org.openqa.selenium.Proxy",
        #                          'autodetect': False}
        #
        # capabilities['proxy']['httpUsername'] = proxy['username']
        # capabilities['proxy']['httpPassword'] = proxy['password']
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--proxy-server=http://60.168.104.30:3128')
        #self.browser = webdriver.Chrome(chrome_options=chromeOptions,executable_path='/home/caidong/developProgram/selenium/chromedriver')
        #self.browser = webdriver.PhantomJS()
        #cookies = ZhihuLogin().login()
        #print(cookies)
        self.browser = webdriver.PhantomJS()
        self.browser = webdriver.Chrome(executable_path='/home/caidong/developProgram/selenium/chromedriver')
        #for cookie in cookies:
          #  self.browser.add_cookie({cookie['name']:cookie['value']})
        #self.browser.add_cookie(cookie)
        time.sleep(5)
        print('cookie',self.browser.get_cookies())
        #print(self.browser.get_cookies())
        #self.browser.add_cookie({"cookie":'_zap=b24c85f0-aae0-456a-ba87-e0919de79409; __utma=243313742.618834370.1505397831.1505397831.1505431589.2; __utmz=243313742.1505397831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); d_c0="AJCCExnEYAyPTuiuB47mCQN_anS_LW2ZmQI=|1505432287"; q_c1=f92e81f1440d49eca643b9bd71df1d06|1505471670000|1502586350000; aliyungf_tc=AQAAABpahiv+pQIA4wmi0wpuOA0ptCdt; __utma=51854390.226003310.1505817316.1505817316.1505817316.1; __utmc=51854390; __utmz=51854390.1505817316.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20170813=1; XSRF-TOKEN=2|02bd5b9f|30893afa3ad96af92f8d3ffb67906faa338d76fe308d3fb267de6cad358569a837dc39ae|1505824255; _xsrf=24ae8d1f-0dde-4510-a20d-ec7278275ab1; l_cap_id="NDYzOWZmNjBmZDhjNDBkZWI5MDg0NjYyZDk4YTk2OTA=|1505824625|220e4527cbfe214589599d071685e4c7f62143fc"; r_cap_id="NWJhOTRmYzg2NTVlNDczY2ExZWY3YzgxNGQ2ZmRmM2I=|1505824625|b050327da2a8dedc37a8e744640b60b553f3b771"; cap_id="YjcyNGZkYjFlY2JkNDU3ZWFlYmQ0NjQ3ZDJmNDcwZjk=|1505824625|5804f3f4999cf311334c3664f2e41ad2d4d93029'})
        self.start_page = 48000
        self.end_page = 47000
    def crawlData(self, url=None):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap[
            "phantomjs.page.settings.userAgent"] = config.get_header()
        # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        #browser =webdriver.Firefox()
        self.browser.get(url)
        i=1
        if i==1:
            time.sleep(30)
            i=i+1
        # print(browser.page_source)
        self.browser.implicitly_wait(3)
        print('cookie',self.browser.get_cookies())
        print(self.browser.page_source)
        # 点击关注者
        self.browser.find_element_by_xpath('//div[@class="NumberBoard FollowshipCard-counts"]').click()
        self.browser.implicitly_wait(3)
        more = self.browser.find_elements_by_xpath('//button[@class="Button PaginationButton Button--plain"]')
        more[-1].click()
        self.browser.implicitly_wait(3)
        total_page = more[-1].text
        c_page = self.browser.find_element_by_xpath('//button[@class="Button PaginationButton PaginationButton--current Button--plain"]').text
        print(c_page)
        for curren_page in range(int(total_page)):
                c_page = self.browser.find_element_by_xpath(
                '//button[@class="Button PaginationButton PaginationButton--current Button--plain"]').text
                print(c_page)
                print('当前页:', str(curren_page))

                #点击上一页
                # self.browser.find_element_by_xpath(
                #     '//button[@class="Button PaginationButton PaginationButton-prev Button--plain"]').click()
               #点击下一页
                self.browser.find_element_by_xpath(
                    '//Button PaginationButton PaginationButton-next Button--plain"]').click()
                self.browser.implicitly_wait(3)
                if int(c_page) < self.start_page and int(c_page) > self.end_page:
                 try:
                    self.loop_list()

                 except:
                          print('循环点击列表出错')
    #循环解析当前列表
    def loop_list(self):
        items = self.browser.find_elements_by_xpath('//div[@class="ContentItem-head"]//a[@class="UserLink-link"]')
        print("数目",len(items))
        for item in items:
            time.sleep(random.randrange(5))
            c_url= item.get_attribute("href")
            print("c_url",c_url)
            if self.SqlH.count({"home_page":c_url+'/activities'})==0:
                #不出现点击点问题
                while not item.is_displayed():
                    time.sleep(1)
                try:
                    item.click()
                except:
                    print('点击错误')
                self.browser.implicitly_wait(1)
                handle_cnt = len(self.browser.window_handles) - 1
                # print('标签数',handle_cnt)
                self.browser.switch_to.window(self.browser.window_handles[handle_cnt])
                print(self.browser.current_url)
                if  self.browser.current_url==self.black_page:
                    time.sleep(10*60)
                try:
                    self.browser.implicitly_wait(3)
                    self.parse_home_page(self.browser.page_source, self.browser.current_url)
                except:
                     print("页面解析错误")
                if handle_cnt > 0:
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
            else:
                print("已存在")
            time.sleep(random.randrange(2))
    #存储数据到mongodb
    def storage_mongod(self,dic):
        user_name =dic.get("user_name")
        if self.SqlH.count({'user_name': user_name}) == 0:
            self.SqlH.insertZhiHu(dic)
        else:
            self.SqlH.update({'user_name': user_name}, {'collect': dic.get('collect')})
        pass

    def parse_home_page(self, html,url):
        tree = etree.HTML(html)
        follow = tree.xpath("//div[@class='NumberBoard-value']/text()")
        if follow:
            flowing = follow[0]
            follower = follow[1].strip()
        else:
            flowing = 'none'
            follower = 'none'
        page_header = tree.xpath("//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']/a/span/text()")
        answer = page_header[0]
        article = page_header[2]
        #print('answer_',answer,'article',article)
        user_name = tree.xpath("//span[@class='ProfileHeader-name']/text()")[0]
        collecter = tree.xpath("//div[@class='Profile-sideColumnItemValue']/text()")
        print("收藏数",collecter)
        if collecter:
            for item in collecter:
                if str(item).endswith("次收藏"):
                    save=item.strip()[:-3]
                else:
                    save = 0
        else:
            save = 0
        print(user_name, flowing,str(save))
        zhihuObj = dict(user_name=user_name, followers=follower,
                        home_page=url, collect=save,article=article,
                        answer=answer)
        try:
            self.storage_mongod(zhihuObj)
        except:
            print("数据存储错误")
        #
        # if int(follower) > 0:
        #     followerList = tree.xpath('//div[@class="List-item"]')
        #     for item in followerList:
        #         followerInfo = etree.ElementTree(item)
        #         name = followerInfo.xpath("//a[@class='UserLink-link']/text()")[0]
        #         home_page = followerInfo.xpath("//a[@class='UserLink-link']/@href")[0]  # 主页
        #         follower_c = followerInfo.xpath("//span[@class='ContentItem-statusItem']//div[@class='NumberBoard-value']/text()")
        #





if __name__ == '__main__':
    crawl = ZHSpider()
    crawl.crawlData(crawl.start_url)
    crawl.browser.quit()
