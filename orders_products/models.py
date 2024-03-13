from peewee import *
import os 

def get_db():
    database_path = os.path.join("instance", "database.sqlite")
    return SqliteDatabase(database_path)
 
def close_db():
    db = get_db()
    db.close()

def init_db() : 
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
    image_url = CharField()

    class Meta:
        database = get_db()  

    @classmethod
    def get_products(cls):
        return cls.select()  
    
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
    total_price = DecimalField()
    email = CharField()
    paid = BooleanField(default=False)
    shipping_price = DecimalField()
    product_id = ForeignKeyField(Product, backref='orders')
    quantity = IntegerField(
        constraints=[Check('quantity > 0')]
    )
    shipping_information = ForeignKeyField(ShippingInformation, backref='orders')
    credit_card = ForeignKeyField(CreditCard, backref='orders')
    transaction = ForeignKeyField(Transaction, backref='orders')

    class Meta:
        database = get_db()

    @classmethod
    def save(cls, *args, **kwargs):
        total_price = cls.product_id.price * cls.quantity
        cls.update(total_price=total_price).where(cls.id == cls.id).execute()

        if cls.product_id.weight < 500 :
            shipping_price = 5 + total_price
            cls.update(shipping_price=shipping_price).where(cls.id == cls.id).execute()
        elif cls.product_id.weight < 2000 :
            shipping_price = 10 + total_price
            cls.update(shipping_price=shipping_price).where(cls.id == cls.id).execute()
        else :
            shipping_price = 25 + total_price
            cls.update(shipping_price=shipping_price).where(cls.id == cls.id).execute()

        return super().save(*args, **kwargs)

    @classmethod
    def get_order_by_id(cls, order_id):
        return cls.get_or_none(cls.id == order_id)