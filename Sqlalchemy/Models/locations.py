from sqlalchemy import INTEGER, DATETIME, Column, ForeignKey
from Sqlalchemy.Db.db import Base
from Sqlalchemy.Models.products import Products
from sqlalchemy.orm import relationship

class Locations(Base):
    __tablename__ = 'locations'
    id = Column(INTEGER(), primary_key=True)
    product_id = Column(INTEGER(), ForeignKey('products.id'), primary_key=True, nullable=False)
    add_date = Column(DATETIME())
    mark_num = Column(INTEGER())
    shelf = Column(INTEGER())
    product = relationship(Products)

