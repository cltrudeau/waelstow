0.11.0
======

* Removed support for Python versions 3.6 and below
* Added testing for Python 3.7, 3.8, 3.9, 3.10, 3.11
* Added noted_raise context manager

0.10.2
======

* Non-compiling test cases used to be ignored by list_tests(), this causes
  problems when filtering test cases as nothing will get run if the shortcut
  label points to a file that doesn't compile. This has been fixed.

0.10.1
======

* update build process to create a universal wheel

0.10
====

* project was initially part of http://python-wrench.readthedocs.io/en/latest/
* initial pypi commit of independent library
