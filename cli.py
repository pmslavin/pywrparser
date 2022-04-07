import sys
import pprint

from pywrparser.parsers import PywrJSONParser
from pywrparser.types import PywrNetwork

if __name__ == "__main__":
    filename = sys.argv[-1]
    parser = PywrJSONParser(filename)
    parser.parse(raise_on_error=False)
    if not parser.has_errors:
        network = PywrNetwork(parser)
        #pprint.pprint(network.as_dict())
        #print("==: End of network.as_dict() :==")
        #pprint.pprint(network.parameters)
        print(len(network.parameters))
        print("="*46)
        network.attach_parameters()
        #pprint.pprint(network.parameters)
        print(len(network.parameters))
        print("="*46)
        for n in network.nodes.values():
            for attr, value in n.data.items():
                if isinstance(value, dict) and "type" in value:
                    print(f"Inline parameter: __{n.name}__:{attr}")
        network.detach_parameters()
        #pprint.pprint(network.parameters)
        print(len(network.parameters))
        print("="*46)
        network.attach_parameters()
        #pprint.pprint(network.parameters)
        print(len(network.parameters))
        print("="*46)
        #breakpoint()
    else:
        errors = [(component,errs) for component,errs in parser.errors.items()]
        pprint.pprint(errors)
        #pprint.pprint(parser.src["parameters"])
    #breakpoint()
    #pprint.pprint(network.as_dict())
    #print(network.as_json())
