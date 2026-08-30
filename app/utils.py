def get_price (price):
    price_text = price.first.inner_text()

    price_text = price_text.replace("R$", "")
    price_text = price_text.replace("\n", "")
    price_text = price_text.replace(",", ".")

    return float(price_text)