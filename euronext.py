import requests
from bs4 import BeautifulSoup

from product import Option


class Page:
    def __init__(self, site=None, ticker_idx=0, params=None):
        self.tickers = ['PXA-DPAR', '4PX-DPAR', '2PX-DPAR', '1PX-DPAR', '5PX-DPAR']
        # liste des options euronext CAC40 :
        # https://derivatives.euronext.com/en/equity-index-derivatives/contract-list?quicktabs_309=4#quicktabs-309
        self.site = "https://derivatives.euronext.com/fr/products/index-options" if not site else site
        self.ticker = self.tickers[ticker_idx]
        self.params = "Class_type=0&Class_symbol=&Class_exchange=&ex=&ps=999&md=11-2018" if not params else params

    def fetch(self):
        requete = requests.get("{}/{}?{}".format(self.site, self.ticker, self.params))
        page = requete.content
        self.soup = BeautifulSoup(page, features="html.parser")
        self.page_title = self.soup.find("h1", {"class": "title"}).text
        self.call = {}
        self.put = {}
        return self.soup

    def scrap_options(self):
        div = self.soup.find("div", {"class": "call-put-table"})
        trs = div.find_all("tr")
        elmts = {}
        self.call = {}
        self.put = {}
        self.data = []
        for tr in trs[3:-1]:
            tds = tr.find_all('td')
            self.data.append([td.text for td in tds])
            if (str(tds[4].text) != '-' and
                str(tds[5].text) != '-' and
                str(tds[9].text) != '-' and
                str(tds[10].text) != '-') :
                strike = float(tds[7].text)
                achat = float(tds[4].text)
                vente = float(tds[5].text)
                c = Option('Call', strike=strike, achat=achat, vente=vente)
                achat = float(tds[9].text)
                vente = float(tds[10].text)
                p = Option('Put', strike=strike, achat=achat, vente=vente)
                elmts[float(c.strike)] = {'call': c, 'put': p}
                self.call[float(c.strike)] = c
                self.put[float(p.strike)] = p
        return elmts
