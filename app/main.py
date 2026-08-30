from fastapi import FastAPI, HTTPException

from app.schemas import ProductRequest
from app.services.product_service import add_product
from app.exceptions import (
    ProductScrapingError,
    ProductAlreadyExistsError
)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Price Radar API is running"}


@app.post("/products")
def create_product(product_request: ProductRequest):
    try:
        product = add_product(
            product_request.url,
            product_request.target_price
        )

        return {
            "id": product.id,
            "name": product.name,
            "url": product.url,
            "price": product.price,
            "target_price": product.target_price,
            "image_url": product.image_url
        }

    except ProductAlreadyExistsError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    except ProductScrapingError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )