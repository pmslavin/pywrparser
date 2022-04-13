import json

#from pywrparser.types import PywrNetwork
from pywrparser.types import PywrParameter, PywrRecorder

class PywrJSONEncoder(json.JSONEncoder):
    def default(self, inst):
        if isinstance(inst, (PywrParameter, PywrRecorder)):
            return inst.data

        return json.JSONEncoder.default(self, inst)
