import time
import requests
from db import add_new_car
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) '
                         'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

url = """
https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=9&model.
id[0]=96&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=
1&generation.id[0][0]=425&generation.id[0][1]=10149&page=0&size=100
"""

print("[x] Script started")

while True:

    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        print(f"[x] Status code {response.status_code} | Connection set")
        soup = BeautifulSoup(response.text, 'html.parser')
        print('[x] Gathering info')
        content_bars = soup.find_all('div', class_='content-bar')

        for car in content_bars:
            try:
                title = car.find('div', class_='head-ticket')
                title = title.text.strip() if title else 'Не вказано'

                details = car.find('div', class_='generation')
                details = details.text.strip() if details else 'Не вказано'

                price_div = car.find('div', class_='price-ticket')
                price_usd = price_div.get('data-main-price') if price_div else 'Не вказано'

                characteristics_ul = car.find('ul', class_='unstyle characteristic')
                li_elements = characteristics_ul.find_all('li', class_='item-char') if characteristics_ul else []

                mileage = li_elements[0].text.strip() if len(li_elements) > 0 else 'Не вказано'
                location = li_elements[1].text.strip().replace("( від )", "") if len(li_elements) > 1 else 'Не вказано'
                fuel_type = li_elements[2].text.strip() if len(li_elements) > 2 else 'Не вказано'
                transmission = li_elements[3].text.strip() if len(li_elements) > 3 else 'Не вказано'

                plate = car.find("span", class_='state-num ua')
                plate = plate.text.strip().replace("  Ми розпізнали держномер авто на фото та перевірили його за реєстрами МВС.", "").replace(" ", "") if plate else 'Не вказано'

                vin_code = car.find('span', class_='label-vin')
                vin_code = vin_code.text.strip().replace(
                    "    AUTO.RIA перевірив VIN-код і порівняв інформацію від продавця з даними реєстрів МВС.  "
                    "Перевірити всю історію авто", ""
                ) if vin_code else 'VIN не вказано'

                link_tag = car.find('a', class_='address')
                link = link_tag.get('href') if link_tag else 'Не вказано'

                add_new_car(title, price_usd, mileage, location, fuel_type, transmission, plate, vin_code, link, details)

            except AttributeError as e:
                print(f'Error: {e}')
        print('[x] Check is 15 minutes')
        time.sleep(900)
    else:
        print(f'[x] {response.status_code}')



