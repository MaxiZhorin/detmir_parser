
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def format_price(price):
    pre_price = str(price)
    pre_price = pre_price[0:-1]
    return int(pre_price.replace(' ', ''))


def scraping(url, driver):
    global price_promo, price
    opts = Options()
    opts.headless = True
    chrome = Chrome(driver, chrome_options=opts)
    page = 21
    index = 1
    items_list = []
    while True:
        url_with_page = url + str(page)
        chrome.get(url_with_page)
        items = chrome.find_elements(By.XPATH, '//a[contains(@href,"https://www.detmir.ru/product/index/id/")]')

        for item in items:
            print('Item {}'.format(index, ))
            p_elem = list(item.find_elements(By.TAG_NAME, 'p'))
            if len(p_elem) > 1:
                id_item = item.get_attribute('href').split('/')[6]
                url_item = item.get_attribute('href')
                title = p_elem[0].text
                if len(p_elem) == 3:
                    # print(p_elem[1].text, p_elem[2].text)
                    price_promo = format_price(p_elem[1].text)
                    price = format_price(p_elem[2].text)
                    index += 1
                elif len(p_elem) == 2:
                    price = format_price(p_elem[1].text)
                    price_promo = False
                provisional_dict = {
                    'id': id_item,
                    'title': title,
                    'price': price,
                    'promo_price': price_promo,
                    'url': url_item
                }
                print(provisional_dict)
                items_list.append(provisional_dict)
            else:
                return
        page += 1

if __name__ == '__main__':
    driver = 'chromedriver'
    url = 'https://www.detmir.ru/catalog/index/name/lego/page/'
    scraping(url, driver)