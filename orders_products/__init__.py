import os 

from flask import Flask, request, redirect, url_for, abort
import requests 

from orders_products.models import get_db, init_db, Product, ShippingInformation, CreditCard, Transaction, Order
from orders_products.services import OrderProductsServices
from orders_products import views

def create_app(initial_config=None):
    # --------------------- REGLER LE PROBLEME DE LA BASE DE DONNEES ---------------------

    app = Flask("orders_products", instance_relative_config=True)
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.sqlite')

    if initial_config != None:
         app.config.update(initial_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    init_db()
    api_products()

    @app.before_request
    def before_request():
        db = get_db()
        db.connect()
        db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order])

    @app.after_request
    def after_request(response):
        db = get_db()
        db.close()
        return response

    @app.route('/', methods=['GET'])
    def index():
        products = Product.get_products()
        return products
        # if products:
        #     return views.index(products)
        # else:
        #     return views.index_empty()

    @app.route('/order', methods=['POST'])
    def post_order():
        order = OrderProductsServices.create_order_from_post_data(request.form)
        if order is None:
            # Missing fields
            return abort(422)
        
        if not order:
            # Out of stock
            return abort(422)

        # Ajouter le code 302 pour la redirection
        return redirect(url_for('order', order_id=order.id))


    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        order = Order.get_order_by_id(order_id)
        if not order:
            return abort(404)

        return views.view_order(order)
    
    @app.route('/order/<int:order_id>', methods=['PUT'])
    def put_order(order_id):
        order = Order.get_order_by_id(order_id)
        if not order:
            return abort(404)

        res = OrderProductsServices.update_from_post_data(order_id, request.form)
        if res is None:
            # Missing fields
            return abort(422)

    # CARTE DE CREDIT

    # @app.route('/shops/pay', methods=['POST'])
    # # TODO

    @app.route('/api_products', methods=['GET'])
    def api_products():
        url = "http://dimprojetu.uqac.ca/~jgnault/shops/products/"
        response = requests.get(url)

        data = response.json()
        OrderProductsServices.init_db_with_api(data)

        return redirect(url_for('index'))   
    
    # @app.route('/api_payment', methods=['POST'])
  
    # @app.error_handler_spec(None, 422)
    # def unprocessable_entity(error):
    #     return views.unprocessable_entity()
    
    # @app.error_handler_spec(None, 404)
    # def not_found(error):
    #     return views.not_found()

    return app
