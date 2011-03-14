MODULE = `(find . -maxdepth 2 -name "__init__.py") | tail -n 1 | sed 's/\/__init__.py//' | sed 's/\.\///'`

all:
	@echo "Nothing to do"

install:
	pip install -r requirements.txt
	python setup.py install
	python ${MODULE}/manage.py syncdb --noinput

test:
	python ${MODULE}/manage.py test

.PHONY: install test 
