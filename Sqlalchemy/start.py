from Sqlalchemy.CRUD import products_crud, locations_crud
from Sqlalchemy.Db.db import get_db
from Sqlalchemy.Models.products import Products
from Sqlalchemy.Models.locations import Locations
from datetime import datetime
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


def create_location(id:int, product_id:int, add_date:str, mark_num:int, shelf:int):

    add_date = datetime.strptime(add_date, '%Y-%m-%dT%H:%M:%S')

    locations = Locations()

    locations.id = id
    locations.product_id = product_id
    locations.add_date = add_date
    locations.mark_num = mark_num
    locations.shelf = shelf

    db = get_db()
    return locations_crud.create_location(db, locations)


try:
    create_product(1, 'молоко')
    create_product(2, 'огурцы')
    get_products_all()

    create_location(1, 1, '2024-10-11T20:30:11', 4, 8)
except Exception as e:
    print(e)


