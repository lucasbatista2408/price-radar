class Product:
    def __init__(self, url, target_price, name = None, price=None, id=None, image_url=None):
        self.id = id
        self.name = name
        self.url = url
        self.target_price = target_price
        self.price = price
        self.image_url = image_url