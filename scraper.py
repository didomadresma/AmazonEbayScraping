from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import base64
import codecs

class Amazon:

    def __init__(self):
        self.url = 'https://www.amazon.fr/gp/product/{}'
        self.ua = UserAgent().chrome
        pass

    def fetch_product_page(self, asin):
        headers = {
            'User-Agent': self.ua
        }

        page = requests.get(self.url.format(asin), headers=headers)
        return page

    def get_product_from_amazon(self, asin):
        page = self.fetch_product_page(asin)
        soup = BeautifulSoup(page.text, 'html.parser')

        try:
            product_section = soup.find(id='dp-container')
            left_column = product_section.find(id='leftCol')
            center_column = product_section.find(id='centerCol')
            right_column = product_section.find(id='rightCol')

            title = center_column.find(id='title_feature_div').find(id='productTitle').get_text().strip()

            price = center_column.find(id='price_feature_div').find('span', id=re.compile(r'priceblock_.*price')).get_text()
            price = float(price.replace('EUR', '').replace(',', '.').strip())

            # main_image = left_column.find(id='main-image-container').find('img', id='landingImage')['src']
            main_image = left_column.find(id='main-image-container').find('img', id='landingImage')['data-old-hires']
            alt_images = left_column.find(id='altImages').find_all('img')
            alt_images = [x['src'] for x in alt_images]

        except Exception as e:
            print(e)


class Ebay:

    def __init__(self):
        self.amazon = Amazon()
        pass

    def upload_product_on_ebay(self, asin):
        pass


if __name__ == "__main__":
    # soup = BeautifulSoup(open('/Users/shubhampatil/Downloads/Dishonored.htm'), 'lxml')
    amazon = Amazon()
    amazon.get_product_from_amazon('B00NMAWY7M')

