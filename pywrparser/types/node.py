import copy

from .base import PywrType


class PywrNode(PywrType):
    def __init__(self, data):
        name = data.get("name")
        if not isinstance(name, str):
            if not name:
                # Unnamed node - will fail validation
                pass
            else:
                # Other non-str name, cast to str
                name = str(name)
                data["name"] = name
        self.data = data


    @property
    def type(self):
        return self.data.get("type")


    @property
    def name(self):
        return self.data.get("name")


    @property
    def attrs(self):
        return self.data.keys()


    def as_dict(self):
        ret = copy.deepcopy(self.data)

        for k,v in ret.items():
            if isinstance(v, PywrType):
                ret[k] = v.as_dict()


    """ Validation rules """

    def rule_node_has_name(self):
        assert self.name is not None, "Missing node name"

    def rule_node_has_type(self):
        assert "type" in self.data, "Node does not define type"

    def rule_node_name_min_len(self):
        assert self.name and len(self.name) > 1, "Node name too short"
