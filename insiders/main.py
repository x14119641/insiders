
from tests import test_insiders
from src import insiders, lite_tools
import unittest


def print_generator(gene):
    for item in gene:
        print(list(item))
    return 'Done'


def main():
    # run unittest
    loader = unittest.TestLoader()
    suite = loader.discover('tests/')
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # test_insiders.unittest.main()
    # insider = insiders.InsiderScraper(sells=False)
    # print(insider.__repr__)
    # print(insider.__str__)
    # max_pages = insider.get_max_pages()
    # print('Max pages are :', max_pages)
    # page_2 = insider.get_page(n=1)
    # print('Page 2:')
    # # print(list(page_2))
    # for item in page_2:
    #     print(item)
    #     symbol, company, country = item['Symbol'], item['Company'], item['Country']
    #     print(symbol, company, country)
    #     lt = lite_tools.IntoLite()
    #     print(lt)
    #     values = (symbol, company, country)
    #     print(lt.execute_sql_str('SELECT * FROM symbols', return_obj=True).fetchall())

    # lt.execute_insert('symbols', values)

    # print('Iterating pages:')
    # gene = insider.iterate_pages(2)
    # print(gene)
    # print_generator(gene)


if __name__ == '__main__':
    main()
