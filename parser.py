
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    opts = Options()
    opts.headless = True
    chrome = Chrome('chromedriver', chrome_options=opts)
    page = 25
    while True:
        url = 'https://www.detmir.ru/catalog/index/name/lego/page/{}/'.format(page)
        chrome.get(url)
        items = chrome.find_elements(By.XPATH, '//a[contains(@href,"https://www.detmir.ru/product/index/id/")]')
        index = 1
        for item in items:
            print('Item {}'.format(index,))
            p_elem = list(item.find_elements(By.TAG_NAME,'p'))
            print('Prices', len(p_elem))
            for i in p_elem:
                print(i.text)
            index += 1
            # break
        break






