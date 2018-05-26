~~~~~~~~~~~~~~~~~~~~~~~
ofxstatement-fidorbank UPDATE THIS README
~~~~~~~~~~~~~~~~~~~~~~~

`ofxstatement`_ plugin to support banking.fidor.de CSV bank statements

`ofxstatement`_ is a tool
to convert proprietary bank statements to OFX format, suitable for
importing into account programs like GnuCash or YNAB.

Plugins for `ofxstatement`_ parse a particular
proprietary bank statement format and produce common data structure,
that is then formatted into an OFX file.

This project provides an `ofxstatement`_ plugin for the German bank
Fidor Bank.

Using `ofxstatement`_ and this plugin, I  successfully converted
CSV bank statements to OFX and imported this into YNAB. Any software
supporting the OFX format should work fine.


Requirements
============

You need python 3.x to run this as ofxstament requires python3


Installation
============

There are multiple ways of installing Python packages. This is just one
example:

.. code:: bash

  pip3 install --user ofxstatement
  git clone https://github.com/MirkoDziadzka/ofxstatement-germany
  cd ofxstatement-germany/germany_fidorbank
  pip3 install --user .

Check the Python documentation on instructions for your operating system and
setup. Remember, you must use Python 3.


Setup
=====

Check if the plugin is installed:

.. code:: bash

  ofxstatement list-plugins

Expected output::

  germany_fidorbank

Edit config. The *account* is the ID used by your accounting program to
associate the transactions with a certain account. Probably you want to use
your bank account number (Kontonummer) i.e. the last 10 digits of your IBAN.
(Note: YNAB does not seem to care about this field, since you import directly
to the account screen anyway.)

.. code:: bash

  ofxstatement edit-config

A text editor will open. Configure something like this::

  [fidorbank]
  plugin = germany_fidorbank
  account = 0123456789

Some other config options you may set are:

* *bank* (default: 50050201)
* *currency* (default: EUR)
* *charset* (default: iso-8859-1)


Usage
=====

.. code:: bash
  ofxstatement convert -t fidorbank umsaetze-0123456789-03.02.2018_15_05.csv test.ofx

You may then import *test.ofx* into any accounting program which
accepts OFX, for example YNAB-classix or gnuCash.

.. _ofxstatement: https://github.com/kedder/ofxstatement
