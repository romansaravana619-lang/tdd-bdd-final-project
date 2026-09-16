from decimal import Decimal
from enum import Enum
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Category(Enum):
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.UNKNOWN)

    def create(self):
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        if not self.id:
            raise ValueError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.price = Decimal(str(data["price"]))
        if not isinstance(data["available"], bool):
            raise ValueError("available must be boolean")
        self.available = data["available"]
        self.category = getattr(Category, data["category"])
        return self

    @classmethod
    def find(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        return cls.query.filter(cls.available == available)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
