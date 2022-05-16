Rules, Warnings, and Rulesets
=============================

Overview
--------

Rules
    Methods defined on Pywr component types (:class:`PywrNode`, :class:`PywrParameter`, etc.)
    which perform arbitrary tests on the data defining that type.

    If the tests are passed an instance of the type can be created, but if the tests are
    failed no instance is created, the containing network is considered `invalid` and an
    ``error`` state is added to the parsing report describing the test that has failed
    and the input data which caused the failure.

    The methods which define rules are applied automatically to the input data by the
    parser during the parsing process.

Warnings
    Methods defined on Pywr component types which operate similarly to ``rules`` but
    result in a ``warning`` which does not prevent the creation of an instance of the
    component type.  As such, `warnings` are used to identify component definitions which
    are in some way suboptimal or may be deprecated in future releases, but which by
    themselves do not preclude the creation of a functioning component of the specified
    type.

    A network which may contain `warnings` but no `errors` is considered `valid`.

Rulesets
    Collections of ``rules`` and ``warnings`` which are customisable and which may
    applied as a group to a Pywr network.

    Custom rulesets allow different collections of ``rules`` and ``warnings`` to be
    applied to a network depending on the context in which the parser operates.


Defining Rules, Warnings, and Rulesets
--------------------------------------

Rules and Warnings
------------------

Both ``rules`` and ``warnings`` are defined as methods on the class representing the
component which they validate.

The method is defined using a structured method name, and an optional :func:`match`
decorator which specifies the sub-types of the component to which the rule or warning should
be applied.

For example, the following rule ensures that the `name` attribute of its data has a
specified minimum length:

.. code-block:: python

    class MyPywrNode(PywrNode):
        ...

    def rule_node_name_min_len(self):
        assert len(self.name) > 6, "Node name too short"

If a rule returns indeed any value, including ``None``, it is deemed to have `passed`.
If a rule raises any form of exception, it has `failed` and an error instance is
logged by the parser.

Methods which implement rules are identified automatically by the parser and applied
to the relevant type when an instance of that type is created.  Any method which begins
with the special prefix ``rule_`` is interpreted as a validation rule.  Any method
beginning with the prefix ``warn_`` indicates a `warning`.  Warnings have identical
behaviour to rules in terms of returning a value or raising an exception, but in the
event of a warning method failing, the parser logs a warning instance and this does
not preclude creation of the corresponding component instance or the network as a whole.

The :func:`match` decorator
---------------------------

TBA

Rulesets
--------

A ``ruleset`` is simply a module in the :mod:`pywrparser.rulesets` package which defines
custom component classes derived from the base types:

* PywrMetadata
* PywrTimestepper
* PywrNode
* PywrParameter
* PywrRecorder
* PywrScenario

The base types are each defined in a dedicated module in :mod:`pywrparser.types` and
should always be imported from the module rather than the :mod:`types` package
when being subclassed. E.g.

.. code-block:: python

    from pywrparser.types.node import PywrNode

Any classes which derive from the base types in a ruleset module are automatically
identified by the parser and become part of the ruleset defined by that module.

In addition, a ruleset module must contain certain module-level variables which are
used by `pywrparser` to describe the ruleset.

__key__
    A short string which acts as the identifier for the ruleset, e.g. "strict"

__ruleset_name__
    A string holding the full name for the ruleset, e.g. "Strict Ruleset"

__version__
    A string containing the version number of the ruleset, e.g. "0.1.0"

__description__
    A string of arbitrary length which describes the ruleset, e.g.
    "A ruleset which enforces strict naming conventions"

Finally, each ruleset module must be imported into the :mod:`ruleset` package's
``__init__.py``.  For example, to import the ruleset defined in the
``/pywrparser/rulesets/strict.py`` file, add...

.. code-block:: python

    from . import strict

...to ``/pywrparser/rulesets/__init__.py``.

The procedure to create a custom ruleset may therefore be summarised as:

1. Create a ruleset module which imports the required base types and defines
   the required module-level variables as described above.

2. Define subclasses of each required base type, defining appropriate
   ``rule_`` and ``warn_`` methods inside these.

3. Add an import of the new ruleset module in the :mod:`ruleset` package's
   :file:`__init__.py`


The ruleset will then be visible in the output from the command line utility's
``--list-rulesets`` option...

.. code-block:: console

    $ pywrparser --list-rulesets
    Available Rulesets:

    [1]	Name: 'Strict Ruleset'  Version: 0.1.0  Key: strict
        A ruleset which enforces strict naming conventions

...and may be applied to input using the ``--use-ruleset <key>`` option...

.. code-block:: console

    $ pywrparser --use-ruleset strict ...

