from playwright.sync_api import sync_playwright
from app.utils import get_price


def amazon_scraper(product):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()
            page.goto(product.url)

            price = page.locator(".priceToPay")
            title = page.locator("#productTitle")
            image = page.locator("#landingImage")

            if price.count() > 0:
                price_value = get_price(price)
                title_value = title.inner_text()

                if image.count() > 0:
                    image_url = image.get_attribute("data-old-hires")
                else:
                    image_url = None

                product.name = title_value
                product.price = price_value

                # Ainda não temos image_url no model.
                # product.image_url = image_url

                browser.close()

                return product

            browser.close()

    except Exception as e:
        print(f"Error trying to get the product information: {e}")
        return None