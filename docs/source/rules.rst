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

Both ``rules`` and ``warnings`` are defined as methods on the class representing the
component which they validate.

The method is defined using a structured method name, and an optional :func:`match`
decorator which specifies the sub-types of the component to which the rule or warning should
be applied.
