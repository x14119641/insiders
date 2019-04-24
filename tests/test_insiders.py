from bin import insiders
import unittest
import inspect


class InsiderTest(unittest.TestCase):
    def setUp(self):
        self.insiders_buying = insiders.InsiderScraper()
        self.insiders_selling = insiders.InsiderScraper(sells=True)
        self.pages_buying = self.insiders_buying.get_max_pages()
        self.pages_selling = self.insiders_buying.get_max_pages()

    def test_get_max_pages(self):
        self.assertIsInstance(self.pages_buying,
                              int)
        self.assertIsInstance(self.pages_selling,
                              int)

    def test_iterate_pages(self):
        self.assertTrue(
            inspect.isgenerator(self.insiders_buying.iterate_pages(2)))
        self.assertTrue(
            inspect.isgenerator(self.insiders_selling.iterate_pages(3)))

        with self.assertRaises(ValueError):
            list(self.insiders_selling.iterate_pages([1, 2]))
            list(self.insiders_buying.iterate_pages('as'))
            list(self.insiders_buying.iterate_pages({1: 'as'}))

    def test_format_utl(self, n=3):
        self.assertEqual(self.insiders_selling.url + f'&p={n}&n=100',
                         self.insiders_buying.url +
                         '&type=S' + f'&p={n}&n=100')

    def test_get_page(self):
        buying_page = self.insiders_buying.get_page(n=1)

        selling_page = self.insiders_selling.get_page(n=3)
        len_buying = sum(1 for x in buying_page)
        len_selling = sum(1 for x in selling_page)
        self.assertTrue(
            inspect.isgenerator(buying_page))
        self.assertIsInstance(list(buying_page), list)
        self.assertEqual(len_buying, 100)
        self.assertTrue(
            inspect.isgenerator(selling_page))
        self.assertIsInstance(list(selling_page), list)
        self.assertEqual(len_selling, 100)

    def test_get_sells_tds(self):
        self.insiders_buying.other_tds = ['90,500', '100%',
                                          '$0.07', '6.34', '0.00',
                                          '0.00', '4.687', '\xa0']
        self.insiders_selling.other_tds = ['Sell', '11,407', '3.76%',
                                           '$192.95', '2200.98', '0.00',
                                           '0.00', '42040.140', '\xa0']

        buying_result = {'Shares': 90500, 'Shares Change (%)': 100.0, 'Trade Price ($)': 0.07,  # noqa
                         'Cost (1000$)': 6.34, 'Yield (%)': 0.0, 'P/E': 0.0, 'Market Cap ($M)': 4.687}  # noqa
        selling_result = {'Shares': 11407, 'Shares Change (%)': 3.76, 'Trade Price ($)': 192.95,  # noqa
                          'Cost (1000$)': 2200.98, 'Yield (%)': 0.0, 'P/E': 0.0, 'Market Cap ($M)': 42040.14}  # noqa
        buying_row = self.insiders_buying.get_buys_tds()
        selling_row = self.insiders_selling.get_sells_tds()

        self.assertIsInstance(buying_row, dict)
        self.assertEqual(buying_result, buying_row)
        self.assertIsInstance(selling_row, dict)
        self.assertEqual(selling_result, selling_row)


if __name__ == '__main__':
    unittest.main()
