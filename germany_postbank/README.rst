~~~~~~~~~~~~~~~~~~~~~~~
ofxstatement-postbank
~~~~~~~~~~~~~~~~~~~~~~~

`ofxstatement`_ plugin to support German Postbank bank statements

`ofxstatement`_ is a tool
to convert proprietary bank statement to OFX format, suitable for
importing into account programms like GnuCash or YNAB classic.

Plugins for `ofxstatement`_ parses a particular
proprietary bank statement format and produces common data structure,
that is then formatted into an OFX file.

This project provides an `ofxstatement`_ plugin for the German bank
Postbank.

Postbank is providing different formats, one of them is a nicely
parsable XML format.

Using `ofxstatement`_ and this plugin, I  successfully converted
bank statements to OFX and import this into my accounting software.
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
  cd ofxstatement-germany/germany_postbank
  pip3 install --user .

Check the Python documentation on instructions for you operating system and
setup. Remember you must use Python 3.


Setup
=====

Check if plugin is installed:

.. code:: bash

  ofxstatement list-plugins

Expected output::

  germany_postbank

Edit config. The *account* is the ID used by your accounting program to
associate the transactions with a certain account. Probably you want to use
your bank account number (Kontonummer) i.e. the last 10 digits of your IBAN.

.. code:: bash

  ofxstatement edit-config

A text editor will open. Configure something like this::

  [postbank]
  plugin = germany_postbank
  account = 0123456789

Some other config options you may set are:

* *bank* (default: 50050201)
* *currency* (default: EUR)
* *charset* (default: iso-8859-1)


Usage
=====

.. code:: bash

  ofxstatement convert -t postbank umsaetze-0123456789-03.02.2018_15_05.csv test.ofx

You may then import *test.ofx* into any accounting program which
accepts OFX, for example YNAB-classix or gnuCash.

.. _ofxstatement: https://github.com/kedder/ofxstatement
