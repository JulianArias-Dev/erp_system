from fastapi import FastAPI
from routes.supplier import supplier

app = FastAPI()

app.include_router(supplier)
