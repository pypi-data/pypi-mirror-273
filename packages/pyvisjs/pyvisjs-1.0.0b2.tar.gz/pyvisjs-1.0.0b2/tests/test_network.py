import pytest
from unittest.mock import patch
from pyvisjs import Network, Node, Edge, Options

def test_network_init():
    # init
    DEFAULT_DICT = {
        "nodes": [],
        "edges": [],
        "options": {}
    }
    # mock


    # call
    n = Network("Network2")
    
    # assert
    assert n.name == "Network2"
    assert n.env is not None
    assert n.to_dict() == DEFAULT_DICT

def test_network_init_with_data():
    # init
    NETWORK_DICT = {
        "nodes": [
            { "id": "1", "label": "node 1", "shape": "dot" },
            { "id": "2", "label": "node 2", "shape": "dot" },
            { "id": "3", "label": "node 3", "shape": "dot" },
        ],
        "edges": [
            { "from": "1", "to": "2" },
            { "from": "2", "to": "3" },
            { "from": "3", "to": "4" }
        ],
        "options": {}
    }
    # mock


    # call
    nd1 = Node(1, "node 1")
    nd2 = Node(2, "node 2")
    nd3 = Node(3, "node 3")

    eg1 = Edge(1, 2)
    eg2 = Edge(2, 3)
    eg3 = Edge(3, 4)

    opt = Options()

    n = Network("Network2", [nd1, nd2, nd3], [eg1, eg2, eg3], opt)
    
    # assert
    assert n.name == "Network2"
    assert n.env is not None
    assert n.to_dict() == NETWORK_DICT

def test_network_read_write_properties():
    # init

    # mock

    # call
    nd1 = Node(1, "node 1")
    nd2 = Node(2, "node 2")
    nd3 = Node(3, "node 3")

    eg1 = Edge(1, 2)
    eg2 = Edge(2, 3)
    eg3 = Edge(3, 4)

    opt = Options()

    n = Network("Network2", [nd1, nd2], [eg1])
    n.options = opt
    n.nodes.append(nd3)
    n.edges.append(eg2)
    n.edges.append(eg3)

    # assert
    assert n.options == opt
    assert n.nodes == [nd1, nd2, nd3]
    assert n.edges == [eg1, eg2, eg3]


def test_network_add_nodes():
    # init

    # mock

    # call
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")
    n.add_node(2) # duplicate node
    n.add_node(3, "hello", "red", "circle", None, None, category="high")
    
    # assert
    assert len(n.nodes) == 3
    assert n.nodes[0].id == "1"
    assert n.nodes[0].label == "1"
    assert n.nodes[1].id == "2"
    assert n.nodes[1].label == "name2"
    assert n.nodes[2].category == "high"

def test_network_add_edges():
    # init

    # mock

    # call
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")
    n.add_edge(1, 2) # both nodes exist
    n.add_edge(2, 3, country="LV") # one node missing
    n.add_edge(2, 3) # duplicate edge
    
    # assert
    assert n.nodes[0].id == "1"
    assert n.nodes[1].id == "2"
    assert n.nodes[2].id == "3"

    assert len(n.edges) == 2
    assert n.edges[0].start == "1"
    assert n.edges[0].end == "2"
    assert n.edges[1].start == "2"
    assert n.edges[1].end == "3"
    assert n.edges[1].country == "LV"

def test_network_to_dict():
    # init
    NETWORK_DICT = {
        "nodes": [
            { "id": "1", "label": "1", "shape": "dot" },
            { "id": "2", "label": "name2", "shape": "dot" },
            { "id": "3", "label": "3", "shape": "dot" },
        ],
        "edges": [
            { "from": "1", "to": "2" },
            { "from": "2", "to": "3" }
        ],
        "options": {}
    }

    # mock

    # call
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")
    n.add_edge(1, 2) # both nodes exist
    n.add_edge(2, 3) # one node missing
    n.add_edge(2, 3) # duplicate edge
    
    # assert
    assert n.to_dict() == NETWORK_DICT

@patch('pyvisjs.network.Environment')
def test_network_render_tom_template_passing_render_default_params(mock_Environment):
    # init
    WIDTH="100%"
    HEIGHT="100%"
    DATA={"nodes": [], "edges": [], "options": {}}
    PYVISJS={
        "enable_highlighting": False,
        "edge_filtering_lookup": None,
        "node_filtering_lookup": None,
        "title": None,
    }
    
    # mock
    mock_render = mock_Environment.return_value.get_template.return_value.render

    # call
    network = Network("Test Network")
    html_output = network.render_tom_template() # <--------------------

    # assert
    mock_render.assert_called_once_with(width=WIDTH, height=HEIGHT, data=DATA, pyvisjs=PYVISJS)

@patch('pyvisjs.network.Environment')
def test_network_render_tom_template_passing_render_params(mock_Environment):
    # init
    WIDTH="100%"
    HEIGHT="100%"
    DATA={"nodes": [], "edges": [], "options": {}}
    TEMPLATE_FILENAME="tom-select.html"
    ENABLE_HIGHLIGHTING=True
    EDGE_FILTERING="edge_field" # str(!) not list
    NODE_FILTERING=["field1", "field2"] # list
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "edge_filtering_lookup": {"edge_field": []},
        "node_filtering_lookup": {"field1": [], "field2": []},
        "title": None,
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    network = Network("Test Network")
    html_output = network.render_tom_template( # <--------------------
        enable_highlighting=ENABLE_HIGHLIGHTING, 
        edge_filtering=EDGE_FILTERING, 
        node_filtering=NODE_FILTERING)

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(width=WIDTH, height=HEIGHT, data=DATA, pyvisjs=PYVISJS)

@patch('pyvisjs.network.Environment')
def test_network_render_tom_template_edge_filtering_list(mock_Environment):
    # init
    WIDTH="100%"
    HEIGHT="100%"
    DATA={
        'nodes': [
            {'id': '1', 'label': '1', 'shape': 'dot'}, 
            {'id': '2', 'label': '2', 'shape': 'dot'}, 
            {'id': '3', 'label': '3', 'shape': 'dot'}], 
        'edges': [
            {'to': '2', 'field1': 'AM', 'from': '1'}, 
            {'to': '3', 'field1': 'AM', 'from': '1'}, 
            {'to': '3', 'field1': 'JL', 'from': '2'}], 
        'options': {}
    }
    TEMPLATE_FILENAME="tom-select.html"
    ENABLE_HIGHLIGHTING=True
    EDGE_FILTERING=["field1", "field2"]
    NODE_FILTERING=["label", "shape"]
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "edge_filtering_lookup": {"field1": ["AM", "JL"], "field2": []},
        "node_filtering_lookup": {"label": ["1", "2", "3"], "shape": ["dot"]},
        "title": None,
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network("Network1")
    net.add_edge(1, 2, field1="AM")
    net.add_edge(1, 3, field1="AM")
    net.add_edge(2, 3, field1="JL")
    html_output = net.render_tom_template( # <--------------------
        enable_highlighting=ENABLE_HIGHLIGHTING, 
        edge_filtering=EDGE_FILTERING,
        node_filtering=NODE_FILTERING) 

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(width=WIDTH, height=HEIGHT, data=DATA, pyvisjs=PYVISJS)

@patch('pyvisjs.network.Environment')
def test_network_render_tom_template_edge_filtering_int(mock_Environment):
    # init
    WIDTH="100%"
    HEIGHT="100%"
    DATA={"nodes": [], "edges": [], "options": {}}
    TEMPLATE_FILENAME="tom-select.html"
    ENABLE_HIGHLIGHTING=True
    EDGE_FILTERING=34
    NODE_FILTERING=22
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "edge_filtering_lookup": {"34": []},
        "node_filtering_lookup": {"22": []},
        "title": None,
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network("Network1")
    html_output = net.render_tom_template(# <--------------------
        enable_highlighting=ENABLE_HIGHLIGHTING, 
        edge_filtering=EDGE_FILTERING,
        node_filtering=NODE_FILTERING) 

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(width=WIDTH, height=HEIGHT, data=DATA, pyvisjs=PYVISJS)

@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_default_template_with_all_default_values(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    DEFAULT_TEMPLATE_FILENAME = "basic.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network.render_default_template() # <--------------------

    # assert
    mock_get_template.assert_called_once_with(DEFAULT_TEMPLATE_FILENAME)
    mock_save_file.assert_not_called()
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_open_in_browser(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "some-template-name.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = DEFAULT_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network._render(TEMPLATE_FILENAME, open_in_browser=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_save_to_output(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "template-1.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network._render(TEMPLATE_FILENAME, save_to_output=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_open_and_save_no_defaults(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "custom_template.html"
    CUSTOM_OUTPUT_FILENAME = "custom_output.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = CUSTOM_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network._render( # <--------------------
        TEMPLATE_FILENAME,
        open_in_browser=True, 
        save_to_output=True, 
        output_filename=CUSTOM_OUTPUT_FILENAME)

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT