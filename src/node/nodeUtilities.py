import os, csv

from src.node.node import Node
import src.dirNavigator as dirNavigator

def write_travelMatrix(nodes_involved:list[Node], file_name:str):
    PATH_TO_SAVE = os.path.join(dirNavigator.DIR_TRAVELMATRIX, file_name)
    os.makedirs(os.path.dirname(PATH_TO_SAVE), exist_ok=True)

    with open(PATH_TO_SAVE, 'w', newline='') as csvFile:
        spamwriter = csv.writer(csvFile, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Distance"] + [each.id for each in nodes_involved])

        for every_node in nodes_involved:
            distance:list[int] = []
            for _ in nodes_involved:
                distance.append(every_node.distance_to(_))

            spamwriter.writerow([every_node.id] + distance)