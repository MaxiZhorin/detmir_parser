from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

def csv_dict_writer(path, data):
    """
    Метод для дампа списка словарей с товаром в csv файл
    """
    fieldnames = ['id', 'title', 'price', 'promo_price', 'url']
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def format_price(price):
    """
    Метод преобразования цены и удаления лишних знаков
    """
    pre_price = str(price)
    pre_price = pre_price[0:-1]
    return int(pre_price.replace(' ', ''))


def scraping(url, driver, page):
    """
    Создаем экземпляр Chrome, передаем путь к веб драйверу
    """
    global price_promo, price
    opts = Options()
    # Отключаем графичекий интерфейс
    opts.headless = True
    chrome = Chrome(driver, chrome_options=opts)
    page = page
    # Создаем пустой список куда будем добавлять товар при успешном парсинге
    items_list = []
    while True:
        # Запускаем безконечный цикл. Цикл прервется если у товара не будет цены, тоесть его не будет в наличии
        url_with_page = url + str(page)
        try:
            chrome.get(url_with_page)
        except Exception as ex:
            print(ex)
        # Так как названия классов меняют ищем с помощью выражения XPATH блок где есть ссылка на товар
        items = chrome.find_elements(By.XPATH, '//a[contains(@href,"https://www.detmir.ru/product/index/id/")]')

        for item in items:
            # Создаем цикл по списку товаров с 1 страницы по 'p' тегу
            p_elem = list(item.find_elements(By.TAG_NAME, 'p'))
            if len(p_elem) > 1:
                # Если 'p' тегов больше одного, то значит есть в наличии и цена. Создаем переменные с данными который
                # спарсили
                id_item = item.get_attribute('href').split('/')[6]
                url_item = item.get_attribute('href')
                title = p_elem[0].text
                # Проверяем есть ли у товара промо цена и в соответсвии создаем переменные
                if len(p_elem) == 3:
                    price_promo = format_price(p_elem[1].text)
                    price = format_price(p_elem[2].text)
                elif len(p_elem) == 2:
                    price = format_price(p_elem[1].text)
                    price_promo = False
                # После всех проверок мы готовы к созданию словаря
                provisional_dict = {
                    'id': id_item,
                    'title': title,
                    'price': price,
                    'promo_price': price_promo,
                    'url': url_item
                }
                items_list.append(provisional_dict)
            else:
                # Если товара с ценами больше нет, передаем готовый список
                return items_list
        page += 1


if __name__ == '__main__':
    driver = 'chromedriver'  # Путь к веб драйверу, я использовал версию ChromeDriver 95.0.4638.54
    url = 'https://www.detmir.ru/catalog/index/name/lego/page/'  # Линк категории
    item_list = scraping(url, driver, 1)  # Вызов функции которой передаем url, путь до веб драйвера, номер страницы
    path = "dict_output.csv"  # Название файла csv
    csv_dict_writer(path, item_list)  # Вызов метода для дампа

