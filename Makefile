.PHONY: clean test

install:
	mkdir -p service/log
	mkdir -p service/run
	python setup.py install

test:
	py.test
