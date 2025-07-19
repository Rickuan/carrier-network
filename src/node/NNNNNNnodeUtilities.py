import csv, os, pandas as pd

import node

import dirNavigator

def addWarehouseInfoToCSV(warehouse_x:int, warehouse_y:int) -> None:

    PATH_ORIGINAL_CSV   = os.path.join(dirNavigator.DIR_NODE, 'nodeInfo.csv')
    PATH_UPDATED_CSV    = os.path.join(dirNavigator.DIR_NODE, 'nodeInfoFromGUI.csv')

    df = pd.read_csv(PATH_ORIGINAL_CSV)
    df.loc[len(df)] = ['N99', 'WAREHOUSE', warehouse_x, warehouse_y]
    df.to_csv(PATH_UPDATED_CSV, index=False)
        
def getNumberOfNodes(file_name = 'nodeInfo.csv'):
    PATH_UPDATED_CSV = os.path.join(PATH_INPUT, file_name)
    with open(PATH_UPDATED_CSV) as csv_file:
        return len(list(csv.reader(csv_file)))-1