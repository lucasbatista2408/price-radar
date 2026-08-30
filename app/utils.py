import re


def get_price(price):
    whole = price.locator(".a-price-whole").inner_text()
    fraction = price.locator(".a-price-fraction").inner_text()

    whole = whole.replace(",", "").replace(".", "").strip()
    fraction = fraction.strip()

    return float(f"{whole}.{fraction}")


def extract_asin(url, page=None):
    """
    Attempts to extract an Amazon ASIN from the URL.
    If the ASIN cannot be found in the URL, optionally
    uses an already opened Playwright page as fallback.
    """

    url_patterns = [
        r"/dp/([A-Z0-9]{10})(?:[/?]|$)",
        r"/gp/product/([A-Z0-9]{10})(?:[/?]|$)",
        r"/gp/aw/d/([A-Z0-9]{10})(?:[/?]|$)",
    ]

    for pattern in url_patterns:
        match = re.search(pattern, url, re.IGNORECASE)

        if match:
            return match.group(1).upper()

    if page is not None:
        asin = extract_asin_from_page(page)

        if asin:
            return asin

    return None


def extract_asin_from_page(page):
    
    #Attempts to extract the ASIN from the already loaded Amazon page.

    selectors = [
        "#ASIN",
        "input[name='ASIN']",
        "[data-asin]",
    ]

    for selector in selectors:
        elements = page.locator(selector)

        for i in range(elements.count()):
            element = elements.nth(i)

            asin = (
                element.get_attribute("value")
                or element.get_attribute("data-asin")
            )

            if is_valid_asin(asin):
                return asin.upper()

    return None


def is_valid_asin(value):
    if not value:
        return False

    return bool(
        re.fullmatch(
            r"[A-Z0-9]{10}",
            value,
            re.IGNORECASE
        )
    )