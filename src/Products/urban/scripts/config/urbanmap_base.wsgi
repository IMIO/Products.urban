import os, sys
os.environ['PYTHON_EGG_CACHE'] = '#PYTHONEGGCACHE#'
sys.path[0:0] = [
    '#URBANMAPDIR#',
]

from paste.deploy import loadapp

application = loadapp('config:#URBANMAPINI#')