from flask import render_template
from .models import Product

def index():
    products = Product.get_products()
    return render_template('index.html', products=products)
