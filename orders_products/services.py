from orders_products.models import init_db, Product, ShippingInformation, CreditCard, Transaction, Order
import requests 
import json

class OrderProductsServices(object) : 
    
    @classmethod
    def create_order_from_post_data(cls, post_data):
        if post_data.keys() != {'product'}:
            return 0
        product = post_data['product']
        
        if product.keys() != {'id', 'quantity'}:
            return 0
        if product['quantity'] < 1:
            return 0
        
        product_db = Product.get_product_by_id(product['id'])
        if product_db is None:
            return 1
        is_product_in_stock = product_db.in_stock

        if not is_product_in_stock:
            return 2
        
        total_price = product_db.price * product['quantity']

        if product_db.weight < 500 :
            shipping_price = 5

        elif product_db.weight < 2000 :
            shipping_price = 10 

        else :
            shipping_price = 25 

        order = Order.create(
            product_id=product['id'],
            quantity=product['quantity'], 
            total_price=total_price,
            shipping_price=shipping_price
        )
        order.save()
        return order
    
    @classmethod
    def update_from_post_data(cls, order_id, post_data):
        if not post_data['email'] :
            return None
        
        if not post_data['shipping_information'] : 
            return None
        
        shipping_info = post_data['shipping_information']
        if not shipping_info['country'] or not shipping_info['address'] or not shipping_info['postal_code'] or not shipping_info['city'] or not shipping_info['province'] :
            return None
        
        shipping_info = ShippingInformation.create(
            country=shipping_info['country'],
            address=shipping_info['address'],
            postal_code=shipping_info['postal_code'],
            city=shipping_info['city'],
            province=shipping_info['province']
        )
        shipping_info.save()

        Order.update(email=post_data['email']).where(id == order_id).execute()
        Order.update(shipping_information=shipping_info).where(id == order_id).execute()

        return Order.get_order_by_id(order_id)
    
    @classmethod
    def api_payment(cls, url, data):
        response = requests.post(url, json=data)
        return response

    @classmethod
    def payment_order_to_api(cls, order_id, post_data) : 
        order = Order.get_order_by_id(order_id)

        if order["email"] is None or order["shipping_information"] is None :
            return {"code":0, "data" : None}
        
        if order["paid"] :
            return {"code":1, "data" : None}
        
        credit_card = post_data['credit_card']
        if not credit_card['number'] or not credit_card['expiration_year'] or not credit_card['cvv'] or not credit_card['name'] or not credit_card['expiration_month']:
            # Missing fields
            return {"code":2, "data" : None}

        amount_charged = order["total_price"] + order["shipping_price"]
        amount_charged = float(amount_charged)

        data = {
            "amount_charged": amount_charged,
            "credit_card": {
                "number": credit_card["number"],
                "expiration_year": credit_card["expiration_year"],
                "expiration_month": credit_card["expiration_month"],
                "cvv": credit_card["cvv"],
                "name": credit_card["name"]
            }
        }

        response = OrderProductsServices.api_payment("http://dimprojetu.uqac.ca/~jgnault/shops/pay/",data)

        if response.status_code != 200 :
            return {"code":3, "data" : response}
        
        body_response = response.text
        body_response = json.loads(body_response)
        body_transaction = body_response['transaction']
        transaction = Transaction.create(
            id=body_transaction['id'],
            success=body_transaction['success'],
            amount_charged=body_transaction['amount_charged']
        )
        transaction.save()

        credit_card = CreditCard.create(
            number=credit_card['number'],
            expiration_year=credit_card['expiration_year'],
            expiration_month=credit_card['expiration_month'],
            cvv=credit_card['cvv'],
            name=credit_card['name']
        )
        credit_card.save()

        Order.update(credit_card=credit_card).where(id == order_id).execute()
        Order.update(transaction=transaction).where(id == order_id).execute()
        Order.update(paid=True).where(id == order_id).execute()

        return {"code":4, "data" : None}