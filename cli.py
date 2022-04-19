import os
import sys
import logging
import pprint

from rich import print as rprint
from rich.json import JSON

from pywrparser.types.network import PywrNetwork
from pywrparser.display import (
    write_results,
    results_as_dict,
    results_as_json
)

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)

if __name__ == "__main__":
    filename = sys.argv[-1]
    #parser = PywrJSONParser(filename)
    #parser.parse(raise_on_error=False)

    network, errors, warnings = PywrNetwork.from_file(filename, raise_on_parser_error=False)

    """
    if warnings:
        for component, warns in warnings.items():
            print(f"[{component}]")
            for warning in warns:
                print(warning)

    if errors:
        for component, errs in errors.items():
            print(f"[{component}]")
            for err in errs:
                print(err)
        exit(1)
    """

    #pprint.pprint(network.as_dict())
    #print("==: End of network.as_dict() :==")
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #network.attach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    """
    for n in network.nodes.values():
        for attr, value in n.data.items():
            if isinstance(value, dict) and "type" in value:
                print(f"Inline parameter: __{n.name}__:{attr}")
    """
    #network.detach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #network.attach_parameters()
    #pprint.pprint(network.parameters)
    #print(len(network.parameters))
    #print("="*46)
    #breakpoint()
    if network:
        network.add_parameter_references()
        network.add_recorder_references()
        report = network.report()
        #print(report)
        rprint(report)
        #rprint(JSON.from_data(report))

    if errors or warnings:
        write_results(filename, errors, warnings, use_emoji=True)
        rad = results_as_dict(filename, errors, warnings)
        #pprint.pprint(rad)
