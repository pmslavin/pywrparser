from .base import PywrType

from pywrparser.parsers import PywrJSONParser

from pywrparser.types import (
    PywrParameter,
    PywrRecorder
)

from pywrparser.utils import canonical_name


class PywrNetwork(PywrType):

    def __init__(self, parser):
        self.metadata = parser.metadata
        self.timestepper = parser.timestepper
        self.scenarios = parser.scenarios
        self.tables = parser.tables
        self.nodes = parser.nodes
        self.links = parser.edges
        self.parameters = parser.parameters
        self.recorders = parser.recorders

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as fp:
            src = fp.read()
        parser = PywrJSONParser(src)
        parser.parse(raise_on_error=False)
        if parser.has_errors:
            return None, parser.errors

        return cls(parser), None

    @classmethod
    def from_json(cls, json_src):
        parser = PywrJSONParser(json_src)
        parser.parse(raise_on_error=False)
        return cls(parser)

    @classmethod
    def from_hydra(cls, hydra_src):
        pass


    def as_dict(self):
        network = {
            "metadata": self.metadata.as_dict(),
            "timestepper": self.timestepper.as_dict(),
            "nodes": [ node.as_dict() for node in self.nodes.values() ],
            "links": [ link.as_dict() for link in self.links ]
        }
        if len(self.parameters) > 0:
            network["parameters"] = {n: p.as_dict() for n,p in self.parameters.items()}

        if len(self.recorders) > 0:
            network["recorders"] = {n: r.as_dict() for n,r in self.recorders.items()}

        if len(self.scenarios) > 0:
            network["scenarios"] = [ s.as_dict() for s in self.scenarios ]

        if len(self.tables) > 0:
            network["tables"] = {n: t.as_dict() for n,t in self.tables.items()}

        return network

    def as_json(self):
        import json
        return json.dumps(self.as_dict(), indent=2)


    def validate(self):
        pass

    def attach_parameters(self):
        """
            1. Any values of attrs in a node which resolve to a global
               parameter are replaced with the instance of that parameter
               and the parameter is removed from the set of global parameters.

            2. Any values of attrs in a node which can be interpreted as
               an inline (i.e. dict) parameter definition are instantiated
               as parameters and the attr value replaced with the instance.
        """
        for node in self.nodes.values():
            for attr, value in node.data.items():
                if isinstance(value, str):
                    param = self.parameters.get(value)
                    if not param:
                        continue
                    print(f"Attaching global param ref: {value}")
                    node.data[attr] = param
                    del self.parameters[value]
                elif isinstance(value, dict):
                    type_key = value.get("type")
                    if not type_key or "recorder" in type_key.lower():
                        continue
                    param_name = canonical_name(node.name, attr)
                    print(f"Creating inline param: {param_name}")
                    if param_name in self.parameters:
                        # Node inline param has same name as global param
                        raise ValueError("inline dups global param")
                    param = PywrParameter(param_name, value)
                    node.data["attr"] = param


    def detach_parameters(self):
        for node in self.nodes.values():
            for attr, value in node.data.items():
                if isinstance(value, PywrParameter):
                    if value.name in self.parameters:
                        # Attr param name duplicates global param name
                        raise ValueError("Attr param name duplicates global param name")
                    self.parameters[value.name] = value
                    node.data[attr] = value.name
