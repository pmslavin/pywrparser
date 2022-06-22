The `pywrparser` Library
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   network
   parser


Usage
=====

Overview
--------

The :class:`PywrNetwork` class provides a simple interface for Pywr JSON
to be parsed, validated, and represented as a Python object.

Two factory methods are provided to create a :class:`PywrNetwork` instance:

* :meth:`pywrparser.types.network.PywrNetwork.from_file`
* :meth:`pywrparser.types.network.PywrNetwork.from_json`

which operate on a file and a JSON string respectively.
For example, to create a :class:`PywrNetwork` from a filename using the default
arguments:

.. code-block:: python

    from pywrparser.types.network import PywrNetwork

    network, errors, warnings = PywrNetwork.from_file("MyPywrNetwork.json")

If the input file contains a valid network, an instance of :class:`PywrNetwork`
will be returned in the ``network`` variable, the ``errors`` variable will be `None`,
and warnings generated during parsing will be present in the ``warnings`` variable,
or this will be `None` if no warnings were generated. As such, either one of ``network``
or ``errors`` will be ``not None``, but not both.

The ``errors`` and ``warnings`` objects
---------------------------------------

When present, the ``errors`` and ``warnings`` objects returned by the :class:`PywrNetwork`
factory methods are each a dictionary mapping the string names of Pywr network components
(`nodes`, `parameters`, etc.) to a list of the errors or warnings generated when
parsing instances of those components.  Each error is warning is represented by
an instance of :class:`PywrTypeValidationError` or :class:`PywrTypeValidationWarning`
respectively.

The :func:`results_as_dict` and :func:`results_as_json` functions in the :mod:`pywrparser.display`
module provide a convenient means to translate ``errors`` and ``warnings`` objects
into `dict` and JSON form respectively.
