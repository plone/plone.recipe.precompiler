========================
plone.recipe.precompiler
========================

Buildout recipe to precompiles Python and locale files in an egg list.

Why precompilation?
===================

Python ordinarily compiles .py files into .pyc or .pyo byte code files
on demand. Likewise, applications like Plone often compile .po locale
files into .mo representations when needed.

However, if you are running a Python application as a daemon and wish
to prevent write access to code directories, you want to do these
compilations at buildout-time, not run-time. That's where this recipe
comes in. Passed an egg list, it will pick up all the eggs in the
buildout working set for the list and find and compile .py and .mo
files in place.

.mo file compilation is optional, and must be turned on.

Usage
=====

Please note that usage changed with release 0.5. If you need the old
options, use 0.4

Common usage::

    [buildout]
    parts =
        ...
        precompile
    eggs = ...


    [precompile]
    recipe = plone.recipe.precompiler
    eggs = ${buildout:eggs}
    compile-mo-files = true


This recipe may return harmless warnings regarding the inability to compile skin
layer scripts, which typically have "return" outside of a function. While these
warnings are harmless, you may suppress them by tuning the skip list.


Options
-------

    recipe = plone.recipe.precompiler

    eggs = required: list of eggs

    compile-mo-files = true/false; default is false

    extra-paths = optional list of additional paths
        that would not be found from eggs
        in multiple
        indented lines

    quiet = true/false; if true, common errors are only shown when buildout's
        verbose flag is set.

Notes
=====

This recipe was created for use in Plone installers, but is hopefully useful in
many buildout contexts.