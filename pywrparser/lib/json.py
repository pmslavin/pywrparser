import json

from pywrparser.types import PywrNetwork

class PywrJSONEncoder(json.JSONEncoder):
    def default(self, inst):
        if isinstance(inst, PywrNetwork):
            return inst.as_dict

        return json.JSONEncoder.default(self, inst)
