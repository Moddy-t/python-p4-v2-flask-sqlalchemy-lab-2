from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Customer, Item, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'


# -------------------- Customer Routes --------------------

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return abort(404, description="Customer not found")
    return jsonify(customer.to_dict())


@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(name=data['name'])
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return abort(404, description="Customer not found")
    data = request.json
    customer.name = data.get('name', customer.name)
    db.session.commit()
    return jsonify(customer.to_dict())


@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return abort(404, description="Customer not found")
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'}), 204


# -------------------- Item Routes --------------------

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    if not item:
        return abort(404, description="Item not found")
    return jsonify(item.to_dict())


@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item = Item(name=data['name'], price=data['price'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
    if not item:
        return abort(404, description="Item not found")
    data = request.json
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify(item.to_dict())


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if not item:
        return abort(404, description="Item not found")
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 204


# -------------------- Review Routes --------------------

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])


@app.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get(id)
    if not review:
        return abort(404, description="Review not found")
    return jsonify(review.to_dict())


@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    customer = Customer.query.get(data['customer_id'])
    item = Item.query.get(data['item_id'])
    if not customer or not item:
        return abort(404, description="Customer or Item not found")

    review = Review(comment=data['comment'], customer=customer, item=item)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201


@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get(id)
    if not review:
        return abort(404, description="Review not found")
    data = request.json
    review.comment = data.get('comment', review.comment)
    db.session.commit()
    return jsonify(review.to_dict())


@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return abort(404, description="Review not found")
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)