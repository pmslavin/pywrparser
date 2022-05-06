Usage
=====

Installation
------------

PywrParser can be installed with the `Poetry <https://python-poetry.org>`_ command:

.. code-block:: console

   $ git clone git@github.com:pmslavin/pywrparser.git
   $ cd pywrparser
   $ poetry install
   $ poetry -h
   usage: pywrparser [-h] [-f <filename> | -l] [--use-ruleset <ruleset>] [--json-output] [--pretty-output] [--raise-on-error] [--raise-on-warning] [--no-duplicate-edges] [--no-emoji]
                  [--no-colour] [--no-digest]

   optional arguments:
      -h, --help            show this help message and exit
      -f <filename>, --filename <filename>
                            File containing a Pywr network in JSON format
      -l, --list-rulesets   Display a list of all available rulesets
      --use-ruleset <ruleset>
                            Apply the specified ruleset during parsing
      --json-output         Display parsing report in json format for machine reading
      --pretty-output       Display parsing report on the console with colour. This is the default output format
      --raise-on-error      Raise failures of parsing rules as exceptions
      --raise-on-warning    Raise failures of parsing warnings as exceptions. Implies `--raise-on-error`
      --no-duplicate-edges  Duplicate edges are treated as an error
      --no-emoji            Omit emoji in console parsing reports
      --no-colour           Omit colour output in console parsing reports. Implies `--no-emoji`
      --no-digest           Omit sha256 digest in JSON and dict parsing reports

Invocation
----------

PywrParser provides both a command-line utility for validating Pywr JSON models,
and a Python library which may be used to parse and manipulate Pywr networks.

This section provides details of the command-line utility.
