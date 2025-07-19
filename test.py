import src.databaseService as databaseService
import src.node.nodeUtilities as nodeUtilities

orders = databaseService.get_order_objects_of_owner(2)
nodes = []
for every in orders:
    nodes.append(databaseService.get_node_object(every.pickup_node))
    nodes.append(databaseService.get_node_object(every.delivery_node))

# print(nodes)

nodeUtilities.write_travelMatrix(nodes, "travel.csv")