from flask import jsonify, request, abort
from service.models import Product, Category
from service.common import status
from . import app


def check_content_type(content_type):
    if request.headers.get("Content-Type") != content_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")


@app.route("/health")
def healthcheck():
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/products", methods=["POST"])
def create_products():
    check_content_type("application/json")
    product = Product().deserialize(request.get_json())
    product.create()
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": f"/products/{product.id}"}


@app.route("/products", methods=["GET"])
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(getattr(Category, category.upper()))
    elif available:
        value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(value)
    else:
        products = Product.all()
    return [product.serialize() for product in products], status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return product.serialize(), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT
