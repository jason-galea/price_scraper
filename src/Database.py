from flask_sqlalchemy import SQLAlchemy

from src.generic_funcs import get_iso_8601_time


db = SQLAlchemy()


class Product(db.Model):
    """
    Defines common SQLAlchemy database tables variables & functions
    """

    ### Schema (Common fields only)
    ### NOTE: Any change requires DB reinitialisation
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)

    UTCTime     = db.Column(db.DateTime, nullable=False)
    Retailer    = db.Column(db.String, nullable=False)
    Title       = db.Column(db.String, nullable=False)
    URL         = db.Column(db.String, nullable=False)
    PriceAUD    = db.Column(db.Float, nullable=False)
    Brand       = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            Retailer.in_(['pccg', 'scorptec', 'centrecom']),
            name='retailer_types'
        ),
    )


    def __init__(self):
        raise NotImplementedError


    def __repr__(self):
        return f"<{self.__class__.__name__} {self.Title}>"


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


class SSD(Product):

    ### Schema (Additional fields only)
    ### NOTE: Any change requires DB reinitialisation
    FormFactor  = db.Column(db.String, nullable=False)
    Protocol    = db.Column(db.String, nullable=False)
    CapacityTB  = db.Column(db.Float, nullable=False)
    CapacityGB  = db.Column(db.Float, nullable=False)
    PricePerTB  = db.Column(db.Float, nullable=False)
    PricePerGB  = db.Column(db.Float, nullable=False)


    def __init__(self,
        utctime, retailer, title, url, priceaud, brand,
        formfactor, protocol, capacitytb, capacitygb, pricepertb, pricepergb
    ):
        # pylint: disable=invalid-name
        self.UTCTime = utctime
        self.Retailer = retailer
        self.Title = title
        self.URL = url
        self.PriceAUD = priceaud
        self.Brand = brand

        self.FormFactor = formfactor
        self.Protocol = protocol
        self.CapacityTB = capacitytb
        self.CapacityGB = capacitygb
        self.PricePerTB = pricepertb
        self.PricePerGB = pricepergb


    @staticmethod
    def export_to_db(products: list) -> None:
        # print("==> DEBUG: Entered 'export_to_db()'")
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

        for product in products:
            # print(f"==> DEBUG: product = {json.dumps(product, indent=4)}")
            temp_product = SSD(
                utctime=product["UTCTime"],
                retailer=product["Retailer"],
                title=product["Title"],
                url=product["URL"],
                priceaud=product["PriceAUD"],
                brand=product["Brand"],

                formfactor=product["FormFactor"],
                protocol=product["Protocol"],
                capacitytb=product["CapacityTB"],
                capacitygb=product["CapacityGB"],
                pricepertb=product["PricePerTB"],
                pricepergb=product["PricePerGB"],
            )

            ### Add to DB queue
            db.session.add(temp_product)

        ### Flush DB queue
        print("==> INFO: Flushing DB queue")
        db.session.commit()

        # print("==> DEBUG: Exiting 'export_to_db()' successfully?? :oooo")


class HDD(Product):

    ### Schema (Additional fields only)
    ### NOTE: Any change requires DB reinitialisation
    FormFactor  = db.Column(db.String, nullable=False)
    Protocol    = db.Column(db.String, nullable=False)
    CapacityTB  = db.Column(db.Float, nullable=False)
    CapacityGB  = db.Column(db.Float, nullable=False)
    PricePerTB  = db.Column(db.Float, nullable=False)
    PricePerGB  = db.Column(db.Float, nullable=False)


    def __init__(self,
        utctime, retailer, title, url, priceaud, brand,
        formfactor, protocol, capacitytb, capacitygb, pricepertb, pricepergb
    ):
        # pylint: disable=invalid-name
        self.UTCTime = utctime
        self.Retailer = retailer
        self.Title = title
        self.URL = url
        self.PriceAUD = priceaud
        self.Brand = brand

        self.FormFactor = formfactor
        self.Protocol = protocol
        self.CapacityTB = capacitytb
        self.CapacityGB = capacitygb
        self.PricePerTB = pricepertb
        self.PricePerGB = pricepergb


    @staticmethod
    def export_to_db(products: list) -> None:
        # print("==> DEBUG: Entered 'export_to_db()'")
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

        for product in products:
            # print(f"==> DEBUG: product = {json.dumps(product, indent=4)}")
            temp_product = SSD(
                utctime=product["UTCTime"],
                retailer=product["Retailer"],
                title=product["Title"],
                url=product["URL"],
                priceaud=product["PriceAUD"],
                brand=product["Brand"],

                formfactor=product["FormFactor"],
                protocol=product["Protocol"],
                capacitytb=product["CapacityTB"],
                capacitygb=product["CapacityGB"],
                pricepertb=product["PricePerTB"],
                pricepergb=product["PricePerGB"],
            )

            ### Add to DB queue
            db.session.add(temp_product)

        ### Flush DB queue
        print("==> INFO: Flushing DB queue")
        db.session.commit()

        # print("==> DEBUG: Exiting 'export_to_db()' successfully?? :oooo")



CATEGORY_CLASS_DICT = {
    "hdd":      HDD,
    "ssd":      SSD,
    # "ddr4":     RAM,
    # "ddr5":     RAM,
}
