import argparse
import pprint

from rich import print as rprint

from pywrparser.types.network import PywrNetwork
from pywrparser.display import (
    write_results,
    results_as_dict,
    results_as_json
)


def configure_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("FILENAME", help="File containing a Pywr network in JSON format")
    parser.add_argument("--raise-on-error",
        action="store_true",
        default=False,
        help="Raise parsing errors as exceptions"
    )
    parser.add_argument("--no-emoji",
        action="store_true",
        default=False,
        help="Omit emoji in console parsing reports"
    )
    parser.add_argument("--no-colour",
        action="store_true",
        default=False,
        help="Omit colour output in console parsing reports."
        " Implies `--no-emoji`"
    )

    return parser.parse_args()


def handle_args(args):
    filename = args.FILENAME
    doraise = args.raise_on_error
    useemoji = not args.no_emoji if not args.no_colour else False

    if args.no_colour:
        from pywrparser.display import console
        console.no_color = True

    network, errors, warnings = PywrNetwork.from_file(filename, raise_on_parser_error=doraise)

    if network:
        network.add_parameter_references()
        network.add_recorder_references()
        report = network.report()
        #print(report)
        rprint(report)
        #rprint(JSON.from_data(report))

    if errors or warnings:
        write_results(filename, errors, warnings, use_emoji=useemoji)
        #rad = results_as_dict(filename, errors, warnings)
        #pprint.pprint(rad)


def run():
    args = configure_args()
    handle_args(args)


if __name__ == "__main__":
    run()
