from peewee import *
import os 
import requests
import html

def get_db():
    # database_path = os.path.join("instance", "database.sqlite")
    db_name = os.environ.get("DB_NAME")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    return PostgresqlDatabase(db_name, user=db_user, password=db_password, host=db_host, port=db_port)
 
def close_db():
    db = get_db()
    db.close()

def remove_null_characters(data):
    return data.replace('\x00', '')

def init_db() : 
    # if os.path.exists("instance/database.sqlite"):
    #     os.remove("instance/database.sqlite")

    with get_db() as db:
        db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order, OrderProduct, ErrorTransaction])
        Product.delete().execute()
        OrderProduct.delete().execute()
        Order.delete().execute()
        ErrorTransaction.delete().execute()
        Transaction.delete().execute()
        ShippingInformation.delete().execute()
        CreditCard.delete().execute()

        url = "http://dimprojetu.uqac.ca/~jgnault/shops/products/"
        response = requests.get(url)
        data = response.json()

        products = data['products']
        for product in products:
            product_save = Product.create(
                name=remove_null_characters(product['name']),
                description=remove_null_characters(product['description']),
                price=product['price'],
                in_stock=product['in_stock'],
                id=product['id'],
                weight=product['weight'],
                image=remove_null_characters(product['image'])
            )
            product_save.save()

class Product(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    in_stock = BooleanField()
    description = TextField()
    price = DecimalField()
    weight = DecimalField(
        constraints=[Check('weight > 0')]
    )
    image = CharField()

    class Meta:
        database = get_db()  

    @classmethod
    def get_products(cls):
        # return cls.select()  
        products = Product.select() 
        list_products = [
            {
                "id": product.id,
                "name": product.name,
                "in_stock": product.in_stock,
                "description": product.description,
                "price": product.price,
                "weight": product.weight,
                "image": product.image
            }
            for product in products
        ]

        return list_products
    
    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.get_or_none(cls.id == product_id)

class ShippingInformation(Model) : 
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField()

    class Meta:
        database = get_db()

class CreditCard(Model):
    name = CharField()
    number = CharField()
    expiration_year = IntegerField()
    expiration_month = IntegerField()
    cvv = CharField()

    class Meta:
        database = get_db()

class Transaction(Model):
    # id = CharField(primary_key=True)
    id = CharField(primary_key=True)
    success = BooleanField()
    amount_charged = DecimalField()

    class Meta:
        database = get_db()

class ErrorTransaction(Model) :
    transaction = ForeignKeyField(Transaction, backref='error_transactions')
    code = CharField()
    name = CharField()

    class Meta:
        database = get_db()

class Order(Model):
    id = AutoField()
    total_price = DecimalField()
    email = CharField(null=True)
    paid = BooleanField(default=False)
    shipping_price = DecimalField()
    # product_id = ForeignKeyField(Product, backref='orders')
    # quantity = IntegerField(
    #     constraints=[Check('quantity > 0')]
    # )
    shipping_information = ForeignKeyField(ShippingInformation, backref='orders', null=True)
    credit_card = ForeignKeyField(CreditCard, backref='orders', null=True)
    transaction = ForeignKeyField(Transaction, backref='orders', null=True)

    class Meta:
        database = get_db()

    @classmethod
    def get_order_by_id(cls, order_id):
        # Revoir affichage credit_card, shipping_information, transaction
        order = cls.get_or_none(cls.id == order_id)
        if order is None:
            return None
        
        if order.shipping_information is not None:
            shipping_information = {
                "country": order.shipping_information.country,
                "address": order.shipping_information.address,
                "postal_code": order.shipping_information.postal_code,
                "city": order.shipping_information.city,
                "province": order.shipping_information.province
            }
        else:
            shipping_information = None

        if order.credit_card is not None:
            credit_card = {
                "name": order.credit_card.name,
                "number": order.credit_card.number,
                "expiration_year": order.credit_card.expiration_year,
                "expiration_month": order.credit_card.expiration_month,
                "cvv": order.credit_card.cvv
            }
        else:
            credit_card = None

        if order.transaction is not None:
            error_transactions = None
            error = order.transaction.error_transactions.first()

            if error :
                error_transactions = {
                        "code": error.code,
                        "name": html.unescape(error.name)
                    }
               
                transaction = {
                    "success": order.transaction.success,
                    "error": error_transactions,
                    "amount_charged": order.transaction.amount_charged
                }
            else : 
                transaction = {
                    "success": order.transaction.success,
                    "amount_charged": order.transaction.amount_charged
                }
        
        else:
            transaction = None

        products = [] 
        for order_product in order.order_products:
            products.append(
                {
                    "id": order_product.product_id,
                    "quantity": order_product.quantity
                }
            )

        order =  {
                    "id": order.id,
                    "total_price": order.total_price,
                    "email": order.email,
                    "credit_card": credit_card,
                    "shipping_information": shipping_information,
                    "paid": order.paid,
                    "transaction": transaction,
                    "products": products,
                    "shipping_price": order.shipping_price
                }
        
        return order

class OrderProduct(Model):
    order = ForeignKeyField(Order, backref='order_products')
    product_id = IntegerField()
    quantity = IntegerField(constraints=[Check('quantity > 0')])

    class Meta:
        database = get_db()