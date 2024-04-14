from rq import Queue
from redis import Redis
from orders_products.services import OrderProductsServices
import os
import json

redis_url = os.environ.get("REDIS_URL")
redis_conn = Redis.from_url(redis_url)

queue = Queue(connection=redis_conn)

def process_payment(order_id, post_data):
    response = OrderProductsServices.payment_order_to_api(order_id, post_data)
    return response
