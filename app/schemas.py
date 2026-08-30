from pydantic import BaseModel


class ProductRequest(BaseModel):
    url: str
    target_price: float