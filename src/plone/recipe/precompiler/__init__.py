##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

# ZC Buildout recipe for precompiling Python in product directories

# The compile_non_skip function is derived from Zope's compilezpy.py,
# which is licensed under the ZPL.


DefaultSkipDirs = """tests
skins
doc
kupu_plone_layer
Extensions
.svn"""

DefaultRX = r"/\."


import os, re, shutil, re
import compileall
import logging
import subprocess
import zc.buildout
import zc.recipe.egg

def compile_non_skip(dir, skip, rx):
    """Byte-compile all modules except those in skip directories."""
    
    # compile current directory
    compileall.compile_dir(dir, maxlevels=0, quiet=1, rx=rx)
    # get a list of child directories
    try:
        names = os.listdir(dir)
    except os.error:
        print "Can't list", dir
        names = []
    # visit subdirectories, calling self recursively
    # skip os artifacts and skip list.
    for name in names:
        fullname = os.path.join(dir, name)
        if (name != os.curdir and name != os.pardir and
                os.path.isdir(fullname) and not os.path.islink(fullname) and
                name not in skip):
            compile_non_skip(fullname, skip, rx)

class Recipe:

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.options, self.name = buildout, options, name

        self.logger = logging.getLogger(self.name)
        self._new_style = options.get('eggs', False)
        self._do_compile_mo_files = options.get('compile-mo-files', False) and \
                options['compile-mo-files'].lower() == 'true'

        # XXX:  support for extra-paths, more usual than "dirs" 

        # BBB 2010-08-12
        options['scripts'] = '' # suppress script generation.

        if not options.has_key('dirs'):
            options['dirs'] = ''

        options.setdefault('skip', DefaultSkipDirs)
        options.setdefault('rx', DefaultRX)

    def install(self):
        return self._run()

    def update(self):
        return self._run()

    def _run(self):
        if self._new_style:
            self._compile_eggs()
            self._do_compile_mo_files and self._compile_mo_files()
        else:
            # BBB 2010-08-12
            self.compileAll()
        return []

    @property
    def ws(self):
        try:
            return self._ws
        except AttributeError:
            self._ws = self.egg.working_set()[1]
            return self._ws

    @property
    def pkgdirs(self):
        return self.ws.entries

    def _compile_eggs(self):
        for pkgdir in self.pkgdirs:
            self.logger.info('Compiling egg: %s.' % pkgdir)
            compileall.compile_dir(pkgdir, quiet=1)

    def _compile_mo_files(self):
        def compile_mo_file(podir, pofile):
            mofile = os.path.join(podir, pofile[:-3]+'.mo')
            pofile = os.path.join(podir, pofile)
            # check timestamps:
            try:
                do_compile = os.stat(mofile).st_mtime < os.stat(pofile).st_mtime
            except OSError:
                do_compile = True
            if do_compile:
                self.logger.info('Start compiling po-file: %s.' % pofile)
                return subprocess.Popen(['msgfmt', '-o', mofile, pofile])
            else:
                self.logger.info('Mo-file already up-to-date: %s.' % mofile)

        childs = []
        for pkgdir in self.pkgdirs:
            for dir, subdirs, files in os.walk(pkgdir):
                pofiles = filter(lambda x: x.endswith('.po'), files)
                for pofile in pofiles:
                    child = compile_mo_file(dir, pofile)
                    if child is not None:
                        childs.append(child)
        while childs:
            for i, child in enumerate(childs):
                if child.poll() is not None:
                    del childs[i]
                else:
                    self.logger.info('Waiting for process %s.' % child.pid)
        self.logger.info('All locale compilations finished.')

    # BBB 2010-08-12
    def compileAll(self):
        
        dirs = self.options['dirs'].split()
        skip = self.options['skip'].split()
        rexp = self.options['rx']

        if rexp:
            rx = re.compile(rexp)
        else:
            rx = None
        for dir in dirs:
            print '  precompiling python scripts in %s' % dir
            compile_non_skip(dir, skip, rx)
