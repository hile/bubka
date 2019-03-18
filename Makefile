#
# Install the scrips, configs and python modules
#

all:
	flake8 | sort

clean:
	@rm -rf build dist .DS_Store .cache .eggs
	@find . -name '*.egg-info' -print0|xargs -0 rm -rf
	@find . -name '*.pyc' -print0|xargs -0 rm -rf

test:
	python setup.py test

build:
	python setup.py build

upload: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: all test
