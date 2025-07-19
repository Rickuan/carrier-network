import os

# project root
DIR_SRC             = os.path.dirname(os.path.abspath(__file__))

# files
DIR_ROUTINGMODEL    = os.path.join(DIR_SRC, "routingModel")
DIR_NODE            = os.path.join(DIR_SRC, "node")
DIR_TRAVELMATRIX    = os.path.join(DIR_NODE, "travelMatrix")
DIR_GUI             = os.path.join(DIR_SRC, "GUI")
DIR_AUCTION         = os.path.join(DIR_SRC, "auction")
DIR_AGENT           = os.path.join(DIR_SRC, "agent")