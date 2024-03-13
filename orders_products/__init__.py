import os 

from flask import Flask, request, redirect, url_for, abort, jsonify
import requests 

from orders_products.models import get_db, init_db, Product, ShippingInformation, CreditCard, Transaction, Order
from orders_products.services import OrderProductsServices
from orders_products import view

from peewee import * 

import json

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

    def api_products(url):
        response = requests.get(url)
        data = response.json()
        OrderProductsServices.init_db_with_api(data)

    url = "http://dimprojetu.uqac.ca/~jgnault/shops/products/"
    api_products(url)

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
        # view.index()
        list_products = Product.get_products()
        list_products = {
            "products": list_products
        }
        return jsonify(list_products)
    
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        order = Order.get_order_by_id(order_id)
        if not order:
            return abort(404)
        return jsonify(order)         
        
    @app.route('/order', methods=['POST'])
    def post_order():
        order = OrderProductsServices.create_order_from_post_data(request.get_json())
        if order is None:
            # Missing fields
            # return {"error": "Invalid data provided"}, 400
            return abort(422)
        
        if not order:
            # Out of stock
            return abort(422)

        # Ajouter le code 302 pour la redirection
        return redirect(url_for('get_order', order_id=order.id))
    
    @app.route('/order/<int:order_id>', methods=['PUT'])
    def put_order(order_id):
        order = Order.get_order_by_id(order_id)
        if not order:
            return abort(404)
        
        body = request.get_json()
        if body.keys() == {"order"} : 
            body = body["order"]
            if body.keys() != {"shipping_information", "email"} :
                return abort(404)
            
            if body["shipping_information"] != None or body["email"] != None :
                res = OrderProductsServices.update_from_post_data(order_id, body)

                if res is None:
                    # Missing fields
                    return abort(422)
                else : 
                # Ajouter le code 302 pour la redirection
                    return redirect(url_for('get_order', order_id=order_id))
                
            else :
                # Vérifier erreur
                return abort(404)
        
        elif body.keys() == {"credit_card"} :

            res = OrderProductsServices.payment_order_to_api(order_id, body)

            if res is None:
                # Missing fields / à voir
                return abort(422)
            
            # Ajouter le code 302 pour la redirection
            return redirect(url_for('get_order', order_id=order_id))
        
        else :
            return abort(404)
  
    # @app.error_handler_spec(None, 422)
    # def unprocessable_entity(error):
    #     return views.unprocessable_entity()
    
    # @app.error_handler_spec(None, 404)
    # def not_found(error):
    #     return views.not_found()

    return app
