
from tests import test_insiders
from src import insiders


def print_generator(gene):
    for item in gene:
        print(list(item))
    return 'Done'


def main():
    # run unittest
    test_insiders.unittest.main()
    insider = insiders.InsiderScraper(sells=False)
    print(insider.__repr__)
    print(insider.__str__)
    max_pages = insider.get_max_pages()
    print('Max pages are :', max_pages)
    page_2 = insider.get_page(n=1)
    print('Page 2:')
    print(list(page_2))

    print('Iterating pages:')
    gene = insider.iterate_pages(2)
    print(gene)
    print_generator(gene)


if __name__ == '__main__':
    main()
