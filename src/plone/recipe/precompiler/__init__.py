import os
import compileall
import logging
import subprocess
import zc.buildout
import zc.recipe.egg


class Recipe:

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.options, self.name = buildout, options, name

        # self.logger = logging.getLogger(self.name)
        self.logger = buildout._logger
        self._do_compile_mo_files = options.get('compile-mo-files', False) and \
                options['compile-mo-files'].lower() == 'true'

        # provide 'extra-paths' alias to 'dirs'
        if not 'dirs' in options:
            options['dirs'] = options.get('extra-paths', '')

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
        import pdb; pdb.set_trace()
        return self.ws.entries + self.options['dirs'].split()

    def _compile_eggs(self):
        for pkgdir in self.pkgdirs:
            self.logger.debug('Compiling egg: %s.' % pkgdir)
            compileall.compile_dir(pkgdir, quiet=1)

    def _compile_mo_files(self):
        def compile_mo_file(podir, pofile):
            mofile = os.path.join(podir, pofile[:-3] + '.mo')
            pofile = os.path.join(podir, pofile)
            # check timestamps:
            try:
                do_compile = os.stat(mofile).st_mtime < os.stat(pofile).st_mtime
            except OSError:
                do_compile = True
            if do_compile:
                self.logger.debug('Start compiling po-file: %s.' % pofile)
                return subprocess.Popen(['msgfmt', '-o', mofile, pofile])
            else:
                self.logger.debug('Mo-file already up-to-date: %s.' % mofile)

        children = []
        for pkgdir in self.pkgdirs:
            for dir, subdirs, files in os.walk(pkgdir):
                pofiles = filter(lambda x: x.endswith('.po'), files)
                for pofile in pofiles:
                    child = compile_mo_file(dir, pofile)
                    if child is not None:
                        children.append(child)
        while children:
            for i, child in enumerate(children):
                if child.poll() is not None:
                    del children[i]
                else:
                    self.logger.debug('Waiting for process %s.' % child.pid)
        self.logger.info('All locale compilations finished.')
