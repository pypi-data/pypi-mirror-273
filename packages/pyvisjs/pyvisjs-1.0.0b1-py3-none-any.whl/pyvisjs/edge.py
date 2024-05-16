from .base_dictable import BaseDictable

class Edge(BaseDictable):
    """Handles the creation and deletion of edges and contains the global edge options and styles.
    
    Notes
    -----
    Original vis.js Node has `from` and `to` attributes for the linked Node ids.
    We can't use `from` as an attribute in python because it is a reserved keyword,
    so we use `start` and `end` attributes insted AND(!) some mapping to change 
    attribute names before injecting them to html templates
    """

    _attributes_mapping = {
        "start": "from",
        "end": "to"
    }

    @classmethod
    def convert_to_template_attribute(cls, attr):
        return cls._attributes_mapping.get(attr, attr)

    def __init__(self, start:str, end:str, **kwargs):
        convert_to_template_attribute = lambda attr: Edge.convert_to_template_attribute(attr)
        is_not_attributes_mapping = lambda attr: attr != "_attributes_mapping"
        super().__init__(attr_map_func = convert_to_template_attribute, attr_filter_func=is_not_attributes_mapping)
        self.start = str(start)
        self.end = str(end)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Edge(\'{self.start}\', \'{self.end}\')"