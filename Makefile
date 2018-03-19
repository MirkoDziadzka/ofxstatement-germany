PYTHON=.venv/bin/python

all: PYTHON

PYTHON: setup.py
	-rm -r .venv
	virtualenv --clear --python python3 .venv
	$(PYTHON) setup.py develop
