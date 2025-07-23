# """Simple Pickup Delivery Problem (PDP)."""

# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp
# import os, pandas

# import src.dirNavigator as dirNavigator
# from src.node.node import Node

# def create_data_model(node_pairs:list[list[Node]], travelMatrix:list[list[int]]):
#     """Stores the data for the problem."""

#     def convertNodeIDToNodeIndex(node_pairs:list[list[Node]]) -> list[list[int]]:
#         pair_of_nodeIndex:list[list[Node]] = []
#         list_of_nodeID:list[str] = []

#         for order in node_pairs:
#             list_of_nodeID.append(order[0].id)
#             list_of_nodeID.append(order[1].id)
#         list_of_sorted_nodeID = sorted(list_of_nodeID)

#         for i in range(len(list_of_nodeID)//2):
#             pair_of_nodeIndex.append([list_of_sorted_nodeID.index(list_of_nodeID[2*i]), list_of_sorted_nodeID.index(list_of_nodeID[2*i+1])])

#         return pair_of_nodeIndex

#     data = {}
#     data["pickup_delivery_index_pairs"] = convertNodeIDToNodeIndex(node_pairs)
#     data["distance_matrix"] = travelMatrix
#     data["num_vehicles"] = 1
#     data["depot"] = len(data["pickup_delivery_index_pairs"]*2)

#     return data

# def print_solution(node_pairs:list[list[Node]], node_warehouse:Node, data:dict, manager:pywrapcp.RoutingIndexManager, routing:pywrapcp.RoutingModel, solution):
#     """Prints solution on console."""

#     resolved_solution = {}
#     resolved_solution["objective"] = solution.ObjectiveValue()
#     resolved_solution["distance"] = []
#     resolved_solution["route_map_index"] = []
#     resolved_solution["route_map_ID"] = []

#     def convertNodeIndexToNodeID(node_pairs:list[list[Node]], node_index:list[int]) -> list[Node]:
#         list_of_nodeID:list[str] = []

#         for order in node_pairs:
#             list_of_nodeID.append(order[0].id)
#             list_of_nodeID.append(order[1].id)
#         list_of_sorted_nodeID = sorted(list_of_nodeID)

#         return [list_of_sorted_nodeID[every] if every < len(list_of_sorted_nodeID) else node_warehouse.id for every in node_index]

#     for vehicle_id in range(data["num_vehicles"]):
#         resolved_solution["route_map_index"].append([])
#         resolved_solution["route_map_ID"].append([])

#         if not routing.IsVehicleUsed(solution, vehicle_id):
#             continue
#         index = routing.Start(vehicle_id)

#         route_distance = 0
#         while not routing.IsEnd(index):
#             resolved_solution["route_map_index"][-1].append(manager.IndexToNode(index))
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             route_distance += routing.GetArcCostForVehicle(
#                 previous_index, index, vehicle_id
#             )
#         # go back to depot
#         resolved_solution["route_map_index"][-1].append(manager.IndexToNode(index))
#         resolved_solution["route_map_ID"][-1] = convertNodeIndexToNodeID(node_pairs, resolved_solution["route_map_index"][-1])
#         resolved_solution["distance"].append(route_distance)

#     return resolved_solution

# def solve_PnD_problem(node_pairs:list[list[Node]], node_warehouse:Node, travelMatrix:list[list[int]]):
#     """Entry point of the program."""
#     # Instantiate the data problem.
#     data = create_data_model(node_pairs, travelMatrix)

#     # Create the routing index manager.
#     manager:pywrapcp.RoutingIndexManager = pywrapcp.RoutingIndexManager(
#         len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
#     )

#     # Create Routing Model.
#     routing:pywrapcp.RoutingModel = pywrapcp.RoutingModel(manager)


#     # Define cost of each arc.
#     def distance_callback(from_index, to_index):
#         """Returns the manhattan distance between the two nodes."""
#         # Convert from routing variable Index to distance matrix NodeIndex.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data["distance_matrix"][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add Distance constraint.
#     dimension_name = "Distance"
#     routing.AddDimension(
#         transit_callback_index,
#         0,  # no slack
#         8000,  # vehicle maximum travel distance
#         True,  # start cumul to zero
#         dimension_name,
#     )
#     distance_dimension = routing.GetDimensionOrDie(dimension_name)
#     distance_dimension.SetGlobalSpanCostCoefficient(100)

#     # Define Transportation Requests.
#     for request in data["pickup_delivery_index_pairs"]:
#         pickup_index = manager.NodeToIndex(request[0])
#         delivery_index = manager.NodeToIndex(request[1])

#         routing.AddPickupAndDelivery(pickup_index, delivery_index)
#         routing.solver().Add(
#             routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
#         )
#         routing.solver().Add(
#             distance_dimension.CumulVar(pickup_index)
#             <= distance_dimension.CumulVar(delivery_index)
#         )

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
#     )

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         return print_solution(node_pairs, node_warehouse, data, manager, routing, solution)
#     else:
#         print("NO SOLUTION")
#         return None


"""Simple Pickup and Delivery Problem (PDP) Solver with OR-Tools."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from src.node.node import Node


def create_data_model(node_pairs: list[list[Node]], node_warehouse: Node, travel_matrix: list[list[int]]) -> dict:
    # 建立所有節點的唯一 ID 並排序（穩定映射）
    unique_ids = sorted({node.id for pair in node_pairs for node in pair})
    id_to_index = {nid: i for i, nid in enumerate(unique_ids)}

    # 將每一對 node_pairs 映射成 index（用於 OR-Tools）
    pickup_delivery_index_pairs = [
        [id_to_index[pair[0].id], id_to_index[pair[1].id]] for pair in node_pairs
    ]

    return {
        "distance_matrix": travel_matrix,
        "pickup_delivery_index_pairs": pickup_delivery_index_pairs,
        "depot_index": len(unique_ids),
        "id_to_index": id_to_index,
        "index_to_id": {v: k for k, v in id_to_index.items()},
        "node_ids": unique_ids,
        "num_vehicles": 1,
        "node_warehouse": node_warehouse,
    }


def extract_solution(data: dict, manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, solution):
    """
    解析 OR-Tools 求解結果，轉換為：
    - 節點 index 路線
    - 節點 ID 路線
    - 總距離
    - 目標值（用於分析）
    """
    route_index = []
    route_ids = []
    distance = 0

    index = routing.Start(0)
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route_index.append(node_index)

        if node_index < len(data["node_ids"]):
            route_ids.append(data["index_to_id"][node_index])
        else:
            route_ids.append(data["node_warehouse"].id)  # depot 虛擬 ID

        next_index = solution.Value(routing.NextVar(index))
        distance += routing.GetArcCostForVehicle(index, next_index, 0)
        index = next_index

    # 最後的 depot
    node_index = manager.IndexToNode(index)
    route_index.append(node_index)
    route_ids.append(data["node_warehouse"].id)

    return {
        "objective": solution.ObjectiveValue(),
        "distance": [distance],
        "route_map_index": [route_index],
        "route_map_ID": [route_ids],
    }


def solve_PnD_problem(node_pairs: list[list[Node]], node_warehouse: Node, travel_matrix: list[list[int]]) -> dict | None:

    data = create_data_model(node_pairs, node_warehouse, travel_matrix)

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot_index"]
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_cb_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

    routing.AddDimension(
        transit_cb_index,
        0,          # slack
        8000,       # max distance
        True,       # start at zero
        "Distance"
    )
    distance_dim = routing.GetDimensionOrDie("Distance")
    distance_dim.SetGlobalSpanCostCoefficient(100)

    for pickup_index, delivery_index in data["pickup_delivery_index_pairs"]:
        pickup_idx = manager.NodeToIndex(pickup_index)
        delivery_idx = manager.NodeToIndex(delivery_index)

        routing.AddPickupAndDelivery(pickup_idx, delivery_idx)
        routing.solver().Add(routing.VehicleVar(pickup_idx) == routing.VehicleVar(delivery_idx))
        routing.solver().Add(distance_dim.CumulVar(pickup_idx) <= distance_dim.CumulVar(delivery_idx))

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

    solution = routing.SolveWithParameters(search_params)

    if solution:
        return extract_solution(data, manager, routing, solution)
    else:
        print("NO SOLUTION")
        return None
