from sqlalchemy.orm import Session
from Sqlalchemy.Models.products import Products

def create_product(db: Session, product: Products):

    """
    Create a new product in database
    :param db: session for the database
    :param product: model table of product
    :return: True if the product was created, False if not
    """
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except Exception as e:
        print(e)
        return False
    return True

def get_products_all(db: Session):
    """
    Get all products from the database
    :param db: session for the database
    :return: list of products
    """
    return db.query(Products).all()

def get_product_by_id(db: Session, id: int):

    """
    Get product from database
    :param db: session for the database
    :param id: id of the product
    :return: dta of product if it exists, none if not
    """
    if product := db.query(Products).filter(Products.id == id).first():
        return product
    return None


def update_product(db: Session, id: int, product: Products):
    """
    Update a product in the database
    :param db: session for the database
    :param id: id of the product
    :param product: model table of the product
    :return: True if the product was updated, False if not
    """
    if get_product_by_id(db, id):
        try:
            db.query(Products).filter(Products.id == id).update({"name": product.name})
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    return False

def delete_product(db: Session, id: int):
    """
    Delete a product from the database
    :param db: session for the database
    :param id: id of the product
    :return: True if the product was deleted, False if not
    """
    if get_product_by_id(db, id):
        try:
            db.query(Products).filter(Products.id == id).delete()
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    return False