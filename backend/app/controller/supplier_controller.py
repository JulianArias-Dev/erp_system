from fastapi import APIRouter
from config.db import conn

supplier = APIRouter()

@supplier.get('/suppliers')
def find_all_suppliers ():
    return "Hello"

@supplier.get('/suppliers/{id}')
def find_supplier ():
    return "Hello"

@supplier.post('/suppliers')
def createSupplier ():
    return "Hello"

@supplier.put('/suppliers/{id}')
def update_supplier ():
    return "Hello"

@supplier.delete('/suppliers/{id}')
def delete_supplier ():
    return "Hello"