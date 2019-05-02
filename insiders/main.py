
from tests import test_insiders
from src import insiders, lite_tools
import unittest


def print_generator(gene):
    """Print generator line by line"""
    for item in gene:
        print(list(item))
    return 'Done'


def run_tests(test_dir='tests/'):
    """Run tests from tests directory"""
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    # run unittest
    # run_tests()

    insider = insiders.InsiderScraper(sells=False)
    max_pages = insider.get_max_pages()
    print('Max pages are :', max_pages)

    lt = lite_tools.IntoLite()
    lt.execute_sql_str("DROP TABLE IF EXISTS symbols")
    lt.execute_sql_str("DROP TABLE IF EXISTS insiders")
    # a = insider.get_page(3)
    # print(a)

    print('deleted')
    lt.create_symbols_table()
    lt.create_insiders_table()
    i = 0
    for gen in insider.iterate_pages(max_pages):
        print('number: ', i, ' - ', gen)
        if i >= 715:
            for item in gen:

                symbol, company, country = item['Symbol'], item['Company'], item['Country']
                values = (symbol, company, country)
                # print(values)
                lt.execute_insert('symbols', values)
                insiders_data = (symbol, item['Insider'], item['Position'],
                                 item['Date'], item['Buy/Sell'], item['Shares'],
                                 item['Shares Change (%)'], item['Trade Price ($)'], item['Cost (1000$)'],
                                 item['Shares']*item['Trade Price ($)'],
                                 item['Yield (%)'], item['P/E'], item['Market Cap ($M)'])
                # print(insiders_data)
                lt.execute_insert('insiders', insiders_data)
        else:
            pass
        i += 1
    # print(lt.execute_sql_str('SELECT * FROM symbols', return_obj=True).fetchall())
    # print('Iterating pages:')
    # gene = insider.iterate_pages(2)
    # for i, item in enumerate(gene):
    #     print(i, ' --- ', item)
    #     for ite in item:
    #         print(ite)


if __name__ == '__main__':
    main()
