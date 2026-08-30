def get_price(price): 
    whole = price.locator(".a-price-whole").inner_text() 
    fraction = price.locator(".a-price-fraction").inner_text()

    whole = whole.replace(",", "").replace(".", "").strip() 
    fraction = fraction.strip()

    return float(f"{whole}.{fraction}")