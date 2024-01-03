from flask_sqlalchemy import SQLAlchemy

from src.generic_funcs import get_iso_8601_time


db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "Please do not create this table 🥺🥺🥺"

    ### Schema
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
        # category_class = CATEGORY_CLASS_DICT[category]
        # category_class = __class__

        latest_product = cls.query.order_by(cls.id.desc()).first()

        products_list_of_tuples = cls.query.filter(
            cls.Retailer == retailer,
            # cls.Category == category,
            cls.UTCTime == latest_product.UTCTime,
        ).order_by(cls.id.desc()).all() ### Convert to list of KeyedTuples

        result = []
        for p in products_list_of_tuples:
            p_converted: dict = p.__dict__
            del p_converted["_sa_instance_state"]
            p_converted["UTCTime"] = get_iso_8601_time(p_converted["UTCTime"])

            result.append(p_converted)

        return result


    @staticmethod
    def export_to_db():
        raise NotImplementedError


class SSD(Product):
    __tablename__ = "ssds"

    ### Schema
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


    def export_to_db(db: SQLAlchemy, products: list) -> None:
        print("==> DEBUG: Entered 'export_to_db()'")
        # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

        # scraper  | ==> DEBUG: extracted_data[0] = {
        # scraper  |     "UTCTime": "2024-01-01T08:55:56.648311",
        # scraper  |     "Retailer": "PCCG",
        # scraper  |     "Title": "Samsung 870 EVO 2.5in SATA SSD 1TB",
        # scraper  |     "URL": "https://www.pccasegear.com/products/53095/samsung-870-evo-2-5in-sata-ssd-1tb",
        # scraper  |     "PriceAUD": 165,
        # scraper  |     "Category": "ssd",

        # scraper  |     "FormFactor": "2.5in",
        # scraper  |     "Protocol": "SATA",
        # scraper  |     "Brand": "Samsung",
        # scraper  |     "CapacityGB": 1000,
        # scraper  |     "CapacityTB": 1.0,
        # scraper  |     "PricePerGB": 0.17,
        # scraper  |     "PricePerTB": 165.0
        # scraper  | }

        for product in products:
            # print(f"==> DEBUG: product = {json.dumps(product, indent=4)}")
            temp_product = SSD(
                utctime=product["UTCTime"],
                retailer=product["Retailer"],
                # category=product["Category"],
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
        print("==> DEBUG: Flushing DB queue")
        db.session.commit()

        print("==> DEBUG: Exiting 'export_to_db()' successfully?? :oooo")


CATEGORY_CLASS_DICT = {
    # "hdd":      HDD,
    "ssd":      SSD,
    # "ddr4":     RAM,
    # "ddr5":     RAM,
}
