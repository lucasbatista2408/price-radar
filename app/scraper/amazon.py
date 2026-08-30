from playwright.sync_api import sync_playwright
from app.utils import get_price


def amazon_scraper(product):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()
            page.goto(product.url)

            price = page.locator(".priceToPay")

            title = page.locator("#productTitle").inner_text()

            if price.count() > 0:
                price_value = get_price(price)

                product.name = title
                product.price = price_value

                browser.close()

                return product

            browser.close()

    except Exception as e:
        print(f"Error trying to get the product information: {e}")
        return None