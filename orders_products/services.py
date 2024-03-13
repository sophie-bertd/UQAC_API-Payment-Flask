from orders_products.models import init_db, Product, ShippingInformation, CreditCard, Transaction, Order

class OrderProductsServices(object) : 
    
    @classmethod
    def create_order_from_post_data(cls, post_data):
        # --------------------- A REVOIR ---------------------
        if not post_data['product_id']:
            return None
        if not post_data['quantity']:
            return None
        if post_data['quantity'] < 1:
            return None
        
        product = Product.get_product_by_id(post_data['product_id'])

        is_product_in_stock = product.in_stock

        if not is_product_in_stock:
            return None

        order = Order.create(
            product_id=product.id,
            quantity=post_data['quantity']
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
        
        ShippingInformation.create(
            country=shipping_info['country'],
            address=shipping_info['address'],
            postal_code=shipping_info['postal_code'],
            city=shipping_info['city'],
            province=shipping_info['province']
        )

        order = Order.get_order_by_id(order_id)
        order.email = post_data['email']
        order.shipping_information = shipping_info
        order.save()

        return order
    
    @classmethod
    def init_db_with_api(cls, products):
        for product in products:
            Product.create(
                name=product['name'],
                description=product['description'],
                price=product['price'],
                in_stock=product['in_stock'],
                id=product['id'],
                weight=product['weight'],
                image=product['image']
            )
            product.save()
        return True