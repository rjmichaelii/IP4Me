import subprocess

PORT = 20000

Nodes = {
    "Node1" : PORT + 1,
    "Node2" : PORT + 2,
    "Node3" : PORT + 3,
    "Node4" : PORT + 4,
}

#   Node Diagram
#      Node 1
#    /       \
# Node 2    Node 3
#    \       /
#      Node 4
Connections = {
    "Node1" : ["Node2", "Node3"],
    "Node2" : ["Node1", "Node4"],
    "Node3" : ["Node1", "Node4"],
    "Node4" : ["Node2", "Node3"]
}

if __name__ == "__main__":
    for node, port in Nodes.items():
        args = 'start python node.py ' + "localhost " + str(port) + " " + node
        for value in Connections.get(node):
            args += " localhost " + str(Nodes.get(value)) + " " + value
        print(args)
        subprocess.run(args, shell=True)
        

