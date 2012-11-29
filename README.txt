========================
plone.recipe.precompiler
========================

Why precompilation?
===================

There are .py and .po files. For .py files it is sane and for .po files
it is essential to be compiled for zope to make use of. In case you run 
zope under a user that has no write access to the code directories, you 
have a problem and you'd like the precompiling to happen before zope is
started.

Usage
=====

for example::

    [buildout]
    parts =
        ...
        precompile
    eggs = ...


    [precompile]
    recipe = plone.recipe.precompiler
    eggs = ${buildout:eggs}
    compile-mo-files = true


old, but should still work
--------------------------

ZC Buildout recipe for precompiling Python in product directories

This recipe searches for Python scripts with .py filename extensions and
compiles them into .pyc bytecode files.

It will compile all the files in specified directories and their descendents. A
"skip" list of directory names will be bypassed.

Precompiling Python code files to bytecode can prevent the Zope process from
writing out .pyc files as it operates -- which requires that the daemon process
be able to write into program directories.

This recipe may return harmless warnings regarding the inability to compile skin
layer scripts, which typically have "return" outside of a function. While these
warnings are harmless, you may suppress them by tuning the skip list.


Usage (old)
-----------

When used in a typical Plone install, usage is as simple as::

    [precompile]
    recipe = plone.recipe.precompiler
    
    When used in a different type of install, or with a need for manual tuning::
    
    [precompile]
    recipe = plone.recipe.precompiler
    dirs = list of dirs
        in multiple
        indented lines
    skip = list of skip
        directories
        in multiple
        indented lines
    rx = individual file exclusion regular expression


Default usage is equivalent to::

    [instance]
    ...
    [precompile]
    recipe = plone.recipe.precompiler
    skip =
        tests
        skins
        doc
        kupu_plone_layer
        Extensions
        .svn
    rx = /\.
