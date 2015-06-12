import os
import re
from optparse import OptionParser

from genshi.template import Context, NewTextTemplate
from genshi.template.eval import UndefinedError


def retLines(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines


def makeContext(pif):
    import socket
    serverip = socket.gethostbyname(socket.gethostname())

    nisre = re.compile(r'^ *INS *= *(\d+)', re.I)
    sqlurlre = re.compile(
        r'^ *sqlalchemy.url *= *postgresql://(\w+):(\w+)@([\w\.]+):\d+/(\w+)',
        re.I)
    urbanmapre = re.compile(r'^ *urbanmap_url *= *(https?://[^ ]+)', re.I)

    sites = {}

    for pifline in retLines(pif):
        pifline = pifline.strip(' \n')
        if not pifline: continue
        if pifline.startswith('#'): continue
        path, dbname, port = pifline.split(';')
        sitename = dbname[4:]
        nis = dbuser = dbpwd = pghost = pylonhost = ''
        inifilename = os.path.join(
                os.path.abspath(path), 'config', '%s.ini' % dbname)
        if not os.path.exists(inifilename):
            continue
        for line in retLines(inifilename):
            line = line.strip('\n')
            if nisre.match(line):
                nis = nisre.match(line).group(1)
            elif sqlurlre.match(line):
                matching = sqlurlre.match(line)
                dbuser = matching.group(1)
                dbpwd = matching.group(2)
                pghost = matching.group(3)
            elif urbanmapre.match(line):
                pylonhost = urbanmapre.match(line).group(1)
        #geohost = "%s:8080" % serverip
        geohost = "geoserver.communesplone.be"
        sites[sitename] = dict(sitename=sitename, nis=nis, pghost=pghost,
             dbname=dbname, dbuser=dbuser, dbpwd=dbpwd,
             geohost=geohost, pylonhost=pylonhost)
    return sites


class Sites(object):

    def __init__(self, input):
        self.input = input
        self.source = open(self.input).read()

    def execute(self, pif):
        template = NewTextTemplate(self.source)
        sites = makeContext(pif)
        context = Context(sites=[sites[key] for key in sorted(sites.keys())])
        try:
            self.result = template.generate(context).render()
        except UndefinedError, e:
            raise ValueError("Error in template %s:\n%s" % (self.input, e.msg))


class PerSite(object):

    def __init__(self, input, directory, extension):
        self.extension = extension
        self.directory = os.path.abspath(directory)
        self.input = input
        self.source = open(self.input).read()

    def execute(self, siteid):
        template = NewTextTemplate(self.source)
        try:
            context = Context(**self.sites[siteid])
            self.result = template.generate(context).render()
        except UndefinedError, e:
            raise ValueError("Error in template %s:\n%s" % (self.input, e.msg))

    def write(self, siteid):
        output = "%s.%s" % (siteid, self.extension)
        output = os.path.abspath(os.path.join(self.directory, output))
        file = open(output, 'w')
        file.write(self.result)
        file.close()

    def write_files(self, pif):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        self.sites = makeContext(pif)
        for siteid in sorted(self.sites.keys()):
            self.execute(siteid)
            self.write(siteid)


def all():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input")
    parser.add_option("-s", "--source", dest="source")
    (options, args) = parser.parse_args()
    input = os.path.abspath(options.input)
    t = Sites(input)
    t.execute(options.source)
    print t.result


def per_site():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input")
    parser.add_option("-d", "--directory", dest="directory")
    parser.add_option("-e", "--extension", dest="extension")
    parser.add_option("-s", "--source", dest="source")
    (options, args) = parser.parse_args()
    input = os.path.abspath(options.input)
    directory = os.path.abspath(options.directory)
    t = PerSite(input, directory, options.extension)
    t.write_files(options.source)
