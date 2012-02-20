import os, sys
sys.path.append('#URBANMAPDIR#')
os.environ['PYTHON_EGG_CACHE'] = '#PYTHONEGGCACHE#'

from paste.deploy import loadapp

application = loadapp('config:#URBANMAPINI#')