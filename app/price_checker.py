def check_price(product):
    if product.price <= product.target_price:
        return "low"

    return "high"