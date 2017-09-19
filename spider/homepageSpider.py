#!/usr/bin/env python
# coding:utf-8
import time,random
from lxml import etree
from selenium import webdriver
import config
from MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ZHSpider():
    def __init__(self):
        self.black_page = 'https://www.zhihu.com/account/unhuman?type=unhuman&message=%E7%B3%BB%E7%BB%9F%E6%A3%80%E6%B5%8B%E5%88%B0%E6%82%A8%E7%9A%84%E5%B8%90%E5%8F%B7%E6%88%96IP%E5%AD%98%E5%9C%A8%E5%BC%82%E5%B8%B8%E6%B5%81%E9%87%8F%EF%BC%8C%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BB%A5%E4%B8%8B%E5%AD%97%E7%AC%A6%E7%94%A8%E4%BA%8E%E7%A1%AE%E8%AE%A4%E8%BF%99%E4%BA%9B%E8%AF%B7%E6%B1%82%E4%B8%8D%E6%98%AF%E8%87%AA%E5%8A%A8%E7%A8%8B%E5%BA%8F%E5%8F%91%E5%87%BA%E7%9A%84'
        self.start_url = 'https://www.zhihu.com/people/kaifulee/followers'
        #self.start_url = 'https://www.zhihu.com/people/ji-da-fa-37/activities'
        self.base_url = 'https://www.zhihu.com'
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhihu','zhihu_1')
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
        # self.browser = webdriver.Chrome(chrome_options=chromeOptions,executable_path='/home/caidong/developProgram/selenium/chromedriver')
        self.browser = webdriver.Chrome(executable_path='/home/caidong/developProgram/selenium/chromedriver')
        self.start_page = 49876
        self.end_page = 4000
    def crawlData(self, url=None):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap[
            "phantomjs.page.settings.userAgent"] = config.get_header()
        # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        #browser =webdriver.Firefox()
        self.browser.get(url)
        i=1
        if i==1:
            time.sleep(15)
            i=i+1
        # print(browser.page_source)
        self.browser.implicitly_wait(3)
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
                self.browser.find_element_by_xpath(
                    '//button[@class="Button PaginationButton PaginationButton-prev Button--plain"]').click()
                self.browser.implicitly_wait(3)
                if int(c_page) < self.start_page and int(c_page) > self.end_page:
                        self.loop_list()
                # try:
                # except:
                #          print('循环点击列表出错')
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
