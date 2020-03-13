# -*- coding: utf-8 -*-
import os
import py_compile
import subprocess
import zc.buildout
import zc.recipe.egg

from pythongettext.msgfmt import Msgfmt
from pythongettext.msgfmt import PoSyntaxError


class Recipe:
    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options["recipe"], options)
        self.buildout, self.options, self.name = buildout, options, name

        # self.logger = logging.getLogger(self.name)
        self.logger = buildout._logger
        self._do_compile_mo_files = (
            options.get("compile-mo-files", False)
            and options["compile-mo-files"].lower() == "true"
        )

        self._quiet = options.get("quiet", "true").lower() == "true"

        # provide 'extra-paths' alias to 'dirs'
        if not "dirs" in options:
            options["dirs"] = options.get("extra-paths", "")

    def install(self):
        return self._run()

    def update(self):
        return self._run()

    def _run(self):
        self._compile_eggs()
        self._do_compile_mo_files and self._compile_mo_files()
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
        return self.ws.entries + self.options["dirs"].split()

    def _compile_eggs(self):
        self.logger.info("Compiling Python files.")
        for pkgdir in self.pkgdirs:
            for dir, subdirs, files in os.walk(pkgdir):
                pyfiles = filter(lambda x: x.endswith(".py"), files)
                for pyfile in pyfiles:
                    fn = os.path.join(dir, pyfile)
                    cfile = fn + "c"
                    ftime = os.stat(fn).st_mtime
                    try:
                        ctime = os.stat(cfile).st_mtime
                    except os.error:
                        ctime = 0
                    if ctime < ftime:
                        self.logger.debug("Compiling %s" % fn)
                        try:
                            py_compile.compile(fn, None, None, True)
                        except py_compile.PyCompileError as err:
                            msg = err.args[0]
                            if ("'return' outside function" in msg) and self._quiet:
                                self.logger.debug(msg)
                            else:
                                self.logger.error(msg)

    def _compile_mo_files(self):
        def compile_mo_file(podir, pofile):
            domain = pofile[:-3]
            mofile = os.path.join(podir, domain + ".mo")
            pofile = os.path.join(podir, pofile)
            # check timestamps:
            try:
                do_compile = os.stat(mofile).st_mtime < os.stat(pofile).st_mtime
            except OSError:
                do_compile = True
            if do_compile:
                self.logger.debug("Compiling po-file: %s" % pofile)
                try:
                    mo = Msgfmt(pofile, name=domain).getAsFile()
                    fd = open(mofile, "wb")
                    fd.write(mo.read())
                    fd.close()
                except (IOError, OSError, PoSyntaxError):
                    msg = "Error while compiling language file %s" % mofile
                    if self._quiet:
                        self.logger.debug(msg)
                    else:
                        self.logger.error(msg)

        self.logger.info("Compiling locale files.")
        for pkgdir in self.pkgdirs:
            for dir, subdirs, files in os.walk(pkgdir):
                pofiles = [file for file in files if file.endswith(".po")]
                for pofile in pofiles:
                    compile_mo_file(dir, pofile)
