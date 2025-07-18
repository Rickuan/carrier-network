import node.node as node

class Carrier:
    def __init__(self):
        self.order:list[list[node.Node]] = []

    def addOrder(self, pickup_node:node.Node, delivery_node:node.Node):
        self.order.append([pickup_node, delivery_node])