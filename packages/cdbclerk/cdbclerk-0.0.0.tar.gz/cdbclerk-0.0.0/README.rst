===============================
cdbclerk
===============================

|CI badge| |PyPI badge|

.. |CI badge| image:: https://github.com/spc-group/cdbclerk/actions/workflows/ci.yml/badge.svg
	:target: https://github.com/spc-group/cdbclerk/actions/workflows/ci.yml
.. |PyPI badge| image:: https://img.shields.io/pypi/v/cdbclerk.svg
        :target: https://pypi.python.org/pypi/cdbclerk

A tool for updating CA/PVA PVs from the components database.

Usage
-----

The main entry point for cdbclerk is the command ``cdbclerk``.

To save the fields for a motor accessible over channel-access at the
PV "255idcVME:m1" to the components database, run

```bash
cdbclerk store 255idcVME:m1
```

Documentation
-------------

Sphinx-generated documentation for this project can be found here:
https://spc-group.github.io/cdbclerk/

Requirements
------------

Describe the project requirements (i.e. Python version, packages and
how to install them)

Installation
------------

The following will download the package and load it into the python environment.

.. code-block:: bash

    git clone https://github.com/spc-group/cdbclerk
    pip install -e cdbclerk


Running the Tests
-----------------

.. code-block:: bash

  $ pip install -e ".[dev]"
  $ pytest -vv
