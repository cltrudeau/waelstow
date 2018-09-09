0.10.2
======

Non-compiling test cases used to be ignored by list_tests(), this causes
problems when filtering test cases as nothing will get run if the shortcut
label points to a file that doesn't compile. This has been fixed.

0.10.1
======

* update build process to create a universal wheel

0.10
====

* project was initially part of http://python-wrench.readthedocs.io/en/latest/
* initial pypi commit of indendent library
