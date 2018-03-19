~~~~~~~~~~~~~~~~~~~~~~~
ofxstatement-germany
~~~~~~~~~~~~~~~~~~~~~~~

`ofxstatement`_ plugin to support different German bank statements.

`ofxstatement`_ is a tool
to convert proprietary bank statement to OFX format, suitable for
importing into account programms like GnuCash or YNAB classic.

Plugins for `ofxstatement`_ parses a particular
proprietary bank statement format and produces common data structure,
that is then formatted into an OFX file.

This project provides an `ofxstatement`_ plugin for the following German banks:

* 1822direkt
* Postbank

Other will follow, I accept pull request for other German Banks.

Using `ofxstatement`_ and this plugin, I  successfully converted
these bank statements to OFX and import this into my accounting software.
I'm using YNAB classic for now. But GnuCash should also work fine.


Requirements
============

You need python 3.x to run this as ofxstament seems to requires python3


Installation
============

There are multiple ways of installing Python packages. This is just one
example:

.. code:: bash

  pip3 install --user ofxstatement
  git clone https://github.com/MirkoDziadzka/ofxstatement-germany
  cd ofxstatement-germany
  pip3 install --user germany_postbank (or any other provided plugin)

Check the Python documentation on instructions for you operating system and
setup. Remember you must use Python 3.

Also check the README in the sub directories for the different banks.


.. _ofxstatement: https://github.com/kedder/ofxstatement
