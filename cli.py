import os
import sys
import logging
import pprint

#from pywrparser.parsers import PywrJSONParser
from pywrparser.types.network import PywrNetwork

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)

if __name__ == "__main__":
    filename = sys.argv[-1]
    #parser = PywrJSONParser(filename)
    #parser.parse(raise_on_error=False)

    network, errors = PywrNetwork.from_file(filename, raise_on_parser_error=False)

    if errors:
        for component, errs in errors.items():
            for err in errs:
                print(err)
        exit(1)

    #pprint.pprint(network.as_dict())
    #print("==: End of network.as_dict() :==")
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #network.attach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    for n in network.nodes.values():
        for attr, value in n.data.items():
            if isinstance(value, dict) and "type" in value:
                print(f"Inline parameter: __{n.name}__:{attr}")
    #network.detach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #network.attach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #breakpoint()
    network.add_parameter_references()
    network.add_recorder_references()
    print(network.report())
