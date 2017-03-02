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
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    ]

    def __init__(self):
        self.proxy = {'https': choice(self.https_proxies)}
        print('using ip: ' + self.proxy['https'])
        self.user_agent = choice(self.user_agents)

        self.headers = requests.utils.default_headers()
        self.headers.update({'User-Agent': choice(self.user_agents)})


    def fetch(self, asin):
        from ipdb import set_trace; set_trace()


class Product:
    def __init__(self, asin):
        self.asin = asin
        self.doc = self.get_product(asin)

    def get_product(self, asin):
        try:
            doc = db[asin]
            print('doc was in db')
        except couchdb.http.ResourceNotFound:
            doc = self.fetch_product(asin)
            print('fetching doc')

    def fetch_product(self, asin):
        fetcher = Fetcher()
        fetcher.fetch(asin)


@queue.task
def get_product(asin):
    product = Product(asin)
