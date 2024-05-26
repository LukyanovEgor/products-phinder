from sqlalchemy import INTEGER, TEXT, Column
from Sqlalchemy.Db.db import Base

class Products(Base):
    __tablename__ = 'products'
    id = Column(INTEGER(), primary_key=True)
    name = Column(TEXT(), nullable=False)


