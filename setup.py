from setuptools import setup, find_packages

name = "plone.recipe.precompiler"
version = "0.7.2"


def read(filename):
    with open(filename) as myfile:
        try:
            return myfile.read()
        except UnicodeDecodeError:
            # Happens on one Jenkins node on Python 3.6,
            # so maybe it happens for users too.
            pass
    # Opening and reading as text failed, so retry opening as bytes.
    with open(filename, "rb") as myfile:
        contents = myfile.read()
        return contents.decode("utf-8")


long_description = """%s

Change history
==============

Changelog for %s.

%s

Contributors
============

%s

""" % (
    read("README.rst"),
    name,
    read("CHANGES.rst"),
    read("CONTRIBUTORS.rst"),
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
    url="https://github.com/plone/plone.recipe.precompiler",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Buildout",
    ],
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    namespace_packages=["plone", "plone.recipe"],
    install_requires=["zc.buildout", "setuptools", "zc.recipe.egg", "python_gettext",],
    dependency_links=["http://download.zope.org/distribution/"],
    zip_safe=False,
    entry_points={"zc.buildout": ["default=%s:Recipe" % name]},
)
