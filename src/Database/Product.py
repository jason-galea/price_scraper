# from sqlalchemy import Integer, String, DateTime
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy.query import Query

from src.Database.db import db

class Product(db.Model):
    __tablename__ = 'products'

    ### Schema
    ### NOTE: Any changes require "db" docker volume to be recreated
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title       = db.Column(db.String, unique=True, nullable=False)
    title       = db.Column(db.String, nullable=False)
    retailer    = db.Column(db.String, nullable=False)
    category    = db.Column(db.String, nullable=False)
    utctime     = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        ### Only allow certain values for retailer
        db.CheckConstraint(
            retailer.in_(['PCCG', 'Scorptec', 'CentreCom']),
            name='retailer_types'
        ),
    )


    def __init__(
        self,
        title,
        retailer,
        category,
        utctime,
    ):
        self.title = title
        self.retailer = retailer
        self.category = category
        self.utctime = utctime


    # def register_product_if_not_exist(self):
    #     db_product = Product.query.filter(Product.title == self.title).all()

    #     if not db_product:
    #         db.session.add(self)
    #         db.session.commit()

    #     return True


    # def get_by_title(title) -> Query:
    #     return Product.query.filter(Product.title == title).first()


    def get_most_recent(retailer, category) -> Query:
        return Product.query.filter(
            Product.retailer == retailer,
            Product.category == category,
        ).all()


    def __repr__(self):
        return f"<Product {self.title}>"
