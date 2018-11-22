from enum import Enum
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from product import Option

class Ticker(Enum):
    CACPXA = 'PXA-DPAR'
    CAC1PX = '1PX-DPAR'
    CAC2PX = '2PX-DPAR'
    CAC4PX = '4PX-DPAR'
    CAC5PX = '5PX-DPAR'

class Page:
    """
    liste des options euronext CAC40 :
    https://derivatives.euronext.com/en/equity-index-derivatives/contract-list?quicktabs_309=4#quicktabs-309
    """
    def __init__(self, site=None, ticker=None, expiry=None, ticker_idx=0, params=None):
        self.tickers = ['PXA-DPAR', '4PX-DPAR', '2PX-DPAR', '1PX-DPAR', '5PX-DPAR']
        # liste des options euronext CAC40 :
        # https://derivatives.euronext.com/en/equity-index-derivatives/contract-list?quicktabs_309=4#quicktabs-309
        self.site = "https://derivatives.euronext.com/fr/products/index-options" if not site else site
        self.expiry = expiry
        if params:
            self.params = params
        else:
            self.params = urlencode({'Class_type': 0,
                                     'Class_symbol': None,
                                     'Class_exchange': None,
                                     'ex': None,
                                     'ps': 999,
                                     'md': self.expiry
                                    })
        self.ticker = ticker.value if ticker else self.tickers[ticker_idx]

    @property
    def _url(self):
        return "{}/{}?{}".format(self.site, self.ticker, self.params)
        
    def fetch(self, return_content=False):
        requete = requests.get(self._url)
        page = requete.content
        self.soup = BeautifulSoup(page, features="html.parser")
        self.page_title = self.soup.find("h1", {"class": "title"}).text
        self.call = {}
        self.put = {}
        if return_content:
            return self.soup

    def scrap_options(self, multiplier=1):
        div = self.soup.find("div", {"class": "call-put-table"})
        trs = div.find_all("tr")
        elmts = {}
        self.call = {}
        self.put = {}
        self.data = []
        for tr in trs[3:-1]:
            tds = tr.find_all('td')
            self.data.append([td.text for td in tds])
            strike = float(tds[7].text)
            if (str(tds[4].text) != '-' and
                str(tds[5].text) != '-'):
                vente = float(tds[4].text)
                achat = float(tds[5].text)
                c = Option('Call', strike=strike, achat=achat, vente=vente, multiplier=multiplier)
                self.call[float(c.strike)] = c
            if (str(tds[9].text) != '-' and
                str(tds[10].text) != '-'):
                vente = float(tds[9].text)
                achat = float(tds[10].text)
                p = Option('Put', strike=strike, achat=achat, vente=vente, multiplier=multiplier)
                self.put[float(p.strike)] = p
        return (self.call, self.put)
