from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Metadata naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with custom metadata
db = SQLAlchemy(metadata=metadata)

# Association table for reviews (many-to-many relationship between customers and items)
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Only serialize relevant fields to avoid recursion issues
    serialize_rules = ('-customer.reviews', '-item.reviews', 'customer_id', 'item_id')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

# Customer model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with reviews
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to access items directly from Customer
    items = association_proxy('reviews', 'item', creator=lambda item: Review(comment='Added by proxy', item=item))

    # Serialize the customer with reviews and items, avoiding circular references
    serialize_rules = ('-reviews.customer', '-items.reviews')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# Item model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship with reviews
    reviews = db.relationship('Review', back_populates='item')

    # Serialize the item with reviews, avoiding circular references
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'