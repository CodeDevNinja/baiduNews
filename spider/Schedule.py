import time
from spider.zhihu_all import Answer

if __name__ == '__main__':
    while True:
        for i in range(1,100):
            crawl1 = Answer().start()
            time.sleep(60*30)