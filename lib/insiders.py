import requests
import time
from lxml import html


class InsiderScraper:
    start_url = ['https://www.gurufocus.com/modules/insiders/InsiderBuy_ajax.php?']  # noqa
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    def __init__(self, sells=False):
        """Initialization of InsidersScraper

        Args:
            sells: bool. Get buyer data or seller data.
        """
        self.url = InsiderScraper.start_url[0]
        self.sells = sells

        if self.sells:
            self.url = self.url + '&type=S'

    def __repr__(self):
        """Object representation"""
        return f'InisderScraper(url:{self.url}, sells={self.sells})'

    def iterate_pages(self, n=0):
        """Iterates n pages and formats the url.

        Args:
            n = int. Default 0.

        Returns:
            link : str
        """
        if not n:
            n = 1
        elif isinstance(n, int):
            pass
        else:
            raise ValueError

        for n in range(0, n):
            yield self.get_page(page_url=self.format_url(n))
            time.sleep(3)

    def format_url(self, n):
        return self.url + f'&p={n}&n=100'

    def get_max_pages(self):
        """Get max pages"""
        page = html.fromstring(requests.get(self.url).content)
        n_str = page.xpath('//a[contains(text(), "LAST")]/text()')[0]
        return int(n_str[n_str.find("(")+1:n_str.find(")")])

    def get_page(self, page_url=None, n=0):
        """Get page data

        Args:
            page_url: str, default None. (It will use start_url)

        Returns:
            json object with data.
        """
        headers = {'User-Agent': InsiderScraper.user_agent}
        try:
            if page_url:
                page = html.fromstring(requests.get(page_url,
                                                    headers=headers).content)
            elif n:
                page = html.fromstring(requests.get(self.format_url(n),
                                                    headers=headers).content)
            else:
                page = html.fromstring(requests.get(self.url,
                                                    headers=headers).content)
        except Exception:
            raise Exception
        table = page.xpath('//table[@class="fixed_headers R5"]/tr')

        for tr in table[0:]:
            country = tr.xpath(
                './/td/img/@src')[0].split('/')[-1].strip('.png')
            symbol, insider = tr.xpath('.//td[@class="text"]/a/text()')
            company, position = tr.xpath('.//td/@title')

            date = tr.xpath('.//td[@class="micro"]/text()')[0]
            self.other_tds = tr.xpath(
                './/td[@class="micro"]/following-sibling::td/text()')
            if self.sells:
                buy_sell = 'Sell'
                rest_of_data = self.get_sells_tds()
            else:
                buy_sell = 'Buy'
                rest_of_data = self.get_buys_tds()

            my_obj = {
                "Country": country,
                "Symbol": symbol,
                "Insider": insider,
                "Company": company,
                "Position": position,
                "Date": date,
                "Buy/Sell": buy_sell
            }
            my_obj.update(rest_of_data)
            yield my_obj

    def get_buys_tds(self):
        """Insider method to get the rest of the data from tds"""
        shares = int(self.other_tds[0].replace(',', ''))
        shares_change = float(self.other_tds[1].strip('%'))
        trade_price = float(self.other_tds[2].strip('$'))
        cost = float(self.other_tds[3])
        yield_pcte = float(self.other_tds[4])
        p_e = float(self.other_tds[5])
        market_cap = float(self.other_tds[6])

        return {
            "Shares": shares,
            "Shares Change (%)": shares_change,
            "Trade Price ($)": trade_price,
            "Cost (1000$)": cost,
            "Yield (%)": yield_pcte,
            "P/E": p_e,
            "Market Cap ($M)": market_cap
        }

    def get_sells_tds(self):
        """Insider method to get the rest of the data from tds"""
        shares = int(self.other_tds[1].replace(',', ''))
        shares_change = float(self.other_tds[2].strip('%'))
        trade_price = float(self.other_tds[3].strip('$'))
        cost = float(self.other_tds[4])
        yield_pcte = float(self.other_tds[5])
        p_e = float(self.other_tds[6])
        market_cap = float(self.other_tds[7])

        return {
            "Shares": shares,
            "Shares Change (%)": shares_change,
            "Trade Price ($)": trade_price,
            "Cost (1000$)": cost,
            "Yield (%)": yield_pcte,
            "P/E": p_e,
            "Market Cap ($M)": market_cap
        }


def print_generator(gene):
    for item in gene:
        print(list(item))
    return 'Done'


def main():
    insider = InsiderScraper()
    print(insider.__repr__)
    max_pages = insider.get_max_pages()
    print('Max pages are :', max_pages)
    page_2 = insider.get_page(n=2)
    print('Page 2:')
    print(list(page_2))

    print('Iterating pages:')
    gene = insider.iterate_pages(3)
    print(gene)
    print_generator(gene)


if __name__ == '__main__':
    main()
