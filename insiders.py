import requests
import time
from lxml import html



class Insiders:



    def __init__(self, sells=True, get_all = True):
        self.url = 'https://www.gurufocus.com/modules/insiders/InsiderBuy_ajax.php?'
        self.sells = sells
        self.get_all = get_all

        if self.sells:
            self.url = self.url + '&type=S'

        if self.get_all:
            self.iterate_pages()
        else:
            self.get_page()

    def iterate_pages(self):
        n = 0
        limit = self.get_max_pages()
        for n in range(0,limit)[0:1]:
            # print(self.url)
            to_visit = self.url+ f'&p={n}&n=100'

            self.get_page(to_visit)
            time.sleep(3)

    def get_max_pages(self):
        page = html.fromstring(requests.get(self.url).content)
        n_str = page.xpath('//a[contains(text(), "LAST")]/text()')[0]
        return int(n_str[n_str.find("(")+1:n_str.find(")")])

    def get_page(self, to_visit=None):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        if to_visit:
            url = 'https://www.gurufocus.com/modules/insiders/InsiderBuy_ajax.php?p=7&n=100'
            page = html.fromstring(requests.get(to_visit,
                                                headers={'User-Agent': user_agent}).content)
        else:
            page = html.fromstring(requests.get(self.url).content)
        table = page.xpath('//table[@class="fixed_headers R5"]/tr')

        for tr in table[0:1]:
            country = tr.xpath('.//td/img/@src')[0].split('/')[-1].strip('.png')
            symbol, insider = tr.xpath('.//td[@class="text"]/a/text()')
            company, position = tr.xpath('.//td/@title')

            date = tr.xpath('.//td[@class="micro"]/text()')[0]
            other_tds = tr.xpath('.//td[@class="micro"]/following-sibling::td/text()')
            if self.sells:
                buy_sell = 'Sell'
                rest_of_data = self.get_sells_tds(other_tds)
            else:
                buy_sell = 'Buy'
                rest_of_data = self.get_buys_tds(other_tds)

            my_obj = {
                "Country": country,
                "Symbol": symbol,
                "Insider": insider,
                "Company": company,
                "Position": position,
                "Date": date,
                "Buy/Sell":buy_sell
            }
            my_obj.update(rest_of_data)
            print(my_obj)


    def get_buys_tds(self,other_tds):
        shares = int(other_tds[0].replace(',', ''))
        shares_change = float(other_tds[1].strip('%'))
        trade_price = float(other_tds[2].strip('$'))
        cost = float(other_tds[3])
        yield_pcte = float(other_tds[4])
        p_e = float(other_tds[5])
        market_cap = float(other_tds[6])

        return {
            "Shares":shares,
            "Shares Change (%)":shares_change,
            "Trade Price ($)":trade_price,
            "Cost (1000$)":cost,
            "Yield (%)":yield_pcte,
            "P/E":p_e,
            "Market Cap ($M)":market_cap
        }

    def get_sells_tds(self,other_tds):
        shares = int(other_tds[1].replace(',', ''))
        shares_change = float(other_tds[2].strip('%'))
        trade_price = float(other_tds[3].strip('$'))
        cost = float(other_tds[4])
        yield_pcte = float(other_tds[5])
        p_e = float(other_tds[6])
        market_cap = float(other_tds[7])

        return {
            "Shares":shares,
            "Shares Change (%)":shares_change,
            "Trade Price ($)":trade_price,
            "Cost (1000$)":cost,
            "Yield (%)":yield_pcte,
            "P/E":p_e,
            "Market Cap ($M)":market_cap
        }

def main():
    Insiders(sells=False)
    Insiders(sells=True)


if __name__ == '__main__':
    main()
