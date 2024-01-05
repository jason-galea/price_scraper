from datetime import datetime
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

    UTCTime: Mapped[datetime]   = mapped_column(DateTime)
    Retailer: Mapped[str]       = mapped_column(String)
    Title: Mapped[str]          = mapped_column(String)
    URL: Mapped[str]            = mapped_column(String)
    PriceAUD: Mapped[float]     = mapped_column(Float)
    Brand: Mapped[str]          = mapped_column(String)

    __table_args__ = (
        db.CheckConstraint(
            Retailer.in_(['pccg', 'scorptec', 'centrecom']),
            name='retailer_types'
        ),
    )

    ### Allow inheritance
    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": "type",
    }


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

    __tablename__ = "drive"

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

    # pylint: disable=invalid-name
    FormFactor: Mapped[str]     = mapped_column(String, nullable=True)
    Protocol: Mapped[str]       = mapped_column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "ssd",
    }


@dataclass
class HDD(Drive):
    """Model for HDDs"""

    __tablename__ = "hdd"

    # pylint: disable=invalid-name
    Series: Mapped[str]         = mapped_column(String, nullable=True)
    HDDModel: Mapped[str]       = mapped_column(String, nullable=True)

    __mapper_args__ = { "polymorphic_identity": "hdd" }


@dataclass
class RAM(Product):
    """Parent Model for RAM"""

    __tablename__ = "ram"

    # pylint: disable=invalid-name
    RAMModel: Mapped[str]           = mapped_column(String, nullable=True)
    RAMCapacityGB: Mapped[float]    = mapped_column(Float, nullable=True)
    KitConfiguration: Mapped[str]   = mapped_column(String, nullable=True)
    SticksPerKit: Mapped[int]       = mapped_column(Integer, nullable=True)
    CapacityPerStick: Mapped[int]   = mapped_column(Integer, nullable=True)
    Clock: Mapped[str]              = mapped_column(String, nullable=True)
    CASPrimary: Mapped[str]         = mapped_column(String, nullable=True)
    Misc: Mapped[str]               = mapped_column(String, nullable=True)
    Lighting: Mapped[str]           = mapped_column(String, nullable=True)
    RAMFormFactor: Mapped[str]      = mapped_column(String, nullable=True)
    RAMPricePerGB: Mapped[float]    = mapped_column(Float, nullable=True)

    ### Allow nested inheritance
    __mapper_args__ = { "polymorphic_abstract": True }


@dataclass
class DDR4(RAM):
    """Model for DDR4"""

    __tablename__ = "ddr4"
    __mapper_args__ = { "polymorphic_identity": "ddr4" }


@dataclass
class DDR5(RAM):
    """Model for DDR5"""

    __tablename__ = "ddr5"
    __mapper_args__ = { "polymorphic_identity": "ddr5" }


CATEGORY_CLASS_DICT = {
    "ssd":      SSD,
    "hdd":      HDD,
    "ddr4":     DDR4,
    "ddr5":     DDR5,
}
