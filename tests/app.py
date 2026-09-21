from tests.manual.add_product_test import add_product_test
from tests.manual.check_products_test import check_products_test
from tests.manual.asin_test import asin_test


def app():
    print("Running tests...")
    asin_test()
    #add_product_test()
    #check_products_test()

if __name__ == "__main__":
    app()