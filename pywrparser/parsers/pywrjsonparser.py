import json
import re
from collections import defaultdict

from pywrparser.types import (
    PywrTimestepper,
    PywrMetadata,
    PywrScenario,
    PywrTable,
    PywrNode,
    PywrEdge,
    PywrParameter,
    PywrRecorder,
)

from pywrparser.types.exceptions import (
    PywrTypeValidationError,
    PywrNetworkValidationError
)

from pywrparser.utils import raiseorpush

DUP_KEY_BASE = "__PywrParser_Duplicate_Key_{pattern}__"
DUP_KEY_FLAG = DUP_KEY_BASE.format(pattern="{idx:03d}")
DUP_KEY_RE   = r"{base}".format(base=DUP_KEY_BASE.format(pattern="[0-9]{3}"))


class PywrJSONParser():
    def __init__(self, json_src):
        self.errors = defaultdict(list)
        self.src = json.loads(json_src, object_pairs_hook=self.__class__.enforce_unique)

        self.nodes = {}
        self.edges = []
        self.parameters = {}
        self.recorders = {}
        self.scenarios = []
        self.tables = {}


    @staticmethod
    def enforce_unique(ordered_pairs):
        d = {}
        sep = ':'
        idx = 1
        for k, v in ordered_pairs:
            if k in d:
                key = DUP_KEY_FLAG.format(idx=idx) + sep + k
                d[key] = v
                idx += 1
            else:
                d[k] = v
        return d


    def parse(self, raise_on_error=False):
        seen_nodes = set()

        with raiseorpush("metadata", raise_on_error, self.errors):
            self.metadata = PywrMetadata(self.src["metadata"])

        with raiseorpush("timestepper", raise_on_error, self.errors):
            self.timestepper = PywrTimestepper(self.src["timestepper"])

        for scenario in self.src.get("scenarios",[]):
            with raiseorpush("scenarios", raise_on_error, self.errors):
                scen = PywrScenario(scenario)
                self.scenarios.append(scen)

        for table_name, table_data in self.src.get("tables", {}).items():
            with raiseorpush("tables", raise_on_error, self.errors):
                t = PywrTable(table_name, table_data)
                self.tables[t.name] = t

        for param_name, param_data in self.src.get("parameters",{}).items():
            if m := re.search(DUP_KEY_RE, param_name):
                span_end = m.span()[1]
                raw_name = param_name[span_end+1:]
                self.errors["network"].append(PywrNetworkValidationError(f"Duplicate parameter name <{raw_name}>"))
            with raiseorpush("parameters", raise_on_error, self.errors):
                p = PywrParameter(param_name, param_data)
                self.parameters[p.name] = p

        for rec_name, rec_data in self.src.get("recorders",{}).items():
            if m := re.search(DUP_KEY_RE, rec_name):
                span_end = m.span()[1]
                raw_name = rec_name[span_end+1:]
                self.errors["network"].append(PywrNetworkValidationError(f"Duplicate recorder name <{raw_name}>"))
            with raiseorpush("recorders", raise_on_error, self.errors):
                r = PywrRecorder(rec_name, rec_data)
                self.recorders[r.name] = r

        for node in self.src["nodes"]:
            with raiseorpush("nodes", raise_on_error, self.errors):
                n = PywrNode(node)
                if n.name in seen_nodes:
                    self.errors["network"].append(PywrNetworkValidationError(f"Duplicate node name <{n.name}>"))
                else:
                    self.nodes[n.name] = n
                    seen_nodes.add(n.name)

        for edge in self.src["edges"]:
            with raiseorpush("edges", raise_on_error, self.errors):
                e = PywrEdge(edge)
                self.edges.append(e)

    @property
    def has_errors(self):
        return len(self.errors) > 0
