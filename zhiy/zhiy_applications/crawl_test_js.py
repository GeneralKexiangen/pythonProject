# -*- coding: utf-8 -*-

import sys

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = "/opt/homebrew/bin/chromedriver"
headers = {
    'Accept': 'application/json, text/plain, */*    ',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'Host': 'sthjt.hubei.gov.cn',
    # 'Pragma': 'no-cache',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Host': 'sthjt.hubei.gov.cn',
#     'Pragma': 'no-cache',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

def get_cookies():
    option = Options()
    option.add_argument("--incognito")  # 配置隐私模式
    # option.add_argument('--headless')  # 配置无界面
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=path, options=option)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator,'webdriver',{
                get: () => undefined
            })
        """
    })
    driver.get('https://fahuo.cainiao.com/consigns/order/ggSend.htm?tab=tb_order')
    #driver.get('http://sthjt.hubei.gov.cn/site/sthjt/search.html?searchWord=%E7%A2%B3%E6%8E%92%E6%94%BE&siteId=41&pageSize=10')
    # driver.maximize_window()

    data = driver.get_cookies()
    cookie = {}
    cookie.update({'cookie2': data[0].get('value')})
    cookie.update({'_tb_token_': data[1].get('value')})
    cookie.update({'t': data[2].get('value')})
    # cookie.update({'token': data[3].get('value')})
    # cookie.update({'JSESSIONID': data[4].get('value')})


    # cookie.update({'uuid': data[0].get('value')})
    # cookie.update({'FSSBBIl1UgzbN7N80T': data[1].get('value')})
    # cookie.update({'FSSBBIl1UgzbN7N80S': data[2].get('value')})
    # cookie.update({'token': data[3].get('value')})
    # cookie.update({'JSESSIONID': data[4].get('value')})
    driver.close()
    print(cookie)
    return cookie

cookie = get_cookies()
url = 'https://fahuo.cainiao.com/consigns/normal/order/queryV2.do?sortBy=max_sort_time&sortType=asc&pageSize=50&pageTab=4&currentPage={0}&hasBuyerMemo=false&hasUserMemo=false&ggService=false&userFlag=-1&lock=false&applyRefund=false&tradeClose=true&startTradeCreateTime=2022-02-23%2000%3A00%3A00&endTradeCreateTime=2022-03-09%2023%3A59%3A59&receiveDivisionIds='
#url = 'https://sthjt.hubei.gov.cn/igs/front/search.jhtml?code=03074fc5eaae4cd5b5be57bd3fe4e9b6&pageNumber={0}&pageSize=10&queryAll=true&searchWord=%E7%A2%B3%E6%8E%92%E6%94%BE&siteId=41'
lis = [i for i in range(1, 3)]
for page, n in enumerate(lis):
    response = requests.get(url.format(page), headers=headers, cookies=cookie)
    response.encoding = response.apparent_encoding
    x = 100
    y = (page + 1) / len(lis)
    done = int(x * y)
    if response.status_code != 200:
        cookie = get_cookies()
        response = requests.get(url.format(page), headers=headers, cookies=cookie)
    else:
        print(response.text)
    done = int(x * y)
    sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (100 - done), x * y) + '\n')
    sys.stdout.flush()
