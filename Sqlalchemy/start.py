from Sqlalchemy.CRUD import products_crud
from Sqlalchemy.Db.db import get_db
from Sqlalchemy.Models.products import Products
import sqlite3


def create_product(id:int, name:str):
    products = Products()
    products.id = id
    products.name = name

    db = get_db()

    return products_crud.create_product(db, products)

def get_products_all():
    db = get_db()
    products = products_crud.get_products_all(db)
    for product in products:
        print(product.id, '|', product.name)



try:
    create_product(1, 'молоко')
    create_product(2, 'огурцы')
    get_products_all()
except Exception as e:
    print(e)


