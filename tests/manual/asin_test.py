from app.utils import extract_asin


def asin_test():
    url_1 = "https://www.amazon.com.br/gp/product/8568224067?smid=A1ZZFT5FULY4LN&psc=1"

    url_2 = "https://www.amazon.com.br/dp/8568224067/?bestFormat=true&k=cinco%20li%C3%A7%C3%B5es%20de%20psican%C3%A1lise&crid=13V5XX8P3NXFJ&sprefix=cinco%20li"

    asin_1 = extract_asin(url_1)
    asin_2 = extract_asin(url_2)

    result = asin_1 is not None and asin_1 == asin_2

    print(result)

if __name__ == "__main__":
    asin_test()