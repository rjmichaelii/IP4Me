import helpers.node_functions as node_functions

IP = 'localhost'
PORT = 20000


Nodes = {
    "Node1": (IP, PORT + 1),
    "Node2": (IP, PORT + 2),
    "Node3": (IP, PORT + 3),
    "Node4": (IP, PORT + 4),
}

#   Node Diagram
#      Node 1
#    /       \
# Node 2    Node 3
#    \       /
#      Node 4

Connections = {
    "Node1": ["Node2", "Node3"],
    "Node2": ["Node1", "Node4"],
    "Node3": ["Node1", "Node4"],
    "Node4": ["Node2", "Node3"]
}

functions = {
    "Node1": node_functions.Node1,
    "Node2": node_functions.Node2,
    "Node3": node_functions.Node3,
    "Node4": node_functions.Node4
}

routing = {
    "Node1": {
        "Node1": "Node1",
        "Node2": "Node2",
        "Node3": "Node3",
        "Node4": "Node3"
    },
    "Node2": {
        "Node1": "Node1",
        "Node2": "Node2",
        "Node3": "Node4",
        "Node4": "Node4"
    },
    "Node3": {
        "Node1": "Node4",
        "Node2": "Node4",
        "Node3": "Node3",
        "Node4": "Node4"
    },
    "Node4": {
        "Node1": "Node2",
        "Node2": "Node2",
        "Node3": "Node3",
        "Node4": "Node4"
    }
}
