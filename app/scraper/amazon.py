from playwright.sync_api import sync_playwright

from app.utils import get_price


def amazon_scraper(product):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(
                product.url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            prices = page.locator(".priceToPay")
            title = page.locator("#productTitle")
            image = page.locator("#landingImage")

            if prices.count() == 0:
                browser.close()
                return None

            price = prices.first

            price_value = get_price(price)
            title_value = title.inner_text()

            if image.count() > 0:
                product.image_url = image.get_attribute(
                    "data-old-hires"
                )
            else:
                product.image_url = None

            product.name = title_value
            product.price = price_value

            browser.close()

            return product

    except Exception as e:
        print(
            f"Error trying to get the product information: {e}"
        )
        return None

