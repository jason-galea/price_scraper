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

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
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
            name='retailer_types'
        ),
    )

    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": "type", ### Allow inheritance
    }


    def __init__(self):
        raise NotImplementedError


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


    @staticmethod
    def export_to_db(products: list):
        raise NotImplementedError


class Drive(Product):
    __tablename__ = "drive"

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
    drive_type: Mapped[str]     = mapped_column(String) ### Allow inheritance

    CapacityTB: Mapped[float]   = mapped_column(Float)
    CapacityGB: Mapped[float]   = mapped_column(Float)
    PricePerTB: Mapped[float]   = mapped_column(Float)
    PricePerGB: Mapped[float]   = mapped_column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "drive",
        "polymorphic_on": "drive_type", ### Allow inheritance
    }


class SSD(Drive):
    __tablename__ = "ssd"

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
    FormFactor: Mapped[str]     = mapped_column(String)
    Protocol: Mapped[str]       = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_identity": "ssd",
    }


    def __init__(self,
        utctime, retailer, title, url, priceaud, brand, ### Product
        capacitytb, capacitygb, pricepertb, pricepergb, ### Drive
        formfactor, protocol ### SSD
    ):
        # pylint: disable=invalid-name
        self.UTCTime = utctime
        self.Retailer = retailer
        self.Title = title
        self.URL = url
        self.PriceAUD = priceaud
        self.Brand = brand

        self.CapacityTB = capacitytb
        self.CapacityGB = capacitygb
        self.PricePerTB = pricepertb
        self.PricePerGB = pricepergb

        self.FormFactor = formfactor
        self.Protocol = protocol


    ### TODO: Convert to dict kwargs, move into "Product" class
    @classmethod
    def export_to_db(cls, products: list) -> None:
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")
        for product in products:
            temp_product = cls(
                utctime=product["UTCTime"],
                retailer=product["Retailer"],
                title=product["Title"],
                url=product["URL"],
                priceaud=product["PriceAUD"],
                brand=product["Brand"],

                capacitytb=product["CapacityTB"],
                capacitygb=product["CapacityGB"],
                pricepertb=product["PricePerTB"],
                pricepergb=product["PricePerGB"],

                formfactor=product["FormFactor"],
                protocol=product["Protocol"],
            )

            db.session.add(temp_product) ### Add to DB queue

        print("==> INFO: Flushing DB queue")
        db.session.commit() ### Flush DB queue


class HDD(Drive):
    __tablename__ = "hdd"

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
    Series: Mapped[str]         = mapped_column(String)
    Model: Mapped[str]          = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_identity": "hdd",
    }


    def __init__(self,
        utctime, retailer, title, url, priceaud, brand, ### Product
        capacitytb, capacitygb, pricepertb, pricepergb, ### Drive
        series, model, ### HDD
    ):
        # pylint: disable=invalid-name
        self.UTCTime = utctime
        self.Retailer = retailer
        self.Title = title
        self.URL = url
        self.PriceAUD = priceaud
        self.Brand = brand

        self.CapacityTB = capacitytb
        self.CapacityGB = capacitygb
        self.PricePerTB = pricepertb
        self.PricePerGB = pricepergb

        self.Series = series
        self.Model = model


    ### TODO: Convert to dict kwargs, move into "Product" class
    @classmethod
    def export_to_db(cls, products: list) -> None:
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")
        for product in products:
            temp_product = cls(
                utctime=product["UTCTime"],
                retailer=product["Retailer"],
                title=product["Title"],
                url=product["URL"],
                priceaud=product["PriceAUD"],
                brand=product["Brand"],

                capacitytb=product["CapacityTB"],
                capacitygb=product["CapacityGB"],
                pricepertb=product["PricePerTB"],
                pricepergb=product["PricePerGB"],
                
                series=product["Series"],
                model=product["Model"],
            )

            db.session.add(temp_product) ### Add to DB queue

        print("==> INFO: Flushing DB queue")
        db.session.commit() ### Flush DB queue


CATEGORY_CLASS_DICT = {
    "ssd":      SSD,
    "hdd":      HDD,
    # "ddr4":     RAM,
    # "ddr5":     RAM,
}
