from selenium import webdriver
import time
from PIL import Image
from io import StringIO,BytesIO
import urllib.request

from selenium.webdriver import ActionChains


class ZhihuLogin():
    def __init__(self):
        self.login_url='https://www.zhihu.com'
        self.browser = webdriver.Chrome(executable_path='/home/caidong/developProgram/selenium/chromedriver')

    def login(self):
        self.browser.get(self.login_url)
        self.browser.implicitly_wait(2)
        self.browser.find_elements_by_xpath('//div[@class="navs-slider"]/a')[1].click()
        self.browser.implicitly_wait(2)
        #time.sleep(5)
        #qrc=self.browser.find_element_by_xpath('//div[@class="qrcode-signin-img-wrapper"]/img').get_attribute("src")
        #print(qrc)
        #self.browser.close()
        self.browser.find_element_by_xpath('//span[@class="signin-switch-password"]').click()
        self.browser.implicitly_wait(2)
        self.browser.find_element_by_xpath('//div[@class="account input-wrapper"]/input').send_keys('13197670564')
        self.browser.find_element_by_xpath('//div[@class="verification input-wrapper"]/input').send_keys('111111')
        self.browser.implicitly_wait(3)
        captcha = self.browser.find_elements_by_xpath('//img[@class="Captcha-image"]')[0]
        ac = ActionChains(self.browser)
        points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                  [129.796875, 22], [150.796875, 22]]
        time.sleep(10)
        seq = input('请输入倒立字的位置\n>')
        for i in seq:
            print(i)
            i=int(i)
            ac.move_to_element_with_offset(captcha,points[i][0],points[i][1]).click().perform()
            time.sleep(1)
            ac.move_to_element_with_offset(captcha,points[i][0],points[i][1]).release().perform()

            ac.move_to_element_with_offset(captcha,points[i+1][0],points[i+1][1]).perform()
            ac.move_to_element_with_offset(captcha,points[i-1][0],points[i-1][1]).perform()
            ac.move_to_element_with_offset(captcha,points[1][0],points[i][1]).click().perform()
            ac.move_to_element_with_offset(captcha,points[1][0],points[i][1]).click().perform()

            time.sleep(1)

            # for j in range(5):
            #     ac.move_by_offset(0.1, 0.1).perform()
            #     time.sleep(0.2)
            #     #time.sleep(0.1)
            #     ac.move_by_offset(0.1,0.1).perform()
                #ac.move_to_element_with_offset(captcha,points[i][0],points[i][1]).release()
                #ac.move_to_element_with_offset(captcha,points[2][0],points[2][1]).perform()
                #ac.move_to_element_with_offset(captcha,points[3][0],points[3][1])

            time.sleep(2)
            self.browser.implicitly_wait(2)
        time.sleep(10)
        self.browser.find_element_by_xpath('//div[@class="view view-signin"]//div[@class="button-wrapper command"]/button["sign-button submit"]').click()
       # file = BytesIO(urllib.request.urlopen(qrc).read())
       # img = Image.open(file)
        #img.show()
        cookies = self.browser.get_cookies()
        #self.browser.close()
        #print(cookies)
        return cookies
    def captcha(self):
        points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                  [129.796875, 22], [150.796875, 22]]

if __name__ == '__main__':
    zl = ZhihuLogin()
    zl.login()