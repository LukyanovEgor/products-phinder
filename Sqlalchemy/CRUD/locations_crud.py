from sqlalchemy.orm import Session
from Sqlalchemy.Models.locations import Locations

def create_location(db: Session, locations: Locations):

    """
    Create a new product in database
    :param db: session for the database
    :param locations: model table of location
    :return: True if the product was created, False if not
    """
    try:
        db.add(locations)
        db.commit()
        db.refresh(locations)
    except Exception as e:
        print(e)
        return False
    return True

def get_locations_all(db: Session):
    """
    Get all locations from the database
    :param db: session for the database
    :return: list of locations
    """
    return db.query(Locations).all()

def get_location_by_id(db: Session, id: int):

    """
    Get location from database
    :param db: session for the database
    :param id: id of the location
    :return: data of location if it exists, none if not
    """
    if location := db.query(Locations).filter(Locations.id == id).first():
        return location
    return None

def get_location_by_product_id(db: Session, product_id:int):

    """

    :param db: session for the database
    :param product_id: id of the product
    :return: data of location if it exists, none if not
    """
    if location := db.query(Locations).filter(Locations.product_id == product_id).first():
        return location
    return None

def update_location(db: Session, id: int, locations: Locations):
    """
    Update a location in the database
    :param db: session for the database
    :param id: id of the location
    :param locations: model table of the locations
    :return: True if the location was updated, False if not
    """
    if get_location_by_id(db, id):
        try:
            db.query(Locations).filter(Locations.id == id).update({"product_id": locations.product_id,
                                                                   "add_date": locations.add_date,
                                                                   "mark_num": locations.mark_num,
                                                                   "shelf": locations.shelf})
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    return False

def delete_location(db: Session, id: int):
    """
    Delete a location from the database
    :param db: session for the database
    :param id: id of the location
    :return: True if the location was deleted, False if not
    """
    if get_location_by_id(db, id):
        try:
            db.query(Locations).filter(Locations.id == id).delete()
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    return False
