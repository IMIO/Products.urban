#!/usr/bin/make
#

options =
plonesites = parts/omelette/Products/urban/scripts/config/plonesites.cfg 
extras = parts/omelette/Products/urban/scripts/config/extras.py.tmpl
mountpoints = parts/omelette/Products/urban/scripts/config/mount_points.conf

all: run

.PHONY: bootstrap
bootstrap:
	virtualenv -p python2 .
	./bin/python bootstrap.py
	./bin/subproducts.sh
	./bin/pip install -r requirements.txt

.PHONY: setup
setup:
	virtualenv -p python2 .
	./bin/pip install --upgrade pip
	./bin/pip install -r requirements.txt

.PHONY: buildout
buildout:
	if ! test -f bin/buildout;then make setup;fi
	bin/buildout -t 60

.PHONY: run
run:
	if ! test -f bin/instance1;then make buildout;fi
	bin/instance1 fg

.PHONY: cleanall
cleanall:
	rm -fr bin/instance1 develop-eggs downloads eggs parts .installed.cfg

.PHONY: libraries
libraries: 
	./bin/subproducts.sh

bin/templates:
	./bin/buildout -t 60 install templates
	touch $@

bin/templates_per_site: 
	./bin/buildout -t 60 install templates
	touch $@

mount_points.conf: bin/templates $(mountpoints)
	bin/templates -i $(mountpoints) -s /srv/urbanmap/urbanMap/config/pylon_instances.txt > $@

pre_extras: bin/templates_per_site $(extras) /srv/urbanmap/urbanMap/config/pylon_instances.txt
	bin/templates_per_site -i $(extras) -d pre_extras -e py -s /srv/urbanmap/urbanMap/config/pylon_instances.txt

plonesites.cfg: bin/templates $(plonesites) pre_extras
	bin/templates -i $(plonesites) -s /srv/urbanmap/urbanMap/config/pylon_instances.txt > plonesites.cfg
