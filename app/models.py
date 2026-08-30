class Product:
    def __init__(self, name, url, target_price, price=None, id=None):
        self.id = id
        self.name = name
        self.url = url
        self.target_price = target_price
        self.price = price