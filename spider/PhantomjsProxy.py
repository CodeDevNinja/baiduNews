import base64
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

service_args = [
    '--ignore-ssl-errors=true',
    '--proxy=114.97.204.196:3129',
    '--proxy-type=http',
]

authentication_token = "Basic " + base64.b64encode(b'user11:123').decode('utf-8')
print(authentication_token)
authentication_token = 'Basic dXNlcjE0OjEyMw=='
capa = DesiredCapabilities.PHANTOMJS
capa['phantomjs.page.customHeaders.Proxy-Authorization'] = authentication_token
driver = webdriver.PhantomJS(desired_capabilities=capa, service_args=service_args)
#driver = webdriver.PhantomJS(service_args=service_args)
# driver = webdriver.Firefox()  # Optional argument, if not specified will search path.
driver.get('http://1212.ip138.com/ic.asp');
driver.implicitly_wait(10)
print(driver.page_source)
# time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
