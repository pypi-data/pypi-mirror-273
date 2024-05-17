# pyvisjs: Python Wrapper for vis.js Network

pyvisjs is a Python package designed to provide seamless interaction with [vis.js](https://visjs.org) network visualizations, allowing users to manipulate and visualize network data using Python.

## Workflow

1. Create a network using python
2. Apply standard vis.js options such as colors, shapes or physics
3. Apply pyvisjs specific options such as node/edge filtering or highlighting
4. Show or generate html file
5. Enjoy network interactions in your browser

## Installation

You can install PyVisjs via pip:

```bash
pip install pyvisjs
```

## Usage

```python
from pyvisjs import Network

# Create a Network instance
net = Network()

# Add nodes and edges
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)

# Display the network
net.show("example.html")
```

For more examples and detailed usage, please refer to the [documentation](link_to_docs).

## Contributing

Contributions are welcome! If you have suggestions, feature requests, or find any bugs, please open an issue or submit a pull request. Make sure to follow the [contribution guidelines](CONTRIBUTING.md).

## Acknowledgments

This project is inspired by the [pyvis](https://github.com/WestHealth/pyvis) Python package and the [visNetwork](https://github.com/datastorm-open/visNetwork) R-language package.

## License

This project is licensed under the [MIT License](link_to_license).