from setuptools import setup, find_packages
import os

version = "2.7.22.dev0"

setup(
    name="Products.urban",
    version=version,
    description="Urban Certificate Management",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "CHANGES.rst")).read(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="Urban IMIO",
    author="Simon Delcourt",
    author_email="simon.delcourt@imio.be",
    url="http://www.communesplone.org/les-outils/applications-metier/"
    "gestion-des-permis-durbanisme",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["Products"],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            "unittest2",
            "zope.testing",
            "plone.testing",
            "testfixtures",
            "plone.app.testing",
            "plone.app.robotframework[debug, test]",
            "ipdb",
        ],
        templates=[
            "Genshi",
        ],
    ),
    install_requires=[
        "archetypes.referencebrowserwidget",
        "collective.ckeditor",
        "collective.datagridcolumns",
        "collective.delaycalculator",
        "collective.documentgenerator>=3.20",
        "collective.externaleditor",
        "collective.exportimport",
        "collective.faceted.datewidget",
        "collective.fingerpointing",
        "collective.iconifieddocumentactions",
        "collective.js.jqueryui",
        "collective.messagesviewlet",
        "collective.noindexing",
        "collective.wfadaptations",
        "collective.z3cform.datagridfield>=0.15",
        "collective.archetypes.select2",
        "five.grok",
        "grokcore.component",
        "imio.actionspanel",
        "imio.dashboard",
        "imio.pm.locales",
        "imio.pm.wsclient",
        "imio.restapi",
        "imio.schedule",
        "imio.urban.core",
        "imio.ws.register",
        "numpy",
        "Pillow",
        "Plone",
        "Products.CMFPlacefulWorkflow",
        "Products.ContentTypeValidator",
        "Products.CPUtils",
        "Products.DataGridField",
        "Products.MasterSelectWidget",
        "Products.PasswordStrength",
        "plone.api",  # to remove once we use a plone version including plone.api
        "plone.app.contenttypes",
        "plone.app.referenceintegrity",
        "plone.namedfile",  # ugly fix because TinyMce needs it but didnt declared it in its setup dependencies
        "plone.z3ctable",
        "plonetheme.imioapps",
        "Products.cron4plone",
        "psycopg2",
        "python-dateutil",
        "python-Levenshtein",
        "requests",
        "setuptools",
        "Sphinx",
        "SQLAlchemy",
        "testfixtures",
        "zope.app.container",
        "zope.sqlalchemy",
        "urban.restapi",
        "urban.vocabulary",
        "urban.schedule",
        "urban.events",
        "python-dateutil",
        "PyMySQL",
    ],
    entry_points={
        "console_scripts": [
            "templates = Products.urban.templates:all",
            "templates_per_site = Products.urban.templates:per_site",
        ],
    },
)
