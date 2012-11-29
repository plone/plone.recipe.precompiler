import os
from setuptools import setup, find_packages

name = "plone.recipe.precompiler"
version = '0.5dev'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = ("""%s

Change history
==============

Changelog for %s.

%s

Contributors
============

%s

""" % (
    read('README.rtf'),
    name,
    read('docs', 'HISTORY.txt'),
    read('docs', 'CONTRIBUTORS.txt'),
    )
)

setup(
    name = name,
    version = version,
    author = "Steve McMahon",
    author_email = "steve@dcn.org",
    description = "zc.buildout recipe to precompile python- and po-files.",
    long_description = long_description,
    license = "ZPL 2.1",
    keywords = "zope2 buildout",
    url='https://svn.plone.org/svn/collective/buildout/plone.recipe.precompiler',
    classifiers=[
      "License :: OSI Approved :: Zope Public License",
      "Framework :: Buildout",
      "Framework :: Zope2",
      "Framework :: Zope3",
      "Programming Language :: Python",
      ],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['plone', 'plone.recipe'],
    install_requires = ['zc.buildout', 'setuptools', 'zc.recipe.egg'],
    dependency_links = ['http://download.zope.org/distribution/'],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = %s:Recipe' % name]},
    )
