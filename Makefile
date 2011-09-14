#!/usr/bin/make
#
all: test

bin/python:
	virtualenv-2.6 --no-site-packages .

develop-eggs: bin/python bootstrap.py
	./bin/python bootstrap.py

bin/buildout: develop-eggs

bin/test: buildout.cfg bin/buildout setup.py
	./bin/buildout -vt 5

bin/instance: buildout.cfg bin/buildout setup.py
	./bin/buildout -vt 5 install instance

.PHONY: test
test: bin/test
	bin/test -s Products.urban

.PHONY: instance
instance: bin/instance
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg
