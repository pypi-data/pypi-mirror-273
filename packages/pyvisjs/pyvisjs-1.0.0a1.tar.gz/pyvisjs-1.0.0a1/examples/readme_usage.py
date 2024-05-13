from pyvisjs import Network, Options

# Create a Network instance
net = Network()

# Add nodes and edges
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)
net.add_edge(2, 3)
net.add_edge(3, 1)

# Display the network
net.show("example.html", enable_highlighting=True, edge_filtering="end")