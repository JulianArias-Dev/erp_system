from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller import product_controller, ingredient_controller, recipe_controller

app = FastAPI()

# Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_controller.router)
app.include_router(ingredient_controller.router)
app.include_router(recipe_controller.router)
