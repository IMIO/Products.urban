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
      install_requires=[
          'setuptools',
          'appy',
          'Plone',
          'Products.MasterSelectWidget',
          'psycopg2',
      ],
      entry_points="""
      """,
      )
