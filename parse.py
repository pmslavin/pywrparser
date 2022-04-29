import argparse
import sys

from rich import print as rprint

from pywrparser.types.network import PywrNetwork
from pywrparser.display import (
    write_results,
    results_as_json
)
from pywrparser.lib import rules


def configure_args():
    parser = argparse.ArgumentParser()

    meg = parser.add_mutually_exclusive_group()
    meg.add_argument("-f", "--filename",
        help="File containing a Pywr network in JSON format",
        type=str,
        default=None)
    meg.add_argument("-l", "--list-rulesets",
        action="store_true",
        default=False,
        help="Display a list of all available rulesets"
    )

    parser.add_argument("--json-output",
        action="store_true",
        default=False,
        help="Display parsing report in json format for machine reading"
    )
    parser.add_argument("--pretty-output",
        action="store_true",
        default=True,
        help="Display parsing report on the console with colour."
        " This is the default output format"
    )
    parser.add_argument("--raise-on-error",
        action="store_true",
        default=False,
        help="Raise failures of parsing rules as exceptions"
    )
    parser.add_argument("--raise-on-warning",
        action="store_true",
        default=False,
        help="Raise failures of parsing warnings as exceptions."
        " Implies `--raise-on-error`"
    )
    parser.add_argument("--no-duplicate-edges",
        action="store_true",
        default=False,
        help="Duplicate edges are treated as an error"
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
    parser.add_argument("--no-digest",
        action="store_true",
        default=False,
        help="Omit sha256 digest in JSON and dict parsing reports"
    )

    return parser.parse_args()


def handle_args(args):
    filename = args.filename
    raise_error = args.raise_on_error
    raise_warning = args.raise_on_warning
    useemoji = not args.no_emoji if not args.no_colour else False
    include_digest = not args.no_digest
    allow_duplicate_edges = not args.no_duplicate_edges

    if args.no_colour:
        from pywrparser.display import console
        console.no_color = True

    if args.list_rulesets:
        print(rules.describe_rulesets())
        sys.exit(1)

    network, errors, warnings = PywrNetwork.from_file(filename,
                                    raise_on_parser_error=raise_error,
                                    raise_on_parser_warning=raise_warning,
                                    allow_duplicate_edges=allow_duplicate_edges
                                )

    if network:
        network.add_parameter_references()
        network.add_recorder_references()
        report = network.report()
        rprint(report)

    if errors or warnings:
        if args.json_output:
            print(results_as_json(filename, errors, warnings, include_digest=include_digest))
        else:
            write_results(filename, errors, warnings, use_emoji=useemoji)


def run():
    args = configure_args()
    handle_args(args)


if __name__ == "__main__":
    run()
