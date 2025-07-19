from src.node.node import Node
from src.agent.carrier import Carrier

class OrderItem:
    def __init__(self, id:int, pickup_node:Node, delivery_node:Node, current_owner:Carrier):
        self.id = id
        self.pickup_node = pickup_node
        self.delivery_node = delivery_node
        self.current_owner = current_owner