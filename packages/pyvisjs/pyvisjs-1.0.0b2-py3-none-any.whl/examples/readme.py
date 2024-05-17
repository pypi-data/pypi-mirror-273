"""
    git clone https://gitlab.com/22kittens/pyvisjs.git
    cd pyvisjs
    git checkout dev
    py -m venv .venv
    .venv\\Scripts\\activate
    py -m pip install -r requirements.txt
    py -m pip install -e .
    py .\\examples\\readme.py
"""

from pyvisjs import Network

# Create a Network instance
net = Network()

# Add nodes and edges
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)
net.add_edge(2, 3)
net.add_edge(3, 1)

# Display the network
net.show("example.html")