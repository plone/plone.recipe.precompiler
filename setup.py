import os
from setuptools import setup, find_packages

name = "plone.recipe.precompiler"
version = '0.6'


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
    read('README.rst'),
    name,
    read('docs', 'HISTORY.txt'),
    read('docs', 'CONTRIBUTORS.txt'),
    )
)

setup(
    name=name,
    version=version,
    author="Steve McMahon",
    author_email="steve@dcn.org",
    description="zc.buildout recipe to precompile python and po files.",
    long_description=long_description,
    license="GPL v 2",
    keywords="buildout",
    url='https://github.com/plone/plone.recipe.precompiler',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Buildout',
      ],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.recipe'],
    install_requires=[
        'zc.buildout', 'setuptools', 'zc.recipe.egg',
        'python_gettext'
        ],
    dependency_links=['http://download.zope.org/distribution/'],
    zip_safe=False,
    entry_points={'zc.buildout': ['default=%s:Recipe' % name]},
    )
