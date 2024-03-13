from peewee import *
import os 
import json

def get_db():
    database_path = os.path.join("instance", "database.sqlite")
    return SqliteDatabase(database_path)
 
def close_db():
    db = get_db()
    db.close()

def init_db() : 
# A REVOIR SI ON PEUT FAIRE MIEUX
    if os.path.exists("instance/database.sqlite"):
        os.remove("instance/database.sqlite")
    with get_db() as db:
        db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order])

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
    id = CharField()
    success = BooleanField()
    amount_charged = DecimalField()

    class Meta:
        database = get_db()

class Order(Model):
    # total_price = product.price * quantity
    id = AutoField()
    total_price = DecimalField()
    email = CharField(null=True)
    paid = BooleanField(default=False)
    shipping_price = DecimalField()
    product_id = ForeignKeyField(Product, backref='orders')
    quantity = IntegerField(
        constraints=[Check('quantity > 0')]
    )
    shipping_information = ForeignKeyField(ShippingInformation, backref='orders', null=True)
    credit_card = ForeignKeyField(CreditCard, backref='orders', null=True)
    transaction = ForeignKeyField(Transaction, backref='orders', null=True)

    class Meta:
        database = get_db()

    # def save(self, *args, **kwargs):
    #     product = Product.get_product_by_id(self.product_id.id)
    #     total_price = product.price * self.quantity
    #     self.update(total_price=total_price).where(self.id == self.id).execute()

    #     if product.weight < 500 :
    #         shipping_price = 5 + total_price
    #         self.update(shipping_price=shipping_price).where(self.id == self.id).execute()

    #     elif product.weight < 2000 :
    #         shipping_price = 10 + total_price
    #         self.update(shipping_price=shipping_price).where(self.id == self.id).execute()

    #     else :
    #         shipping_price = 25 + total_price
    #         self.update(shipping_price=shipping_price).where(self.id == self.id).execute()

    #     return super().save(*args, **kwargs)

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

        order =  {
                    "id": order.id,
                    "total_price": order.total_price,
                    "email": order.email,
                    "credit_card": order.credit_card,
                    "shipping_information": shipping_information,
                    "paid": order.paid,
                    "transaction": order.transaction,
                    "product": 
                        {
                            "id": order.product_id.id,
                            "quantity": order.quantity,
                        }, 
                    "shipping_price": order.shipping_price
                }
        
        return order