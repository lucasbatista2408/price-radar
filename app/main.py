import threading

from fastapi import FastAPI

from app.routers.product_router import router as product_router
from app.scheduler.scheduler import run_scheduler


app = FastAPI()


app.include_router(product_router)


scheduler_thread = threading.Thread(
    target=run_scheduler,
    daemon=True
)

scheduler_thread.start()


@app.get("/")
def root():
    return {"message": "Price Radar API is running"}