from setuptools import setup, find_packages
import os

version = '1.11.0.dev0'

setup(name='Products.urban',
      version=version,
      description="Urban Certificate Management",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://www.communesplone.org/les-outils/applications-metier/'
          'gestion-des-permis-durbanisme',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'unittest2', 'zope.testing', 'plone.testing',
              'testfixtures',
              'plone.app.testing',
              'plone.app.robotframework[debug, test]',
          ],
          templates=[
              'Genshi',
          ]),
      install_requires=[
          'archetypes.referencebrowserwidget',
          'collective.z3cform.datagridfield>=0.15',
          'collective.datagridcolumns',
          'collective.delaycalculator',
          'collective.documentgenerator',
          'collective.externaleditor',
          'collective.iconifieddocumentactions',
          'collective.js.jqueryui',
          'five.grok',
          'grokcore.component',
          'imio.actionspanel',
          'imio.dashboard',
          'Pillow',
          'Plone',
          'Products.CMFPlacefulWorkflow',
          'Products.ContentTypeValidator',
          'Products.DataGridField',
          'Products.MasterSelectWidget',
          'plone.api',  # to remove once we use a plone version including plone.api
          'plone.app.referenceintegrity',
          'plone.namedfile',  # ugly fix because TinyMce needs it but didnt declared it in its setup dependencies
          'plone.z3ctable',
          'plonetheme.imioapps',
          'profilehooks',
          'psycopg2',
          'python-dateutil',
          'python-Levenshtein',
          'requests',
          'setuptools',
          'Sphinx',
          'SQLAlchemy',
          'testfixtures',
          'zope.app.container',
      ],
      entry_points={
          'console_scripts': ['templates = Products.urban.templates:all',
          'templates_per_site = Products.urban.templates:per_site']
      },
      )
