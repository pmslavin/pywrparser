Usage
=====

Installation
------------

PywrParser can be installed with the `Poetry <https://python-poetry.org>`_ command:

.. code-block:: console

   $ git clone git@github.com:pmslavin/pywrparser.git
   $ cd pywrparser
   $ poetry install
   $ pywrparser -h
   usage: pywrparser [-f <filename> | -l] [OPTIONS]

   A toolkit for parsing and validating Pywr models.

   optional arguments:
     -h, --help            show this help message and exit
     -f <filename>, --filename <filename>
                           File containing a Pywr network in JSON format
     -l, --list-rulesets   Display a list of all available rulesets

   validation options:
     --use-ruleset <ruleset>
                           Apply the specified ruleset during parsing
     --raise-on-warning    Raise failures of parsing warnings as exceptions. Implies `--raise-on-error`
     --raise-on-error      Raise failures of parsing rules as exceptions
     --no-duplicate-edges  Duplicate edges are treated as an error

   display options:
     --json-output         Display parsing report in json format for machine reading
     --pretty-output       Display parsing report on the console with colour. This is the default output format
     --no-emoji            Omit emoji in console parsing reports
     --no-colour           Omit colour output in console parsing reports. Implies `--no-emoji`

   general options:
     --no-digest           Omit sha256 digest in JSON and dict parsing reports
     --version             Display the version of pywrparser

   For further information, please visit https://pmslavin.github.io/pywrparser

Invocation
----------

PywrParser provides both a command-line utility for validating Pywr JSON models,
and a Python library which may be used to parse and manipulate Pywr networks.

This section provides details of the command-line utility.

Usage of the :class:`pywrparser` library is described in :doc:`library` section.

Basic Usage
===========

Validation
----------

The basic operation of the :class:`pywrparser` command validates a Pywr JSON network,
and returns either:

* A report describing a valid Pywr network, along with any warnings generated
  when parsing the network
* A report detailing the errors that prevented parsing
