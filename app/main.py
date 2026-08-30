from fastapi import FastAPI, HTTPException

from app.schemas import ProductRequest

from app.services.product_service import (
    add_product,
    get_product
)

from app.database import get_products as get_products_from_database

from app.exceptions import (
    ProductScrapingError,
    ProductAlreadyExistsError,
    ProductNotFoundError
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
            "image_url": product.image_url,
            "asin": product.asin
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


@app.get("/products")
def get_products():
    products = get_products_from_database()

    return [
        {
            "id": product.id,
            "name": product.name,
            "url": product.url,
            "price": product.price,
            "target_price": product.target_price,
            "image_url": product.image_url,
            "asin": product.asin
        }
        for product in products
    ]


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    try:
        product = get_product(product_id)

        return {
            "id": product.id,
            "name": product.name,
            "url": product.url,
            "price": product.price,
            "target_price": product.target_price,
            "image_url": product.image_url,
            "asin": product.asin
        }

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )