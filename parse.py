import argparse
import sys

from rich import print as rprint

from pywrparser import (
    rules,
    __version__
)
from pywrparser.display import (
    write_results,
    results_as_json
)
from pywrparser.types.network import PywrNetwork


def configure_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-f <filename> | -l] [OPTIONS]",
        epilog="For further information, please visit https://pmslavin.github.io/pywrparser",
        description="A toolkit for parsing and validating Pywr models."
    )

    meg = parser.add_mutually_exclusive_group()
    meg.add_argument("-f", "--filename",
        metavar="<filename>",
        help="File containing a Pywr network in JSON format",
        type=str,
        default=None)
    meg.add_argument("-l", "--list-rulesets",
        action="store_true",
        default=False,
        help="Display a list of all available rulesets"
    )

    validation = parser.add_argument_group("validation options")

    validation.add_argument("--use-ruleset",
        metavar="<ruleset>",
        type=str,
        default=None,
        help="Apply the specified ruleset during parsing"
    )

    validation.add_argument("--raise-on-warning",
        action="store_true",
        default=False,
        help="Raise failures of parsing warnings as exceptions."
        " Implies `--raise-on-error`"
    )
    validation.add_argument("--raise-on-error",
        action="store_true",
        default=False,
        help="Raise failures of parsing rules as exceptions"
    )
    validation.add_argument("--no-duplicate-edges",
        action="store_true",
        default=False,
        help="Duplicate edges are treated as an error"
    )

    display = parser.add_argument_group("display options")

    display.add_argument("--json-output",
        action="store_true",
        default=False,
        help="Display parsing report in json format for machine reading"
    )
    display.add_argument("--pretty-output",
        action="store_true",
        default=True,
        help="Display parsing report on the console with colour."
        " This is the default output format"
    )
    display.add_argument("--no-emoji",
        action="store_true",
        default=False,
        help="Omit emoji in console parsing reports"
    )
    display.add_argument("--no-colour",
        action="store_true",
        default=False,
        help="Omit colour output in console parsing reports."
        " Implies `--no-emoji`"
    )

    general = parser.add_argument_group("general options")

    general.add_argument("--no-digest",
        action="store_true",
        default=False,
        help="Omit sha256 digest in JSON and dict parsing reports"
    )
    general.add_argument("--version",
        action="store_true",
        default=False,
        help="Display the version of %(prog)s"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()


def handle_args(args):
    filename = args.filename
    raise_error = args.raise_on_error
    raise_warning = args.raise_on_warning
    useemoji = not args.no_emoji if not args.no_colour else False
    include_digest = not args.no_digest
    allow_duplicate_edges = not args.no_duplicate_edges

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.list_rulesets:
        print(rules.describe_rulesets(),end="")
        sys.exit(0)

    if ruleset := args.use_ruleset:
        rulesets = rules.get_rulesets()
        if not ruleset in rulesets:
            print(f"No ruleset with key: {ruleset}", file=sys.stderr)
            sys.exit(1)

    if args.no_colour:
        from pywrparser.display import console
        console.no_color = True

    network, errors, warnings = PywrNetwork.from_file(filename,
                                    raise_on_parser_error=raise_error,
                                    raise_on_parser_warning=raise_warning,
                                    allow_duplicate_edges=allow_duplicate_edges,
                                    ruleset=ruleset
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
