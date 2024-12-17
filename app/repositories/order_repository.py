from models import Order
from database import orders

class OrderRepository:
    @staticmethod
    # create a new order
    def create_order(product_id, user_id, quantity):
        order = Order(product_id, user_id, quantity)
        orders[order.order_id] = order
        return order


    @staticmethod
    # find all orders for a user
    def find_all_orders_for_user(user_id):
        return [order for order in orders.values() if order.user_id == user_id]


    @staticmethod
    # find order by order_id
    def find_order_by_id(order_id):
        return orders.get(order_id)


    @staticmethod
    # delete an order
    def delete_order(order_id):
        return orders.pop(order_id, None)
