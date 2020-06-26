0.7.3 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- *add item here*


0.7.2 (2020-06-26)
------------------

Bug fixes:

- Small packaging updates.  [gforcada, jensens, maurits]


0.7.1 (2018-11-11)
------------------

Bug fixes:

- Rerelease to fix Python 3 issue in 0.7
  [esteele]


0.7 (2018-11-07)
----------------

Bug fixes:

- Fix reversion in 0.6, displaying too many .po compile errors.

0.6 (2012-12-17)
----------------

- Use python_gettext rather than msgfmt to compile .po files. Removes
  dependence on gettext.
  (smcmahon)

0.5
---

- Suck up error messages and filter them to hide .po compile errors
  and .py "return outside function" errors when quiet option is true (default).
  (smcmahon)

- Make the extra-paths work with the new working set method for finding eggs.
  (smcmahon)

- Removed BBB code. The new way of finding eggs introduced by chaoflow is much
  better than my original.
  (smcmahon)

- removed the functionality to automatically extract products directories from
  parts with the zope2instance recipe. This resulted in buildouts that always
  installed ALL parts. If you need the products dir, you must declare it explicitly
  like so: dirs = ${instance:products}
  (do3cc - 2012-07-12)


0.4 (2010-08-12)
----------------

- support for walking eggs dependencies, without skip/rx, manually tested.
  (chaoflow - 2010-08-12)

- support for compiling mo files in those egg dirs, manually tested.
  (chaoflow - 2010-08-12)

- kept old syntax and code, just don't specify eggs (untested)

0.3
---

- support to recursively compile list of dirs, with subdir blacklist and file
  blacklist regex.
  (Steve McMahon)

