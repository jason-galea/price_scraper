from flask_sqlalchemy import SQLAlchemy


# from flask_sqlalchemy import select
# from flask_sqlalchemy.query import Query

from src.generic_funcs import get_iso_8601_time
# from src.Database import db
from src.config import CATEGORY_CLASS_DICT


db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "Please do not create this table 🥺🥺🥺"

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)

    UTCTime     = db.Column(db.DateTime, nullable=False)
    Retailer    = db.Column(db.String, nullable=False)
    # Category    = db.Column(db.String, nullable=False)
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


    @staticmethod
    def get_most_recent(retailer) -> list:
        """
        Each "batch" of products in the table shares a UTC timestamp.\n
        This can be used to only fetch products from the latest batch.\n
        Returns a list of dictionaries.
        """
        latest_product: Product = Product.query.order_by(Product.id.desc()).first()

        products_list_of_tuples = Product.query.filter(
            Product.Retailer == retailer,
            # Product.Category == category,
            Product.UTCTime == latest_product.UTCTime,
        ).order_by(Product.id.desc()).all() ### Convert to list of KeyedTuples

        result = []
        for p in products_list_of_tuples:
            p_converted: dict = p.__dict__
            del p_converted["_sa_instance_state"]
            p_converted["UTCTime"] = get_iso_8601_time(p_converted["UTCTime"])

            result.append(p_converted)

        return result


    @staticmethod
    def export_to_db(db: SQLAlchemy, extracted_data: list):
        raise NotImplementedError




class SSD(Product):
    __tablename__ = "ssds"

    ### Schema
    ### NOTE: Any change requires DB reinitialisation
    FormFactor  = db.Column(db.String, nullable=False)
    CapacityTB  = db.Column(db.Float, nullable=False)
    CapacityGB  = db.Column(db.Float, nullable=False)
    PricePerTB  = db.Column(db.Float, nullable=False)
    PricePerGB  = db.Column(db.Float, nullable=False)


    def __init__(self,
        utctime, retailer, _category, title, url, priceaud, brand,
        formfactor, capacitytb, capacitygb, pricepertb, pricepergb
    ):
        self.UTCTime = utctime
        self.Retailer = retailer
        # self.Category = category
        self.Title = title
        self.URL = url
        self.PriceAUD = priceaud
        self.Brand = brand

        self.FormFactor = formfactor
        self.CapacityTB = capacitytb
        self.CapacityGB = capacitygb
        self.PricePerTB = pricepertb
        self.PricePerGB = pricepergb


    def export_to_db(db: SQLAlchemy, extracted_data: list) -> None:
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

        # category_class = CATEGORY_CLASS_DICT[category]
        # category_class = Product

        for product_data in extracted_data:
            # print(f"==> DEBUG: product_data = {json.dumps(product_data, indent=4)}")

            temp_product = SSD(
                title=product_data["Title"],
                retailer=product_data["Retailer"],
                utctime=product_data["UTCTime"],
                # category=product_data["Category"],
            )

            ### Write entry to DB queue
            db.session.add(temp_product)

        ### Flush DB queue
        print("==> DEBUG: Flushing DB queue")
        db.session.commit()

        print("==> DEBUG: Exiting 'export_to_db()' successfully?? :oooo")
