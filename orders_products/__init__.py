import os 

from flask import Flask, request, redirect, url_for, jsonify, abort

from orders_products.models import get_db, init_db, Product, ShippingInformation, CreditCard, Transaction, Order
from orders_products.services import OrderProductsServices
from orders_products import view

from peewee import * 
import json
import redis 

def create_app(initial_config=None):
    app = Flask("orders_products", instance_relative_config=True, template_folder="../templates", static_folder="../static")
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.sqlite')

    if initial_config != None:
         app.config.update(initial_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    get_db()

    redis_url = os.environ.get("REDIS_URL") 
    redis_conn = redis.Redis.from_url(redis_url)

    register_cli_commands(app)

    @app.before_request
    def before_request():
        db = get_db()
        db.connect()

    @app.after_request
    def after_request(response):
        db = get_db()
        db.close()
        return response

    @app.route('/', methods=['GET'])
    def index():
        
        list_products = Product.get_products()
        if list_products is None:
            return {"error": 
                    {
                        "product" : {
                            "code" : "not_found",
                            "name" : "Aucun produit n'est disponible"
                        }
                    }
                    }, 404

        list_products = {
            "products": list_products
        }
        # return jsonify(list_products)
        return view.index()
    
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        cache_key = f"order_{order_id}"
        cached_order = redis_conn.get(cache_key)

        if cached_order:
            return json.loads(cached_order)

        order = Order.get_order_by_id(order_id)
        if not order:
            return {"error": 
                    {
                        "order" : {
                            "code" : "not_found",
                            "name" : "La commande n'existe pas"
                        }
                    }
                    }, 404
        return jsonify(order)         
        
    @app.route('/order', methods=['POST'])
    def post_order():
        order = OrderProductsServices.create_order_from_post_data(request.get_json())
        if order == 0:
            # Missing fields
            return {"error" : 
                    {
                        "product" : {
                            "code" : "missing_fields",
                            "name" : "La création d'une commande nécessite un produit"
                        }
                    }}, 422
        if order == 1:
            # Missing fields
            return {"error" : 
                    {
                        "product" : {
                            "code" : "not_found",
                            "name" : "Le produit demandé n'existe pas"
                        }
                    }}, 404
        if order == 2:
            # Out of stock
            return {"error" : 
                    {
                        "product" : {
                            "code" : "out-of-inventory",
                            "name" : "Le produit demandé n'est pas en inventaire"
                        }
                    }}, 422

        # return {
        #     "Location": f"/order/{order.id}"
        # }
        return redirect(url_for('get_order', order_id=order.id))
    
    @app.route('/order/<int:order_id>', methods=['PUT'])
    def put_order(order_id):
        order = Order.get_order_by_id(order_id)
        if not order:
            return {"error": 
                    {
                        "order" : {
                            "code" : "not_found",
                            "name" : "La commande n'existe pas"
                        }
                    }
                    }, 404
        
        body = request.get_json()
        if body.keys() == {"order"} : 
            body = body["order"]
            if body.keys() != {"shipping_information", "email"} :
                return {
                    "errors": {
                        "order": {
                            "code": "missing_fields",
                            "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                        }
                    }
                }, 422
            
            else : 
                res = OrderProductsServices.update_from_post_data(order_id, body)

                if res is None:
                    # Missing fields
                    return {
                        "errors": {
                            "order": {
                                "code": "missing_fields",
                                "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                            }
                        }
                    }, 422
                else : 
                    return jsonify(success=True)
        
        elif body.keys() == {"credit_card"} :

            res = OrderProductsServices.payment_order_to_api(order_id, body)

            if res["code"] == 0:
                return {
                        "errors": {
                            "order": {
                                "code": "missing_fields",
                                "name": "Les informations du client sont nécessaire avant de procéder au paiement"
                            }
                        }
                }, 422
            
            elif res["code"] == 1:
                return {
                        "errors": {
                            "order": {
                                "code": "already_paid",
                                "name": "La commande a déjà été payée"
                            }
                        }
                }, 422
            
            elif res["code"] == 2:
                return {
                        "errors": {
                            "order": {
                                "code": "missing_fields",
                                "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                            }
                        }
                }, 422
            
            # elif res["code"] == 3:  
            #     response = res["data"].text 
            #     response = json.loads(response)
            #     return response , res["data"].status_code
            
            return jsonify(success=True)
        
        else :
            return {
                "errors": {
                    "order": {
                        "code": "missing_fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                    }
                }
            }, 422

    return app

def register_cli_commands(app) :
    @app.cli.command("init-db")
    def init_db_command():
        init_db()

