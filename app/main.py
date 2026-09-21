import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.product_router import router as product_router
from app.scheduler.scheduler import run_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia o scheduler em segundo plano assim que a API sobe
    scheduler_thread = threading.Thread(
        target=run_scheduler,
        daemon=True
    )
    scheduler_thread.start()
    
    yield  # A aplicação FastAPI fica ativa e rodando
    
    # Trecho executado no encerramento (shutdown) da aplicação, se necessário


app = FastAPI(
    title="PriceRadar API",
    description="API para monitoramento de preços em marketplaces",
    version="1.0.0",
    lifespan=lifespan
)

# Registra as rotas da aplicação
app.include_router(product_router)


@app.get("/")
def root():
    return {"message": "Price Radar API is running"}