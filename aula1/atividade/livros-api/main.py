from fastapi import FastAPI

import models  # noqa: F401  (garante o registro da tabela no metadata)
from database import Base, engine
from router import router

# Cria as tabelas no SQLite (arquivo livros.db) se ainda não existirem.
# Os dados NÃO são apagados ao reiniciar a API.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Livros API", version="1.0.0")
app.include_router(router)


@app.get("/", tags=["Root"])
def raiz():
    return {"mensagem": "Livros API no ar. Acesse /docs para o Swagger."}
