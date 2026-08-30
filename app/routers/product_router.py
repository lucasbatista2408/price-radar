from fastapi import APIRouter, HTTPException

from app.schemas import ProductRequest

from app.services.product_service import (
    add_product,
    get_product
)

from app.services.price_service import (
    check_all_products,
    get_product_price_history
)

from app.database import get_products as get_products_from_database

from app.exceptions import (
    ProductScrapingError,
    ProductAlreadyExistsError,
    ProductNotFoundError
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("")
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


@router.get("")
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


@router.get("/{product_id}")
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


@router.post("/check-price")
def check_prices():
    results = check_all_products()

    return [
        {
            "id": result["product"].id,
            "name": result["product"].name,
            "price": result["price"],
            "target_price": result["product"].target_price,
            "target_reached": result["target_reached"],
            "error": result["error"]
        }
        for result in results
    ]

@router.get("/{product_id}/price-history")
def get_price_history(product_id: int):
    history = get_product_price_history(product_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return {
        "id": history[0][0],
        "name": history[0][1],
        "image_url": history[0][2],
        "history": [
            {
                "price": row[3],
                "checked_at": row[4]
            }
            for row in history
            if row[3] is not None
        ]
    }