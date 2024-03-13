from flask import render_template
from .model import Product

def index():
    products = Product.get_products()
    return render_template('../templates/index.html', products=products)
