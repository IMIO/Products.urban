#!/usr/bin/make
#

options =

mountpoints = src/Products/urban/scripts/config/mount_points.conf
plonesites = src/Products/urban/scripts/config/plonesites.cfg
extras = src/Products/urban/scripts/config/extras.py.tmpl

.PHONY: test instance cleanall portals

all: test docs

bin/python:
	virtualenv-2.7 .

develop-eggs: bin/python bootstrap.py
	./bin/python bootstrap.py

docs: docs/html/index.html

docs/html/index.html: README.rst docs/*.rst docs/urban/*.rst bin/sphinx-build
	bin/sphinx-build -W docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

bin/buildout: develop-eggs

bin/test: versions.cfg buildout.cfg bin/buildout setup.py
	./bin/buildout -t 5
	touch $@

bin/instance: versions.cfg buildout.cfg bin/buildout setup.py
	./bin/buildout -t 5 install instance
	touch $@

bin/templates: setup.py buildout.cfg
	./bin/buildout -t 5 install templates
	touch $@

bin/templates_per_site: bin/templates
	touch $@

pre_extras: bin/templates_per_site $(extras)
	bin/templates_per_site -i $(extras) -d pre_extras -e py -s tmp/pylon_instances.txt
	touch $@

plonesites.cfg: bin/templates $(plonesites) pre_extras
	bin/templates -i $(plonesites) -s tmp/pylon_instances.txt > plonesites.cfg

mount_points.conf: bin/templates $(mountpoints)
	bin/templates -i $(mountpoints) -s tmp/pylon_instances.txt > $@

test: bin/test
	bin/test -s Products.urban $(options)

instance: bin/instance
	bin/instance fg

cleanall:
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg devel

portals: versions.cfg buildout.cfg plonesites.cfg portals.cfg bin/buildout setup.py mount_points.conf
	./bin/buildout -vt 5 -c portals.cfg
