# coding:utf-8
from lxml import etree
from selenium import webdriver
class ToutiaoCrawl:
    def __init__(self):
        pass
    def spider(self):
        browser=webdriver.PhantomJS()
        browser.get('https://www.toutiao.com/ch/news_hot/')
        browser.implicitly_wait(1)
        print (browser.page_source)

if __name__ == '__main__':
 tt = ToutiaoCrawl()
 tt.spider()