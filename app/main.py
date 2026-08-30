from fastapi import FastAPI

from app.routers.product_router import router as product_router


app = FastAPI()


app.include_router(product_router)


@app.get("/")
def root():
    return {"message": "Price Radar API is running"}