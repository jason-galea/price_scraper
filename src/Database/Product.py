# from flask_sqlalchemy import select
# from flask_sqlalchemy.query import Query

from src.generic_funcs import convert_datetime_to_iso_8601
from src.Database.db import db

class Product(db.Model):
    __tablename__ = 'products'

    ### Schema
    ### NOTE: Any changes require "db" docker volume to be recreated
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title       = db.Column(db.String, unique=True, nullable=False)
    Title       = db.Column(db.String, nullable=False)
    Retailer    = db.Column(db.String, nullable=False)
    Category    = db.Column(db.String, nullable=False)
    UTCTime     = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        ### Only allow certain values for retailer
        db.CheckConstraint(
            Retailer.in_(['pccg', 'scorptec', 'centrecom']),
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
        self.Title = title
        self.Retailer = retailer
        self.Category = category
        self.UTCTime = utctime


    # def register_product_if_not_exist(self):
    #     db_product = Product.query.filter(Product.title == self.Title).all()

    #     if not db_product:
    #         db.session.add(self)
    #         db.session.commit()

    #     return True


    @staticmethod
    def get_most_recent(retailer, category) -> list:
        """
        Each "batch" of products in the table shares a UTC timestamp.\n
        This can be used to only fetch products from the latest batch.\n
        Returns a list of dictionaries.
        """
        latest_utctime = Product.query.order_by(Product.id.desc()).first().utctime

        products_list_of_tuples = Product.query.filter(
            Product.Retailer == retailer,
            Product.Category == category,
            Product.UTCTime == latest_utctime,
        ).order_by(Product.id.desc()).all() ### Convert to list of KeyedTuples

        result = []
        for p in products_list_of_tuples:
            p_converted: dict = p.__dict__
            del p_converted["_sa_instance_state"]
            p_converted["utctime"] = convert_datetime_to_iso_8601(p_converted["utctime"])

            result.append(p_converted)

        return result


    def __repr__(self):
        return f"<Product {self.Title}>"
