from fastapi import FastAPI
from routers.producao import router as producao_router
from routers.processamento import router as processamento_router
from routers.comercializacao import router as comercializacao_router
from routers.importacao import router as importacao_router
from routers.exportacao import router as exportacao_router

app = FastAPI()

app.include_router(producao_router, prefix="/producao", tags=["Produção"])
app.include_router(
    processamento_router, prefix="/processamento", tags=["Processamento"]
)
app.include_router(
    comercializacao_router, prefix="/comercializacao", tags=["Comercialização"]
)
app.include_router(importacao_router, prefix="/importacao", tags=["Importação"])
app.include_router(exportacao_router, prefix="/exportacao", tags=["Exportação"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
