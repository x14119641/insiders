import requests
from lxml import html



class Insiders:



    def __init__(self, sells=False, get_all = True):
        self.url = 'https://www.gurufocus.com/modules/insiders/InsiderBuy_ajax.php'
        if get_all:
            self.url = self.url + '?p=0&n=100'
        if sells:
            self.url = self.url + '&type=S'


    def get_page(self):

        doc = html.fromstring(requests.get(self.url).content)
        table = doc.xpath('//table[@class="fixed_headers R5"]/tr')

        for tr in table[0:1]:
            country = tr.xpath('.//td/img/@src')[0].split('/')[-1].strip('.png')
            symbol, insider = tr.xpath('.//td[@class="text"]/a/text()')
            company, position = tr.xpath('.//td/@title')

            date = tr.xpath('.//td[@class="micro"]/text()')[0]
            other_tds = tr.xpath('.//td[@class="micro"]/following-sibling::td/text()')
            shares = other_tds[0]
            shares_change = float(other_tds[1].strip('%'))
            trade_price = float(other_tds[2].strip('$'))
            cost = float(other_tds[3])
            yield_pcte = float(other_tds[4])
            p_e = float(other_tds[5])
            market_cap = float(other_tds[6])
            buy_sell, _= tr.xpath('.//td/font[@class="tkg"]/text()')


            my_obj = {
                "Country": country,
                "Symbol": symbol,
                "Insider": insider,
                "Company": company,
                "Position": position,
                "Date": date,
                "Shares":shares,
                "Shares Change (%)":shares_change,
                "Trade Price ($)":trade_price,
                "Cost (1000$)":cost,
                "Yield (%)":yield_pcte,
                "P/E":p_e,
                "Market Cap ($M)":market_cap,
                "Buy/Sell":buy_sell
            }
            print(my_obj)



if __name__ == '__main__':
    Insiders().get_page()
