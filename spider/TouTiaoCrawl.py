# coding:utf-8
from lxml import etree
from selenium import webdriver

class ToutiaoCrawl:
    def __init__(self):
        pass
    def spider(self):
        browser=webdriver.Chrome('/home/caidong/developProgram/selenium/chromedriver')
        browser.get('https://www.toutiao.com/ch/news_hot/')
        browser.implicitly_wait(1)

        print (browser.page_source)
    def parse(self,html):
        xhtml=etree.HTML(html)
        xhtml.xpath()

if __name__ == '__main__':
 tt = ToutiaoCrawl()
 tt.spider()