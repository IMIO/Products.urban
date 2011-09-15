from setuptools import setup, find_packages
import os

version = '1.0b1'

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
            test=['unittest2', 'zope.testing', 'plone.testing',
                  'testfixtures',
                  'plone.app.testing']),
      install_requires=[
          'setuptools',
          'appy',
          'Plone',
          'Pillow',
          'archetypes.referencebrowserwidget',
          'five.grok',
          'grokcore.component',
          'collective.plonefinder',
          'Products.MasterSelectWidget',
          'Products.DataGridField',
          'python-dateutil',
          'collective.externaleditor',
          'Products.ExternalEditor',
          'plone.app.referenceintegrity',
          'psycopg2'])
