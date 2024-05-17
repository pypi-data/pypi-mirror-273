from .base_dictable import BaseDictable
from .utils import open_file, save_file
from .node import Node
from .edge import Edge
from .options import Options
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import List, Dict

class Network(BaseDictable):
    """
    Network is a visualization to display networks consisting of nodes and edges. 
    The visualization is easy to use and supports custom shapes, styles, colors, sizes, images, and more. 
    The network visualization works smooth on any modern browser for up to a few thousand nodes and edges. 
    Network uses HTML canvas for rendering.
    """
    def __init__(self, name="Network", nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        only_use_data_attr = lambda attr: attr == "_data"
        super().__init__(attr_filter_func=only_use_data_attr)
        self.name = name
        self._initialize_data(nodes, edges, options)
        self.env = Environment(
            loader=PackageLoader("pyvisjs"),
            autoescape=select_autoescape()
        )

    @property
    def options(self) -> Options:
        opt = self._data["options"]   
        return opt if isinstance(opt, Options) else None
    
    @options.setter
    def options(self, val:Options):
        self._data["options"] = val
    
    @property
    def nodes(self) -> List[Node]: 
        return self._data["nodes"]  
    
    @property
    def edges(self) -> List[Edge]: 
        return self._data["edges"]  

    def _initialize_data(self, nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        default_data = {"nodes": [], "edges": [], "options": {}}

        if nodes:
            default_data.update({
                "nodes": nodes,
            })

        if edges:
            default_data.update({
                "edges": edges,
            })

        if options:
            default_data.update({
                "options": options,
            })

        self._data = default_data

    def __repr__(self):
        return f"Network(\'{self.name}\')"
    
    def add_node(self, node_id:str, label=None, color=None, shape="dot", size=None, cid=None, **kwargs):
        """
        Creates a Node with node_id and adds it to the nodes list. 
        Wont add node if the nodes list alredy contains a node with the same node_id.

        Parameters
        ----------
        node_id: str, default undefined
            The id of the node. The id is mandatory for nodes and they have to be unique. 
            Will be used as a node reference in edges

        label: str, default undefined
            Will be replaced with `str(node_id)` if undefined. 
            The label is the piece of text shown in or under the node, depending on the shape.
        
        color: str, default undefined, but if undefined, `'#97C2FC'` will be used by vis.js
            Could be value like `'#ffffff'` or `'red'`
        
        **kwargs: dict, optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        if not [node.id for node in self.nodes if node.id == str(node_id)]:
            self.nodes.append(Node(node_id, label, color, shape, size, cid, **kwargs))

    def add_edge(self, from_id:str, to_id:str, **kwargs):
        """Creates an Edge which connects two nodes using from_id and to_id and adds it to the edges list.
        If you provide node ID which is not presented in the nodes list 
        such a node will be automatically created and added to the nodes list.
        
        Parameters
        ----------
        from_id: str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the from node. 
            You have to supply the corresponding node ID.
        
        to_id: str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the to node. 
            You have to supply the corresponding node ID.

        **kwargs: dist, Optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        self.add_node(from_id)
        self.add_node(to_id)

        if not [edge.start for edge in self.edges if edge.start == str(from_id) and edge.end == str(to_id)]:
            self.edges.append(Edge(from_id, to_id, **kwargs))

    def to_dict(self):
        return super().to_dict()["_data"]

    def show(self, file_name):
        self.render_default_template(open_in_browser=True, output_filename=file_name)

    def _render(self, template_filename:str, open_in_browser=False, save_to_output=False, output_filename="default.html", pyvisjs_options:Dict=None):
        network_dict = self.to_dict()

        html_output = self.env \
            .get_template(template_filename) \
            .render(
                width=network_dict["options"].get("width", "100%"),
                height=network_dict["options"].get("height", "100%"),
                data=network_dict,
                pyvisjs=pyvisjs_options or {},
            )

        if save_to_output or open_in_browser:
            file_path = save_file(output_filename, html_output)

        if open_in_browser:
            open_file(file_path)

        return html_output
    
    def render_default_template(self, open_in_browser=False, save_to_output=False, output_filename="default.html"):
        return self._render(
            template_filename="basic.html",
            open_in_browser=open_in_browser,
            save_to_output=save_to_output,
            output_filename=output_filename)
    

    def render_tom_template(self, title:str=None, open_in_browser=False, save_to_output=False, output_filename="default.html", 
    enable_highlighting=False, edge_filtering=None, node_filtering=None) -> str:
        """This method uses jinja to inject prepared data to `'templates\\tom-select.html'` \n
        (for more info about the injected data see Notes section below).
        
        Parameters
        ----------
        open_in_browser: bool, default=False
            Resolved template will be saved as the `output_filename` and opened with `os.startfile`

        save_to_output: bool, default=False
            Resolved template will be just saved (not opened) as the `output_filename`

        output_filename: str, default=".\\default.html"
            Can be just a file name or have relative or absolute path

        enable_highlighting: bool, default=False
            - `true` - turns highlighting mode on, which means filtering in the tom-select control will highlight a part of the network - not hide it
            - `false` - turns highlighting mode off, which means filtering in the tom-select control will hide a part of the network - not highlight it
            This setting is not a standard vis.js option and injects to the template as the `enable_highlighting` key of the `pyvisjs` dict
        
        edge_filtering: str or list, default=None
            Enables edges filtering using predefined or dynamic edge attributes which means hiding all edges which do not satisfy filtering condition
            So for example you can:
            add a dynamic attribute "size" with 3 possible values ['S', 'M', 'L'] to the edges and 
            pass `edge_filtering="size"` to the `render_tom_template` method
            expecting resolved template to have `<select>` element with S/M/L options lookup
            which will filter all nodes connected with edges having selected option
            see example on `gitlab.com/22kittens/pyvisjs/examples/bluor.py`

        node_filtering: str or list, default=None
            Enables nodes filtering using predefined or dynamic node attributes which means hiding all nodes which do not satisfy filtering condition
            So for example you can:
            add a dynamic attribute "size" with 3 possible values ['S', 'M', 'L'] to the nodes and 
            pass `node_filtering="size"` to the `render_tom_template` method
            expecting resolved template to have `<select>` element with S/M/L options lookup
            which will filter all nodes having selected option
            see example on `gitlab.com/22kittens/pyvisjs/examples/bluor.py`

        Notes
        -----
        The data injected will be:

        >>> .render(
        >>>     width=network_dict["options"].get("width", "100%"),
        >>>     height=network_dict["options"].get("height", "100%"),
        >>>     data=network_dict,
        >>>     pyvisjs={
        >>>         "enable_highlighting": enable_highlighting,
        >>>         "edge_filtering_lookup": edge_filtering_lookup,
        >>>         "node_filtering_lookup": node_filtering_lookup,
        >>>     },
        >>> )

        you can find more details about `edge_filtering_lookup` and `node_filtering_lookup` structure here `tests\\test_network.py\\test_network_render_template_edge_filtering_list`
        """

        edge_filtering_lookup: Dict = None
        node_filtering_lookup: Dict = None

        # edges
        if not edge_filtering is None:
            if not isinstance(edge_filtering, list):
                edge_filtering = [str(edge_filtering)]

            edge_filtering_lookup = {}
            for field_name in edge_filtering:
                tp_field_name = Edge.convert_to_template_attribute(field_name)
                unique_values = list(set([str(getattr(edge, field_name)) for edge in self.edges if hasattr(edge, field_name)]))
                unique_values.sort()
                edge_filtering_lookup[tp_field_name] = unique_values

        # nodes
        if not node_filtering is None:
            if not isinstance(node_filtering, list):
                node_filtering = [str(node_filtering)]

            node_filtering_lookup = {}
            for field_name in node_filtering:
                unique_values = list(set([str(getattr(node, field_name)) for node in self.nodes if hasattr(node, field_name)]))
                unique_values.sort()
                node_filtering_lookup[field_name] = unique_values             
        
        pyvisjs_options = {
                    "enable_highlighting": enable_highlighting,
                    "edge_filtering_lookup": edge_filtering_lookup,
                    "node_filtering_lookup": node_filtering_lookup,
                    "title": title,
                };
         
        return self._render(
            template_filename="tom-select.html",
            open_in_browser=open_in_browser,
            save_to_output=save_to_output,
            output_filename=output_filename,
            pyvisjs_options=pyvisjs_options)
        
