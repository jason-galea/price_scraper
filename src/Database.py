from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime

from src.generic_funcs import get_iso_8601_time


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Product(db.Model):
    """
    Parent class for other product tables.\n
    Defines common database fields & functions.
    """

    __tablename__ = "product"

    id: Mapped[int]             = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str]           = mapped_column(String) ### Allow inheritance

    UTCTime: Mapped[DateTime]   = mapped_column(DateTime)
    Retailer: Mapped[str]       = mapped_column(String)
    Title: Mapped[str]          = mapped_column(String)
    URL: Mapped[str]            = mapped_column(String)
    PriceAUD: Mapped[float]     = mapped_column(Float)
    Brand: Mapped[str]          = mapped_column(String)

    __table_args__ = (
        db.CheckConstraint(
            Retailer.in_(['pccg', 'scorptec', 'centrecom']),
            name='Retailer_types'
        ),
    )

    ### Allow inheritance
    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": "type",
    }


    # def __init__(self):
    #     raise NotImplementedError


    def __repr__(self):
        return f"{self.__class__.__name__}({self.Title!r})"


    @classmethod
    def get_most_recent(cls, retailer) -> list:
        """
        Each "batch" of products in the table shares a UTC timestamp.\n
        This can be used to only fetch products from the latest batch.\n
        Returns a list of dictionaries.
        """

        latest_product = cls.query.order_by(cls.id.desc()).first()

        if not latest_product:
            return

        products_list_of_tuples = (
            cls.query.filter(
                cls.Retailer == retailer,
                cls.UTCTime == latest_product.UTCTime,
            )
            .order_by(cls.id.desc())
            .all()
        )

        result = []
        for p in products_list_of_tuples:
            p_converted: dict = p.__dict__
            del p_converted["_sa_instance_state"]
            p_converted["UTCTime"] = get_iso_8601_time(p_converted["UTCTime"])

            result.append(p_converted)

        return result


    @classmethod
    def export_to_db(cls, products: list) -> None:
        """Export products (a list of dictionaries) to PostgreSQL DB"""
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

        for product in products:
            db.session.add(cls(**product)) ### Add to DB queue

        db.session.commit() ### Flush DB queue
        print("==> INFO: Successfully flushed DB queue")


class Drive(Product): # pylint: disable=abstract-method
    """Parent Model for drives, or products that have some capacity"""

    CapacityTB: Mapped[float]   = mapped_column(Float, nullable=True)
    CapacityGB: Mapped[float]   = mapped_column(Float, nullable=True)
    PricePerTB: Mapped[float]   = mapped_column(Float, nullable=True)
    PricePerGB: Mapped[float]   = mapped_column(Float, nullable=True)

    ### Allow nested inheritance
    __mapper_args__ = { "polymorphic_abstract": True }


@dataclass
class SSD(Drive):
    """Model for SSDs"""

    __tablename__ = "ssd"

    FormFactor: Mapped[str]     = mapped_column(String, nullable=True)
    Protocol: Mapped[str]       = mapped_column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "ssd",
    }


@dataclass
class HDD(Drive):
    """Model for HDDs"""

    __tablename__ = "hdd"

    Series: Mapped[str]         = mapped_column(String, nullable=True)
    Model: Mapped[str]          = mapped_column(String, nullable=True)

    __mapper_args__ = { "polymorphic_identity": "hdd" }


CATEGORY_CLASS_DICT = {
    "ssd":      SSD,
    "hdd":      HDD,
    # "ddr4":     RAM,
    # "ddr5":     RAM,
}
