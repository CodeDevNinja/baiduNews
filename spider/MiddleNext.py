#!/usr/bin/env python
# coding:utf-8


import time, random
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config


class ZHSpider():
    def __init__(self):
        self.start_url = 'https://www.zhihu.com/people/kaifulee/followers?page=25575'
        self.base_url = 'https://www.zhihu.com'
        self.type = ['hot', 'local', 'shehui', 'guonei', 'guoji', 'recomment', 'junshi', 'finance', 'technology',
                     'sports', 'fashionbang', 'fashionbang', 'auto_moto', 'fangcan', 'technology', 'yangshengtang']
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhihu','zhihu_1')
        self.page = 2
        self.totla_url_set = set()
        self.wait_use_url_set = set()
        self.current_type = ''

    def crawlData(self, url=None):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        browser = webdriver.Chrome('/home/caidong/developProgram/selenium/chromedriver')
        browser.get(url)
        # print(browser.page_source)
        browser.implicitly_wait(10)
        # print(browser.page_source)
        # 点击关注者
        #browser.find_element_by_xpath('//div[@class="NumberBoard FollowshipCard-counts"]').click()
        #time.sleep(2)
        # for i in range(1,10):
        #     if i<9:
        #         bt_mouseover = browser.find_element_by_xpath('//li[@class="nav_item"]['+str(i)+']/a')
        #         actions =ActionChains(browser)
        #         actions.move_to_element(bt_mouseover).perform()
        #         browser.implicitly_wait(5)
        #         time.sleep(5)
        #         html = browser.page_source
        #         #print(html)
        #         self.current_type=self.type[i]
        #         self.parse(html)
        #     else:
        #         more = browser.find_elements_by_xpath('//div[@class="more_list"]/a')
        #         i=1
        #         for item in more:
        #             if i < 2:
        #                 bt_mouseover = browser.find_element_by_xpath('//a[@class="more"]')
        #             else:
        #                 bt_mouseover = browser.find_element_by_xpath('//a[@class="more more_current"]')
        #             i += 1
        #             actions = ActionChains(browser)
        #             actions.move_to_element(bt_mouseover).perform()
        #             time.sleep(60)
        #             browser.implicitly_wait(50)
        #             try:
        #                 item.click()
        #             except:
        #                 print ("click error")
        #             browser.implicitly_wait(15)
        #             html = browser.page_source
        #             self.current_type = self.type[i+6]
        #             print(self.current_type)
        #             #print(html)
        #             self.parse(html)
        #             #actions.click(item)
        #             time.sleep(2)

        # browser.get_screenshot_as_file('1.png')
        # print(browser.page_source)
        # exit()
        # if index <= 6:
        #     bt_element=('//div[@class="fieed-box"]/a[@id="%s"]'%xpath_str)
        # else:
        #     actions = ActionChains(browser)
        #     more = browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="more_anchor"]')
        #     actions.move_to_element(more).perform()
        #     bt_element=('//div[@class="tab-box-pop"]/a[@id="%s"]'%xpath_str)
        # #if index > 6:
        #  browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="pc_6"]').click()
        # time.sleep(2)

        # time.sleep(2)
        # actions.move_to_element(more).perform()
        # browser.find_element_by_xpath(bt_element).click()
        # time.sleep(2)
        #
        # #browser.get_screenshot_as_file('tex.png')
        # js1 = 'return document.body.scrollHeight'
        # js2 = 'window.scrollTo(0, document.body.scrollHeight)'
        # old_scroll_height = 0
        # while(browser.execute_script(js1) > old_scroll_height):
        #     old_scroll_height = browser.execute_script(js1)
        #     browser.execute_script(js2)
        #     time.sleep(0.8)
        # for i in range(self.page):
        #     load_more_xpath='//div[@class="jzgd"]/a'
        #     browser.find_element_by_xpath(load_more_xpath).click()
        #self.parse(browser.page_source, url)
        # print(browser.page_source)
        # try:
        more = browser.find_elements_by_xpath('//button[@class="Button PaginationButton Button--plain"]')
        # except:
        #     print('没有下一页')
        # for page in range(len(more)):
        #     browser.find_elements_by_xpath('//button[@class="Button PaginationButton Button--plain"]')[page].click()
        #     time.sleep(2)
        #     self.parse_page(browser.page_source)
        # browser.find_element_by_xpath('//button[@class="Button PaginationButton PaginationButton-next Button--plain"]').click()
        ######每一次执行下一页
        total_page = more[-1].text
        print("tot", total_page)
        for curren_page in range(int(total_page)):
            try:
                browser.find_element_by_xpath(
                    '//button[@class="Button PaginationButton PaginationButton-next Button--plain"]').click()
                time.sleep(2)
            except:
                print('没有下一页')
            self.parse_page(browser.page_source)
        # exit()
        ######end


        browser.quit()

    def parse_page(self, html):
        tree = etree.HTML(html)
        followerList = tree.xpath('//div[@class="List-item"]')
        # print(followerList)
        for item in followerList:
            followerInfo = etree.ElementTree(item)
            name = followerInfo.xpath("//a[@class='UserLink-link']/text()")[0]
            home_page = followerInfo.xpath("//a[@class='UserLink-link']/@href")[0]  # 主页
            follower_c = followerInfo.xpath("//span[@class='ContentItem-statusItem']/text()")[2]
            # print('---------',home_page)
            if home_page and self.base_url + home_page not in self.totla_url_set:
                self.wait_use_url_set.add(self.base_url + home_page)
                self.totla_url_set.add(self.base_url + home_page)
                zhihuObj = dict(user_name=name, followers=follower_c[:-3].strip(),
                                home_page=home_page, collect='none'
                                )
                self.saveDB(zhihuObj, name)
            print(name, home_page, follower_c)

    def parse(self, html, url):
        tree = etree.HTML(html)
        follow = tree.xpath("//div[@class='NumberBoard-value']/text()")
        follower = follow[1]
        # print('====',follower,type(int(follower)))
        if int(follower) > 0:
            followerList = tree.xpath('//div[@class="List-item"]')
            # print(followerList)
            for item in followerList:
                followerInfo = etree.ElementTree(item)
                name = followerInfo.xpath("//a[@class='UserLink-link']/text()")[0]
                home_page = followerInfo.xpath("//a[@class='UserLink-link']/@href")[0]  # 主页
                follower_c = followerInfo.xpath("//span[@class='ContentItem-statusItem']/text()")[2]
                # print('---------',home_page)
                if home_page and self.base_url + home_page not in self.totla_url_set:
                    self.wait_use_url_set.add(self.base_url + home_page)
                    self.totla_url_set.add(self.base_url + home_page)
                    zhihuObj = dict(user_name=name, followers=follower_c[:-3].strip(),
                                    home_page=home_page, collect='none'
                                    )
                    self.saveDB(zhihuObj, name)
                print(name, home_page, follower_c)
        user_name = tree.xpath("//span[@class='ProfileHeader-name']/text()")[0]
        collecter = tree.xpath("//div[@class='Profile-sideColumnItemValue']/text()")
        # time.sleep(2)
        flowing = follow[0]
        if collecter:
            save = collecter[2][:-3].strip()
        else:
            save = 0
        # print(save)
        # print(html)
        print(user_name, flowing, save)
        zhihuObj = dict(user_name=user_name, followers=follower, flowing=flowing,
                        collect=save, home_page=url
                        )
        # zhihuContent = {'user_name':user_name,'followers':follower,"flowing":flowing,"save":save,}
        if self.SqlH.count({'user_name': user_name}) == 0:
            self.SqlH.insertZhiHu(zhihuObj)
        elif self.SqlH.count({'user_name': user_name, 'collect': 'none'}):
            self.SqlH.update({'user_name': user_name}, {'collect': save})
            # print(zhihuContent)

    def saveDB(self, content, user_name):
        if self.SqlH.count({'user_name': user_name}) == 0:
            self.SqlH.insertZhiHu(content)
        elif self.SqlH.count({'user_name': user_name, 'collect': 'none'}):
            self.SqlH.update({'user_name': user_name}, {'collect': 'none'})
        pass
        # updatetime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        # news_content = tree.xpath("//div[@class='data_row news_photoview clearfix ']|//div[@class='data_row news_article clearfix ']")
        # for item in news_content:
        #     content = etree.ElementTree(item)
        #     imgUrl =content.xpath("//img/@src")
        #     txtTitle = content.xpath("//h3/a/text()")
        #     detail_url = content.xpath("//h3/a/@href")
        #     print(imgUrl)
        #     print(txtTitle)
        #     print(detail_url)
        # wxContent = {'title': txtTitle, 'url': detail_url, 'content': '',
        #              'category': self.current_type,
        #              'secCategory': '', 'image': imgUrl, 'time': updatetime, 'from': 'WX'}
        # if self.SqlH.count({'title': txtTitle}) == 0:
        #     self.SqlH.insert(wxContent)
        # print(updatetime)
        # imgUrl = '//div[@class="ndi_main"]//img/@src'
        # txtTitle = '//div[@class="ndi_main"]//h3/a/text()'
        # detail_url = '//div[@class="ndi_main"]//h3/a/@href'
        # #txt_content = '//ul[@class="news-list"]/li/div[@class="txt-box"]/p/text()'
        # wx_item_detail_url= tree.xpath(detail_url)
        # wx_item_img_url = tree.xpath(imgUrl)
        # wx_item_text = tree.xpath(txtTitle)
        # #wx_item_content = tree.xpath(txt_content)
        # print(len(wx_item_detail_url))
        # print(len(wx_item_img_url))
        # print(len(wx_item_text))
        # #print(len(wx_item_content))
        # print(wx_item_content)
        # print(wx_item_text)
        # for i in range(0,len(news_text)):
        #  if 'http' in news_url[i]:
        #     newsContent  = {'title': news_text[i], 'url': news_url[i], 'content': '', 'category': item,
        #        'secCategory': '', 'image': '', 'time': updatetime, 'from': ''}
        #     count = SqlH.select(1, {'title': news_text[i]})
        #     #print(count)
        #     if len(count) == 0:
        #         SqlH.insert(newsContent)


if __name__ == '__main__':
    crawl = ZHSpider()
    # html = crawl.crawlData(crawl.start_url)
    # content = crawl.parse(html)
    # crawl.SqlH.insert(content)
    # use_url_set=list(crawl.wait_use_url_set.copy())
    # time.sleep(2)
    # print(use_url_set)
    use_url_set = [crawl.start_url]
    html = crawl.crawlData(crawl.start_url)
    while True:
        for url in use_url_set:
            print("使用：" + url)
            # if crawl.SqlH.count({"home_page":url,"collect":"none"})!=0:
            try:
                html = crawl.crawlData(url)
                # content = crawl.parse(html, url)
                # if crawl.SqlH.count({"title": content["title"]}) == 0:
                # crawl.SqlH.insert(content)
                # print("入库")
                time.sleep(random.randrange(1, 1.2))
            except:
                continue
        use_url_set = list(crawl.wait_use_url_set.copy())
        crawl.wait_use_url_set = set()
        #     crawl = ZHSpider()
        #     html = crawl.crawlData(crawl.start_url)
        # #    content = crawl.parse(html)
        #     #crawl.SqlH.insert(content)
        #     use_url_set = crawl.wait_use_url_set
        #     #time.sleep(1)
        #     print(use_url_set)
        #     for url in use_url_set:
        #         if url != "":
        #             html = crawl.crawlData(url)
        #             #content = crawl.parse(html)
        #             #crawl.SqlH.insert(content)
        #         else:
        #             use_url_set = crawl.wait_use_url_set
        # while True:
        #     wx = WXSpider()
        #     wx.spider()
        #     time.sleep(2 * 60 * 60)