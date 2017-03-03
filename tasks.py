import settings

from random import choice

from celery import Celery
import couchdb
import requests
import lxml.html


queue = Celery('tasks', broker=settings.BROKER_URL)
couch = couchdb.Server(settings.DB_URL)
db = couch['queue']


class Fetcher:
    https_proxies = [
        "212.144.222.27:3128",
        "5.9.84.210:80",
        "185.2.101.31:3128",
        "212.224.76.176:80",
        "138.201.63.123:31288",
        "5.196.7.246:80",
        "46.4.38.139:8080",
        "195.158.139.46:3128",
    ]
    user_agents = [
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    ]

    def __init__(self):
        self.amazon_base_url = 'https://www.amazon.de/'
        self.proxy = {'https': choice(self.https_proxies)}
        print('using ip: ' + self.proxy['https'])
        self.user_agent = choice(self.user_agents)

        self.headers = requests.utils.default_headers()
        self.headers.update({'User-Agent': choice(self.user_agents)})
        self.doc = {}

    def dump_html(self, html):
        with open('product.html', 'wb') as file:
            for block in html.iter_content(1024):
                file.write(block)

    def check_bot(self):
        title = self.dom.xpath('/html/head/meta[4]')
        title_text = title[0].attrib['content']
        if title_text == 'Bot Check':
           from ipdb import set_trace; set_trace() 

    def amazon_url_product(self, asin):
        return '{}dp/{}'.format(self.amazon_base_url, asin)

    def fetch(self, asin):
        product_url = self.amazon_url_product(asin)
        html = requests.get(product_url, proxies=self.proxy, headers=self.headers)
        self.dump_html(html)
        self.dom = lxml.html.fromstring(html.content)
        self.check_bot()
        self.doc = {
            'title': self.get_title(),
            'price': self.get_price(),
            'seller': self.get_seller(),
        }
        from ipdb import set_trace; set_trace()

    def get_title(self):
        return self.dom.xpath('//*[@id="productTitle"]/text()')[0].strip()

    def get_price(self):
        from ipdb import set_trace; set_trace()
        scraped_price = self.dom.xpath('//*[starts-with(@id, "priceblock_")]/text()')[3]
        currency_slice = slice(0, 3)
        price_slice = slice(4, None)
        price = scraped_price[price_slice]
        currency = scraped_price[currency_slice]
        price_type = self.dom.xpath('//*[starts-with(@id, "priceblock_")]')[2].attrib['id']
        return {'price': price, 'currency': currency, 'priceType': price_type}

    def get_seller(self):
        elem = self.dom.xpath('//*[@id="merchant-info"]/a[1]')[0]
        seller = elem.text_content()
        sellerURL = elem.attrib['href']
        return {'name': seller, 'amazonURL': sellerURL}


class Product:
    def __init__(self, asin):
        self.asin = asin
        self.doc = self.get_product(asin)

    def get_product(self, asin):
        try:
            doc = db[asin]
            print('doc was in db')
        except couchdb.http.ResourceNotFound:
            print('fetching doc')
            doc = self.fetch_product(asin)

    def fetch_product(self, asin):
        fetcher = Fetcher()
        fetcher.fetch(asin)


@queue.task
def get_product(asin):
    product = Product(asin)
