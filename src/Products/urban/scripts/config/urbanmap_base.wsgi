import os, sys
os.environ['PYTHON_EGG_CACHE'] = '#PYTHONEGGCACHE#'
sys.path[0:0] = [
    '#URBANMAPDIR#',
# replace this line by all the eggs list found in urbanmap/bin/paster
]

from paste.deploy import loadapp

application = loadapp('config:#URBANMAPINI#')