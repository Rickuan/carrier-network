import os

import src.databaseService as databaseService
import src.node.nodeUtilities as nodeUtilities
import src.routingModel.routing as routing
import src.dirNavigator as dirNavigator

orders = databaseService.get_order_objects_of_owner(2)
nodes = []
for every in orders:
    nodes.append(databaseService.get_node_object(every.pickup_node))
    nodes.append(databaseService.get_node_object(every.delivery_node))

nodes.append(databaseService.get_node_object("Warehouse B"))
nodeUtilities.write_travelMatrix(nodes, "travel.csv")

node_pairs = []
for every in orders:
    node_pairs.append([databaseService.get_node_object(every.pickup_node), databaseService.get_node_object(every.delivery_node)])

print(routing.solve_PnD_problem(node_pairs, databaseService.get_node_object("Warehouse B"), databaseService.read_travelMatrix(os.path.join(dirNavigator.DIR_TRAVELMATRIX, "travel.csv"))))