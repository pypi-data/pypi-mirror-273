Flake8 Extension to enforce better comma placement.
===================================================

This is an obsolete fork of PyCQA/flake8-commas which added support for Python
3.12, match statement, and other features. Support for Python version below 3.8
was dropped, as well as older (5.x) versions of flake8.

**This fork is deprecated -- use flake8-commas instead.**

|Build Status| |PyPI - Version| |No Maintenance Intended|

Migration back to flake8-commas
-------------------------------

All users should migrate back to `flake8-commas <https://pypi.org/project/flake8-commas/>`_.

As both packages unfortunately install the same module, removal of this package is required *before* installing that one:

.. code:: shell

    pip uninstall flake8-commas-x
    pip install flake8-commas

Usage
-----

If you are using flake8 it's as easy as:

.. code:: shell

    pip install flake8-commas-x

Now you can avoid those annoying merge conflicts on dictionary and list diffs.

Errors
------

Different versions of python require commas in different places. Ignore the
errors for languages you don't use in your flake8 config:

+------+-----------------------------------------+
| Code | message                                 |
+======+=========================================+
| C812 | missing trailing comma                  |
+------+-----------------------------------------+
| C813 | missing trailing comma in Python 3      |
+------+-----------------------------------------+
| C814 | missing trailing comma in Python 2      |
+------+-----------------------------------------+
| C815 | missing trailing comma in Python 3.5+   |
+------+-----------------------------------------+
| C816 | missing trailing comma in Python 3.6+   |
+------+-----------------------------------------+
| C818 | trailing comma on bare tuple prohibited |
+------+-----------------------------------------+
| C819 | trailing comma prohibited               |
+------+-----------------------------------------+

Examples
--------

.. code:: Python

    lookup_table = {
        'key1': 'value',
        'key2': 'something'  # <-- missing a trailing comma
    }

    json_data = json.dumps({
        "key": "value",
    }),                      # <-- incorrect trailing comma. json_data is now a tuple. Likely by accident.


.. |Build Status| image:: https://github.com/PeterJCLaw/flake8-commas/actions/workflows/.github/workflows/tests.yml/badge.svg?branch=main
   :target: https://github.com/PeterJCLaw/flake8-commas/actions?query=branch%3Amain

.. |PyPI - Version| image:: https://img.shields.io/pypi/v/flake8-commas-x
   :target: https://pypi.org/project/flake8-commas-x/

.. |No Maintenance Intended| image:: https://unmaintained.tech/badge.svg
  :target: https://unmaintained.tech
  :alt: No Maintenance Intended
