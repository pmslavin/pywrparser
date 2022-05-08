import json
import re
from collections import (
    defaultdict,
    Counter
)
from functools import partial

from pywrparser import rules

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
    PywrParserException,
    PywrTypeValidationError,
    PywrNetworkValidationError
)

from pywrparser.utils import raiseorpush

DUP_KEY_BASE = "__PywrParser_Duplicate_Key_{pattern}__"
DUP_KEY_FLAG = DUP_KEY_BASE.format(pattern="{idx:03d}")
DUP_KEY_RE   = r"{base}".format(base=DUP_KEY_BASE.format(pattern="[0-9]{3}"))


class PywrJSONParser():
    def __init__(self, json_src, ruleset=None):
        """
        Creates an instance of a parser in which the specified `json_src` is
        validated against the specified `ruleset`.

        Args:
            json_src (str): A JSON encoded representation of a Pywr network
            ruleset (str): The key of a ruleset whose rules are to be applied
        """
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)

        if ruleset:
            self.set_parser_ruleset(ruleset)

        try:
            self.src = json.loads(json_src, object_pairs_hook=self.__class__.enforce_unique)
        except json.decoder.JSONDecodeError as err:
            raise PywrParserException(f"Invalid JSON document: {str(err)}")

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

    def set_parser_ruleset(self, ruleset):
        rulesets = rules.get_rulesets()
        if not ruleset in rulesets:
            raise PywrParserException(f"No ruleset with key: {ruleset}")

        import importlib
        import pywrparser.types
        rules.set_active_ruleset(ruleset)
        importlib.reload(pywrparser.types)
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
        globals()["PywrTimestepper"] = PywrTimestepper
        globals()["PywrMetadata"] = PywrMetadata
        globals()["PywrScenario"] = PywrScenario
        globals()["PywrTable"] = PywrTable
        globals()["PywrNode"] = PywrNode
        globals()["PywrEdge"] = PywrEdge
        globals()["PywrParameter"] = PywrParameter
        globals()["PywrRecorder"] = PywrRecorder



    def parse(self, raise_on_error=False, raise_on_warning=False, allow_duplicate_edges=True):
        seen_nodes = set()

        """
        Only component varies between invocations, create partial
        for fixed arguments to context manager.
        """
        component_exc_capture = partial(raiseorpush,
                                  raise_error=raise_on_error,
                                  raise_warning=raise_on_warning,
                                  dest=self)

        with component_exc_capture("metadata"):
            self.metadata = PywrMetadata(self.src["metadata"])

        with component_exc_capture("timestepper"):
            self.timestepper = PywrTimestepper(self.src["timestepper"])

        for scenario in self.src.get("scenarios",[]):
            with component_exc_capture("scenarios"):
                scen = PywrScenario(scenario)
                self.scenarios.append(scen)

        for table_name, table_data in self.src.get("tables", {}).items():
            with component_exc_capture("tables"):
                t = PywrTable(table_name, table_data)
                self.tables[t.name] = t

        for param_name, param_data in self.src.get("parameters",{}).items():
            if m := re.search(DUP_KEY_RE, param_name):
                span_end = m.span()[1]
                raw_name = param_name[span_end+1:]
                self.errors["network"].append(PywrNetworkValidationError(f"Duplicate parameter name <{raw_name}>"))
            with component_exc_capture("parameters"):
                p = PywrParameter(param_name, param_data)
                self.parameters[p.name] = p

        for rec_name, rec_data in self.src.get("recorders",{}).items():
            if m := re.search(DUP_KEY_RE, rec_name):
                span_end = m.span()[1]
                raw_name = rec_name[span_end+1:]
                self.errors["network"].append(PywrNetworkValidationError(f"Duplicate recorder name <{raw_name}>"))
            with component_exc_capture("recorders"):
                r = PywrRecorder(rec_name, rec_data)
                self.recorders[r.name] = r

        for node in self.src["nodes"]:
            with component_exc_capture("nodes"):
                n = PywrNode(node)
                if n.name in seen_nodes:
                    self.errors["network"].append(PywrNetworkValidationError(f"Duplicate node name <{n.name}>"))
                else:
                    self.nodes[n.name] = n
                    seen_nodes.add(n.name)

        for edge in self.src["edges"]:
            with component_exc_capture("edges"):
                e = PywrEdge(edge)
                self.edges.append(e)

        if not allow_duplicate_edges and self.has_duplicate_edges:
            for edge in self.duplicate_edges:
                self.errors["network"].append(PywrNetworkValidationError(f"Duplicate edge <{edge}>"))


    @property
    def has_errors(self):
        return len(self.errors) > 0


    @property
    def has_warnings(self):
        return len(self.warnings) > 0

    @property
    def has_duplicate_edges(self):
        return len(self.duplicate_edges) > 0

    @property
    def duplicate_edges(self):
        """
        Return a dict of "duplicate" edges, that is edges of length `n`
        comprised of the same `n` nodes in the same order which are
        defined more than once.
        This is permitted by Pywr but may indicate a malformed network
        in some enviroments.
        """
        edge_count = Counter((n1, n2) for (n1, n2) in self.edges)
        return {edge: count for edge, count in edge_count.items() if count > 1}
